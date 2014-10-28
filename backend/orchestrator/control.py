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

import os
import time
from contextlib import closing
from utils.system import Process
from Queue import Empty

from simplejson import JSONDecodeError
from pants import Engine as HttpServerEngine
from pants.http import HTTPServer
from pants.web import Application
from pants.web.fileserver import FileServer

from models import StreamManager
from settings import DEBUG
from settings import APP_STORAGE_PATH, STATIC_PATH, SERVER_PORT
from orchestrator.urls import module as appModule
from orchestrator.pubsub import PubSub
from downloader.images import processBacklogEntry, downloadArtwork
from identifier import getStreamRecords, getFixedRecords, identifyMovieByTitleYear, getShorthandFromFilename
from utils.config import processCurrentUserConfig
from utils.net import deleteResponseCache
from utils.logs import getLogger


def _getMovieRecordFromLocation(profile, streamLocation, basedataFromStream, basedataFromDir, processCallback):
    processCallback()

    logger = getLogger(profile, 'orchestrator')

    if not appModule.userConfig.get('isDemoMode', False):
        logger.info('Found new supported file: %s' % streamLocation)
    else:
        logger.info('Importing TOP 250 movie: "%s (%d)"' % (basedataFromStream['title'], basedataFromStream['year']))

    processCallback()

    movieRecord = identifyMovieByTitleYear(
        profile,
        appModule.userConfig.get('language', 'en'),
        basedataFromDir.get('title'), basedataFromDir.get('year'),
        basedataFromStream.get('title'), basedataFromStream.get('year'),
        processCallback,
    )

    if movieRecord is not None:
        for imageType in ('Poster', 'Backdrop'):
            movieRecord['key' + imageType] = movieRecord['url' + imageType].replace('/', '').replace('.jpg', '')
            pathname = os.path.join(APP_STORAGE_PATH, 'artwork', imageType.lower() + 's', movieRecord['key' + imageType])
            try:
                os.makedirs(pathname)
            except OSError:
                pass
            processCallback()
            with open(os.path.join(pathname, 'source.url'), 'wb+') as fp:
                fp.write('[InternetShortcut]\r\nURL=%soriginal%s\r\n' % (appModule.imageBaseUrl, movieRecord['url' + imageType]))
            processCallback()
            closing(open(os.path.join(APP_STORAGE_PATH, 'backlog', imageType.lower() + 's', movieRecord['key' + imageType]), 'w+'))
            processCallback()
            del movieRecord['url' + imageType]

    return movieRecord


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

                    streamGenerator = getStreamRecords(appModule.userConfig.get('sources', []))

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

                    isContainerKnown = streamManager.isStreamKnown(streamLocation)
                    _processRequests()

                    if not isContainerKnown:
                        try:
                            movieRecord = _getMovieRecordFromLocation(profile, streamLocation, basedataFromStream, basedataFromDir, _processRequests)
                        except (JSONDecodeError, AttributeError, TypeError, KeyError):
                            logger.error('Error while querying themoviedb.org')
                        else:
                            if movieRecord is None:
                                logger.warning('Could not identify file: %s' % streamLocation)
                            else:
                                processBacklogEntry(profile, 'backdrop', movieRecord.get('keyBackdrop'), _processRequests)
                                downloadArtwork(profile, '%s%s/%s.jpg' % (appModule.imageBaseUrl,  appModule.imageClosestSize, movieRecord.get('keyPoster')), 'poster@draft', movieRecord.get('keyPoster'), _processRequests)

                            version = getShorthandFromFilename(streamLocation, basedataFromStream.get('year'))
                            _processRequests()
                            movieId = streamManager.addMovieStream(movieRecord, streamLocation, version) # TODO: re-wire stream to correct movie if necessary
                            _processRequests()

                            if movieRecord is not None:
                                if pubSubReference.connected:
                                    pubSubReference.write(unicode('["receive:movie:item", %s]' % streamManager.getMovieAsJson(movieId)))
                                    _processRequests()

                                if isDownloaderIdle:
                                    queue.put('downloader:resume')
                                    _processRequests()

            elif syncFinished is True:
                deleteResponseCache()

                syncFinished = None

                queue.put('downloader:missing:artwork') # TODO: rename to downloader:restock:artwork

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
