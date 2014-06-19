# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import time
from multiprocessing import Process
from Queue import Empty

from pants import Engine as HttpServerEngine
from pants.http import HTTPServer
from pants.web import Application

from settings import DEBUG
from settings.net import ENFORCED_CIPHERS
from orchestrator.urls import module as appModule
from orchestrator.pubsub import PubSub
from models import StreamManager
from identifier import getMoviePathnames, getBaseDataFromDirName, identifyMovieByTitleYear
from utils.fs import getLongPathname


def _startOrchestrator(queue, certificateLocation, userAgent, serverPort, bridgeToken, bootToken):
    global pubSubReference
    pubSubReference = None

    def _getPubSubReference(reference):
        global pubSubReference
        pubSubReference = reference

    def _proxy(request):
        if DEBUG or (request.is_secure and request.protocol == 'HTTP/1.1' and request.headers.get('User-Agent', None) == userAgent):
            if request.headers.get('Sec-WebSocket-Version', None) == 13:
                PubSub(queue, request, userAgent, bridgeToken, _getPubSubReference)
            else:
                app(request)
        else:
            request.finish()
            request.connection.close()

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
    streamWatcherStarted = False

    appModule.interProcessQueue = queue
    appModule.presented = False
    appModule.streamManager = streamManager
    appModule.bootToken = bootToken
    if DEBUG:
        appModule.userAgent = userAgent
        appModule.serverPort = serverPort
    # END DEBUG

    app = Application(debug=DEBUG)
    app.add('', appModule)

    sslOptions = dict(do_handshake_on_connect=False, server_side=True, certfile=certificateLocation, ssl_version=3, ciphers=ENFORCED_CIPHERS)
    HTTPServer(_proxy).startSSL(sslOptions).listen(('', serverPort))

    engine = HttpServerEngine.instance()

    while True:
        try:
            command = queue.get_nowait()

            if command == 'orchestrator:start:scan':

                streamGenerator = getMoviePathnames(getLongPathname(r'\\Diskstation\Movies'))

                queue.task_done()
            elif command == 'orchestrator:watch':
                # streamWatcher.start()
                streamWatcherStarted = True
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
                movieUuid = command.replace('orchestrator:poster-refresh:', '')
                pubSubReference.write(unicode('["movie:poster:refresh", "%s"]' %movieUuid))

                queue.task_done()
            else:
                queue.put(command)
                queue.task_done()
        except Empty:
            if engine is not None:
                engine.poll(poll_timeout=0.015)

            if streamGenerator is not None and pubSubReference is not None and pubSubReference.connected:
                try:
                    (path, container, files) = streamGenerator.next()
                except StopIteration:
                    streamGenerator = None
                    syncFinished = True
                else:
                    basedata = getBaseDataFromDirName(container)

                    for filename in files:
                        streamLocation = os.path.join(path, filename)

                        if not streamManager.isStreamKnown(streamLocation):
                            movieRecord = identifyMovieByTitleYear('en', 'us', basedata.get('title'), basedata.get('year'))
                            if movieRecord is None:
                                print 'unknown stream:', streamLocation

                            # TODO: call getEditVersionFromFilename(filename, year)

                            movie = streamManager.addMovieStream(movieRecord, streamLocation)

                            if movie is not None:
                                pubSubReference.write(unicode('["receive:movie:item", %s]' % streamManager.getMovieAsJson(movie.uuid)))

            elif syncFinished is True:
                syncFinished = None

                queue.put('orchestrator:watch')
                queue.put('downloader:start')
            else:
                time.sleep(0.015)


def start(*args):
    global globalInterProcessQueue
    globalInterProcessQueue = args[0]

    process = Process(target=_startOrchestrator, args=args)
    process.start()

    return process


def stop():
    global globalInterProcessQueue
    globalInterProcessQueue.put('orchestrator:stop:all')
