# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import time
from utils.system import Process
from Queue import Empty

from pants import Engine as HttpServerEngine
from pants.http import HTTPServer
from pants.web import Application

from settings import DEBUG
from orchestrator.urls import module as appModule
from orchestrator.pubsub import PubSub
from models import StreamManager
from identifier import getStreamRecords, getFixedRecords, identifyMovieByTitleYear
from utils.config import getCurrentUserConfig

from . import logger


def _startOrchestrator(queue, certificateLocation, userAgent, serverPort, bridgeToken, bootToken, mustSecure, userConfig):
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
            engine.poll(poll_timeout=0.015)

    # logging.basicConfig(level=logging.INFO,
    #                     format='%(asctime)s - %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S')

    # https://pythonhosted.org/watchdog/quickstart.html#a-simple-example
    # http://stackoverflow.com/questions/19991033/generating-multiple-observers-with-python-watchdog
    # http://stackoverflow.com/questions/21892080/combining-python-watchdog-with-multiprocessing-or-threading

    # event_handler = LoggingEventHandler()
    # streamWatcher = Observer()

    # streamWatcher.schedule(event_handler, getLongPathname(r'\\DiskStation\Movies'), recursive=True)




    streamManager = StreamManager()
    streamGenerator = None
    syncFinished = False
    # streamWatcherStarted = False
    isDownloaderIdle = False
    # isImportingDemoMovies = False

    appModule.interProcessQueue = queue
    # appModule.presented = False
    appModule.streamManager = streamManager
    appModule.bootToken = bootToken
    appModule.userConfig = userConfig

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
                appModule.userConfig = getCurrentUserConfig()

                if appModule.userConfig.get('isDemoMode', False): # and not appModule.userConfig.get('hasDemoMovies', False):
                    appModule.userConfig['hasDemoMovies'] = True
                    appModule.userConfig = getCurrentUserConfig(appModule.userConfig)

                    streamGenerator = getFixedRecords()
                    # isImportingDemoMovies = True
                else: # if not appModule.userConfig.get('isDemoMode', False):
                    if appModule.userConfig.get('hasDemoMovies', False):
                        appModule.userConfig['hasDemoMovies'] = False
                        appModule.userConfig = getCurrentUserConfig(appModule.userConfig)

                    streamGenerator = getStreamRecords(appModule.userConfig.get('sources', []))
                    # isImportingDemoMovies = False
                # else:
                #     streamGenerator = None
                #     isImportingDemoMovies = False

                queue.task_done()
            # elif command == 'orchestrator:watch':
            #     # streamWatcher.start()
            #     streamWatcherStarted = True
            #     queue.task_done()
            elif command == 'orchestrator:reload:config':
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
            elif command == 'orchestrator:stop:all':
                # if streamWatcherStarted:
                #     streamWatcher.stop()
                #     streamWatcher.join()

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
                    movieUuid = command.replace('orchestrator:poster-refresh:', '')
                    pubSubReference.write(unicode('["movie:poster:refresh", "%s"]' %movieUuid))

                queue.task_done()
            else:
                queue.task_done()
                queue.put(command)

                time.sleep(0.015)
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
                        # if not isImportingDemoMovies:
                        if not appModule.userConfig.get('isDemoMode', False):
                            logger.info('Found new supported file: %s' % streamLocation)
                        else:
                            logger.info('Importing TOP 250 movie: "%s (%d)"' % (basedataFromStream['title'], basedataFromStream['year']))

                        _processRequests()

                        movieRecord = identifyMovieByTitleYear(
                            userConfig.get('language', 'en'),
                            basedataFromDir.get('title'), basedataFromDir.get('year'),
                            basedataFromStream.get('title'), basedataFromStream.get('year'),
                        )
                        _processRequests()

                        if movieRecord is None:
                            logger.warning('Could not identify file: %s' % streamLocation) # TODO: handle this! perhaps try again when app is re-launched?

                        movieUuid = streamManager.addMovieStream(movieRecord, streamLocation) # TODO: re-wire stream to correct movie if necessary

                        _processRequests()

                        if movieRecord is not None:
                            if pubSubReference.connected:
                                pubSubReference.write(unicode('["receive:movie:item", %s]' % streamManager.getMovieAsJson(movieUuid)))
                                _processRequests()
                            if isDownloaderIdle:
                                queue.put('downloader:resume')

            elif syncFinished is True:
                syncFinished = None

                # queue.put('orchestrator:watch')
                queue.put('downloader:start')

            _processRequests()
            # elif syncFinished is False:
            #     time.sleep(0.015)
            # else:
            #     if engine is not None: engine.poll(poll_timeout=0.015)


def start(*args):
    global globalInterProcessQueue
    globalInterProcessQueue = args[0]

    process = Process(target=_startOrchestrator, args=args)
    process.start()

    return process


def stop():
    global globalInterProcessQueue
    globalInterProcessQueue.put('orchestrator:stop:all')
