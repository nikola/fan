# coding: utf-8
"""
fan - A movie compilation and playback app for Windows. Fast. Lean. No weather widget.
Copyright (C) 2013-2014 Nikola Klaric.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
__author__ = 'Nikola Klaric (nikola@klaric.org)'
__copyright__ = 'Copyright (C) 2013-2014 Nikola Klaric'

import time
from utils.system import Process
from Queue import Empty

from pants import Engine as HttpServerEngine
from pants.http import HTTPServer
from pants.web import Application
from pants.web.fileserver import FileServer

from models import StreamManager
from settings import DEBUG
from settings import STATIC_PATH, SERVER_PORT
from orchestrator.urls import module as appModule
from orchestrator.pubsub import PubSub
from downloader.images import processBacklogEntry, downloadArtwork
from identifier import getContainerCount, getStreamRecords, getFixedRecords, getShorthandFromFilename, getMovieRecordFromLocation, getClientMovieRecordAsJson
from utils.config import processCurrentUserConfig
from utils.net import deleteResponseCache
from utils.logs import getLogger


def _startOrchestrator(profile, queue):
    global pubSubReference
    pubSubReference = None

    def _getPubSubReference(reference):
        global pubSubReference
        pubSubReference = reference

    def _proxy(request):
        if request.protocol == 'HTTP/1.1':
            if request.headers.get('Upgrade', '') == 'websocket':
                PubSub(request, queue, _getPubSubReference)
            else:
                app(request)
        else:
            request.finish()
            request.connection.close()

    def _processRequests():
        if engine is not None:
            engine.poll(poll_timeout=0.015)
        else:
            time.sleep(0.015)

    streamManager = StreamManager(profile)
    streamGenerator = None
    syncFinished = False
    isDownloaderIdle = False
    mustSendContainerCount = None
    mustSendPosterCount = None
    logger = getLogger(profile, 'orchestrator')

    appModule.interProcessQueue = queue
    appModule.streamManager = streamManager
    appModule.profile = profile
    appModule.userConfig = processCurrentUserConfig(profile)

    app = Application(debug=DEBUG)
    app.add('', appModule)
    FileServer(STATIC_PATH, headers={'Cache-Control': 'no-cache,max-age=0'}).attach(app, '/static/')

    HTTPServer(_proxy).listen(('', SERVER_PORT))
    engine = HttpServerEngine.instance()

    while True:
        _processRequests()

        try:
            command = queue.get_nowait()

            if command == 'orchestrator:stop':
                if engine is not None:
                    if pubSubReference is not None:
                        pubSubReference.close()
                        pubSubReference = None
                    engine.stop()
                    engine = None

                streamManager.shutdown()

                queue.task_done()
                time.sleep(0)

                break
            elif command == 'orchestrator:start:scan':
                appModule.userConfig = processCurrentUserConfig(profile)

                if appModule.userConfig.get('isDemoMode', False):
                    appModule.userConfig['hasDemoMovies'] = True
                    processCurrentUserConfig(profile, appModule.userConfig)

                    streamGenerator = getFixedRecords()
                else:
                    if appModule.userConfig.get('hasDemoMovies', False):
                        appModule.userConfig['hasDemoMovies'] = False
                        processCurrentUserConfig(profile, appModule.userConfig)

                    mustSendContainerCount = getContainerCount(appModule.userConfig.get('sources', []))
                    _processRequests()

                    streamGenerator = getStreamRecords(appModule.userConfig.get('sources', []))
                    _processRequests()

                queue.task_done()

                _processRequests()
            elif command == 'orchestrator:reload:config':
                queue.task_done()
                queue.put('downloader:pause')
                time.sleep(0)

                syncFinished = False
                isDownloaderIdle = True

                appModule.userConfig = processCurrentUserConfig(profile)

                if appModule.userConfig.get('isDemoMode', False):
                    if not appModule.userConfig.get('hasDemoMovies', False):
                        streamManager.purge()
                elif appModule.userConfig.get('hasDemoMovies', False):
                    streamManager.purge()

                pubSubReference.write(unicode('["force:redirect:url", "load.html"]'))
                _processRequests()
            elif command == 'orchestrator:resume:detail':
                pubSubReference.write(unicode('["resume:detail:screen", ""]'))

                queue.task_done()
                _processRequests()
            elif command == 'orchestrator:player:updated':
                pubSubReference.write(unicode('["player:update:complete", ""]'))

                queue.task_done()
            elif command == 'orchestrator:wake-up:downloader':
                isDownloaderIdle = True

                queue.task_done()
                _processRequests()
            elif command == 'orchestrator:active:downloader':
                isDownloaderIdle = False

                queue.task_done()
                _processRequests()
            # elif command.startswith('orchestrator:poster-refresh:'):
            #     if pubSubReference is not None and pubSubReference.connected:
            #         movieId = command.replace('orchestrator:poster-refresh:', '')
            #         pubSubReference.write(unicode('["movie:poster:refresh", "%s"]' % movieId))
            #         _processRequests()

            #     queue.task_done()

            #     _processRequests()
            elif command.startswith('orchestrator:push:pending:poster-count:'):
                mustSendPosterCount = int(command[command.rindex(':')+1:])

                queue.task_done()
                _processRequests()
            elif command == 'orchestrator:push:poster-decrement':
                queue.task_done()

                if pubSubReference.connected:
                    pubSubReference.write(unicode('["receive:poster:decrement", 1]'))
                    _processRequests()
            elif command == 'orchestrator:push:posters-done':
                queue.task_done()

                if pubSubReference.connected:
                    pubSubReference.write(unicode('["receive:posters:processed", null]'))
                    _processRequests()
            else:
                queue.task_done()
                queue.put(command)

                _processRequests()
        except Empty:
            _processRequests()

            if streamGenerator is not None and pubSubReference is not None and pubSubReference.connected:
                try:
                    (streamLocation, basedataFromStream, basedataFromDir) = streamGenerator.next()
                except StopIteration:
                    streamGenerator = None
                    syncFinished = True
                else:
                    _processRequests()

                    if mustSendContainerCount and pubSubReference.connected:
                        pubSubReference.write(unicode('["receive:container:count", %d]' % mustSendContainerCount))
                        mustSendContainerCount = None
                        _processRequests()

                    isContainerKnown = streamManager.isStreamKnown(streamLocation)
                    _processRequests()

                    if pubSubReference.connected:
                        pubSubReference.write(unicode('["receive:container:decrement", 1]'))
                        _processRequests()

                    if not isContainerKnown:
                        try:
                            movieRecord = getMovieRecordFromLocation(
                                profile,
                                streamLocation,
                                basedataFromStream,
                                basedataFromDir,
                                appModule.userConfig,
                                appModule.imageBaseUrl,
                                _processRequests,
                            )
                        except (ValueError, AttributeError, TypeError, KeyError):
                            logger.error('Error while querying themoviedb.org')
                        else:
                            if movieRecord is None:
                                logger.warning('Could not identify file: %s' % streamLocation)
                            else:
                                # Pre-load backdrop and poster draft.
                                processBacklogEntry(profile, 'backdrop', movieRecord.get('keyBackdrop'), _processRequests)
                                downloadArtwork(profile, '%s%s/%s.jpg' % (appModule.imageBaseUrl,  appModule.imageClosestSize, movieRecord.get('keyPoster')), 'poster@draft', movieRecord.get('keyPoster'), _processRequests)

                            version = getShorthandFromFilename(streamLocation, basedataFromStream.get('year'))
                            _processRequests()
                            movieId = streamManager.addMovieStream(movieRecord, streamLocation, version)
                            _processRequests()

                            if movieId is not None:
                                if pubSubReference.connected:
                                    pubSubReference.write(unicode('["receive:movie:item", %s]' % getClientMovieRecordAsJson(movieId, movieRecord, streamLocation)))
                                    _processRequests()

                                if isDownloaderIdle:
                                    queue.put('downloader:resume')
                                    _processRequests()
            elif syncFinished is True:
                deleteResponseCache()

                syncFinished = None

                queue.put('downloader:process:missing:artwork')
            elif mustSendPosterCount and pubSubReference.connected:
                pubSubReference.write(unicode('["receive:poster:count", %d]' % mustSendPosterCount))
                mustSendPosterCount = None

            _processRequests()


def start(*args):
    global globalInterProcessQueue
    globalInterProcessQueue = args[1]

    process = Process(target=_startOrchestrator, args=args)
    process.start()

    return process


def stop():
    global globalInterProcessQueue
    globalInterProcessQueue.put('orchestrator:stop')
