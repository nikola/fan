# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@klaric.org)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import time
from contextlib import closing
from utils.system import Process
from Queue import Empty

from pants import Engine as HttpServerEngine
from pants.http import HTTPServer
from pants.web import Application

from models import StreamManager
from settings import DEBUG
from settings import APP_STORAGE_PATH
from orchestrator.urls import module as appModule
from orchestrator.pubsub import PubSub
from downloader.images import processBacklogEntry
from identifier import getStreamRecords, getFixedRecords, identifyMovieByTitleYear, getEditVersionFromFilename
from utils.config import getCurrentUserConfig, getOverlayConfig, saveCurrentUserConfig
from utils.net import deleteResponseCache

from . import logger


def _getMovieRecordFromLocation(streamLocation, basedataFromStream, basedataFromDir, processCallback):
    processCallback()
    if not appModule.userConfig.get('isDemoMode', False):
        logger.info('Found new supported file: %s' % streamLocation)
    else:
        logger.info('Importing TOP 250 movie: "%s (%d)"' % (basedataFromStream['title'], basedataFromStream['year']))

    processCallback()

    movieRecord = identifyMovieByTitleYear(
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
        processBacklogEntry('backdrop', movieRecord.get('keyBackdrop'), processCallback)

    return movieRecord


def _startOrchestrator(queue, certificateLocation, userAgent, serverPort, bridgeToken, bootToken, mustSecure, userConfig, useExternalConfig):
    global pubSubReference
    pubSubReference = None

    def _getPubSubReference(reference):
        global pubSubReference
        pubSubReference = reference

    def _proxy(request):
        if DEBUG or (request.protocol == 'HTTP/1.1' and request.headers.get('User-Agent', None) == userAgent):
            # if request.headers.get('Sec-WebSocket-Version', None) == 13:
            if request.headers.get('Upgrade', None) == 'websocket':
                PubSub(queue, request, userAgent, bridgeToken, _getPubSubReference)
            else:
                app(request)
        else:
            request.finish()
            request.connection.close()

    def _processRequests():
        if engine is not None:
            engine.poll(poll_timeout=0.005)
        time.sleep(0)

    streamManager = StreamManager()
    streamGenerator = None
    syncFinished = False
    isDownloaderIdle = False

    appModule.interProcessQueue = queue
    appModule.streamManager = streamManager
    appModule.bootToken = bootToken
    appModule.userConfig = userConfig
    appModule.useExternalConfig = useExternalConfig

    if DEBUG:
        appModule.userAgent = userAgent
        appModule.serverPort = serverPort
    # END if DEBUG

    app = Application(debug=DEBUG)
    app.add('', appModule)

    if mustSecure:
        sslOptions = dict(
            do_handshake_on_connect=False,
            server_side=True,
            certfile=certificateLocation,
            ssl_version=3,
            ciphers='ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+3DES:!aNULL:!MD5:!DSS',
        )
        HTTPServer(_proxy).startSSL(sslOptions).listen(('', serverPort))
    else:
        HTTPServer(_proxy).listen(('', serverPort))

    engine = HttpServerEngine.instance()

    while True:
        _processRequests()

        try:
            command = queue.get_nowait()

            if command == 'orchestrator:start:scan':
                if useExternalConfig:
                    appModule.userConfig = getOverlayConfig(useExternalConfig)
                else:
                    appModule.userConfig = getCurrentUserConfig()

                if appModule.userConfig.get('isDemoMode', False):
                    appModule.userConfig['hasDemoMovies'] = True
                    appModule.userConfig = saveCurrentUserConfig(appModule.userConfig) # , useExternalConfig)

                    streamGenerator = getFixedRecords()
                else:
                    if appModule.userConfig.get('hasDemoMovies', False):
                        appModule.userConfig['hasDemoMovies'] = False
                        appModule.userConfig = saveCurrentUserConfig(appModule.userConfig) # , useExternalConfig)

                    streamGenerator = getStreamRecords(appModule.userConfig.get('sources', []))

                queue.task_done()
            elif command == 'orchestrator:reload:config':
                # appModule.userConfig = getCurrentUserConfig()
                if useExternalConfig:
                    appModule.userConfig = getOverlayConfig(useExternalConfig)
                else:
                    appModule.userConfig = getCurrentUserConfig()

                if appModule.userConfig.get('isDemoMode', False):
                    if not appModule.userConfig.get('hasDemoMovies', False):
                        streamManager.purge()
                elif appModule.userConfig.get('hasDemoMovies', False):
                    streamManager.purge()

                pubSubReference.write(unicode('["force:redirect:url", "load.asp"]'))

                queue.task_done()
            elif command == 'orchestrator:resume:detail':
                pubSubReference.write(unicode('["resume:detail:screen", ""]'))

                queue.task_done()
            elif command == 'orchestrator:player:updated':
                pubSubReference.write(unicode('["player:update:complete", ""]'))

                queue.task_done()
            elif command == 'orchestrator:wake-up:downloader':
                isDownloaderIdle = True

                queue.task_done()
            elif command == 'orchestrator:active:downloader':
                isDownloaderIdle = False

                queue.task_done()
            elif command == 'orchestrator:stop':
                if engine is not None:
                    if pubSubReference is not None:
                        pubSubReference.close()
                        pubSubReference = None
                    engine.stop()
                    engine = None

                streamManager.shutdown()

                queue.task_done()
                break
            elif command.startswith('orchestrator:poster-refresh:'):
                if pubSubReference is not None and pubSubReference.connected:
                    movieId = command.replace('orchestrator:poster-refresh:', '')
                    pubSubReference.write(unicode('["movie:poster:refresh", "%s"]' % movieId))
                    _processRequests()

                queue.task_done()
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

                    if not streamManager.isStreamKnown(streamLocation):
                        movieRecord = _getMovieRecordFromLocation(streamLocation, basedataFromStream, basedataFromDir, _processRequests)

                        if movieRecord is None:
                            logger.warning('Could not identify file: %s' % streamLocation)
                        else:
                            editVersion = getEditVersionFromFilename(streamLocation, basedataFromStream.get('year'))
                            movieId = streamManager.addMovieStream(movieRecord, streamLocation, editVersion) # TODO: re-wire stream to correct movie if necessary
                            _processRequests()

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
    globalInterProcessQueue = args[0]

    process = Process(target=_startOrchestrator, args=args)
    process.start()

    return process


def stop():
    global globalInterProcessQueue
    globalInterProcessQueue.put('orchestrator:stop')
