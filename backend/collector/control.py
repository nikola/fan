# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import time
import logging
import json
from Queue import Empty
from multiprocessing import Process

from pants.http import HTTPServer, WebSocket
from pants import Engine
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from settings import DEBUG
from settings.net import SERVER_HEADERS, ENFORCED_CIPHERS
from models import StreamManager
from collector.extractor import getMoviePathnames, getBaseDataFromDirName
from collector.identifier import identifyMovieByTitleYear


class Publisher(WebSocket):

    def __init__(self, request, userAgent, bridgeToken, *args):
        # print '__init__', args
        self.userAgent = userAgent
        self.bridgeToken = bridgeToken

        super(Publisher, self).__init__(request)

    def on_handshake(self, request, headers=SERVER_HEADERS):
        # print 'on_handshake'

        return DEBUG or (request.is_secure and request.protocol == 'HTTP/1.1' and request.headers.get('User-Agent', None) == self.userAgent)


    def on_connect(self, *args):
        # print 'on_connect'
        self.ping() # data=self.bridgeToken)


    def on_pong(self, data):
        # print 'data ponged:', data
        global publisherInstance
        publisherInstance = self
        # print 'sending:', repr(self.bridgeToken)
        # self.write(unicode(self.bridgeToken), flush=True)


    def on_read(self, data):
        # print 'on_read'
        self.write(data)


    def on_close(self):
        pass
        # print 'on_close'
        # self.close(flush=True)
        # global publisherInstance
        # publisherInstance = None


def _startCollector(queue, port, certificateFile, userAgent, bridgeToken):

    # streamManager = StreamManager()

    def proxy(request):
        Publisher(request, userAgent, bridgeToken)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # https://pythonhosted.org/watchdog/quickstart.html#a-simple-example
    # http://stackoverflow.com/questions/19991033/generating-multiple-observers-with-python-watchdog
    # http://stackoverflow.com/questions/21892080/combining-python-watchdog-with-multiprocessing-or-threading

    event_handler = LoggingEventHandler()
    streamWatcher = Observer()
    streamWatcher.schedule(event_handler, r'M:\\', recursive=True)
    collectorStreamManager = None
    streamGenerator = None

    global publisherInstance
    publisherInstance = None

    sslOptions = dict(do_handshake_on_connect=False, server_side=True, certfile=certificateFile, ssl_version=3, ciphers=ENFORCED_CIPHERS)
    HTTPServer(proxy).startSSL(sslOptions).listen(port)

    engine = Engine.instance()

    while True:
        try:
            command = queue.get_nowait()
            if command == 'collector:start':
                if collectorStreamManager is None:
                    collectorStreamManager = StreamManager()

                    # TODO: remove !!!
                    # collectorStreamManager.deleteStreams()


                    streamGenerator = getMoviePathnames(r'M:\\')

                    streamWatcher.start()

                queue.task_done()
            elif command == 'collector:stop':
                if collectorStreamManager is not None:
                    streamWatcher.stop()
                    streamWatcher.join()

                if engine is not None and collectorStreamManager is not None:
                    publisherInstance.close()
                    publisherInstance = None
                    engine.stop()
                    engine = None

                if collectorStreamManager is not None:
                    collectorStreamManager.shutdown()

                queue.task_done()
                break
            else:
                queue.put(command)
                queue.task_done()
        except Empty:
            if engine is not None:
                engine.poll(poll_timeout=0.015)

            if publisherInstance is not None and publisherInstance.connected and streamGenerator is not None:
                try:
                    (path, container, files) = streamGenerator.next()
                except StopIteration:
                    streamGenerator = None
                else:
                    basedata = getBaseDataFromDirName(container)



                    for filename in files:
                        streamLocation = os.path.join(path, filename)

                        # if collectorStreamManager.isStreamKnown(streamLocation):
                        #     movie = collectorStreamManager.getMovieFromStreamLocation(streamLocation)
                        # else:
                        if not collectorStreamManager.isStreamKnown(streamLocation):
                        # if True:
                            movieRecord = identifyMovieByTitleYear('en', 'us', basedata.get('title'), basedata.get('year'))
                            if movieRecord is None:
                                print 'unknown stream:', streamLocation
                            movie = collectorStreamManager.addMovieStream(movieRecord, streamLocation)
                            # else:
                            #     movie = None


                            # TODO: also create ImageManager() here and write dummy entry containing the GUID of movie
                            # then pass along GUID via web socket


                            if movie is not None:
                                movie = collectorStreamManager.getMovieAsJson(movie.uuid)
                                # publisherInstance.write(unicode('["receive:movie:item", "%s"]' % movie.titleOriginal))
                                # publisherInstance.write(unicode('["receive:movie:item", "%s"]' % movie.urlPoster))
                                # publisherInstance.write(unicode('["receive:movie:item", "%s"]' % movie.idTheMovieDb))

                                # print unicode('["receive:movie:item", %s]' % json.dumps(movie, separators=(',',':')))

                                publisherInstance.write(unicode('["receive:movie:item", %s]' % json.dumps(movie, separators=(',',':'))))

                                # collectorStreamManager.deleteMovie(movie.uuid)
            elif False: # elif ... all files collected in above generator loop
                pass # TODO: implement here kickoff of filewatcher
            else:
                # only 30 requests every 10 seconds per IP
                time.sleep(0.015)


def _dummy():
    """
        for (path, container, files) in getMoviePathnames(r"M:\\"):
            basedata = getBasedataFromPathname(container)

            for filename in files:
                streamLocation = os.path.join(path, filename)
                print streamLocation
                continue

                print "processing %s" % streamLocation
                movieRecord = getMovieFromRawData("de", "de", basedata["title"], basedata["year"])
                if movieRecord is None: continue

                print "adding %s from %s" % (movieRecord["titleOriginal"], streamLocation)
                streamManager.addMovieStream(movieRecord, streamLocation)

                time.sleep(0.5)
    """


def start(*args):
    global globalInterProcessQueue
    globalInterProcessQueue = args[0]

    process = Process(target=_startCollector, args=args)
    process.start()

    return process


def stop():
    global globalInterProcessQueue
    globalInterProcessQueue.put('collector:stop')
