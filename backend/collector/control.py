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
from utils.fs import getLongPathname


class Publisher(WebSocket):

    def __init__(self, queue, request, userAgent, *args):
        self.queue = queue
        self.userAgent = userAgent

        super(Publisher, self).__init__(request)

    def on_handshake(self, request, headers=SERVER_HEADERS):
        return DEBUG or (request.is_secure and request.protocol == 'HTTP/1.1' and request.headers.get('User-Agent', None) == self.userAgent)

    def on_connect(self, *args):
        self.ping()

    def on_pong(self, data):
        global publisherInstance
        publisherInstance = self

    def on_read(self, data):
        command, payload = json.loads(data)
        if command == 'movie:play':
            self.queue.put('player:play:%s' % payload)

    def on_close(self):
        pass


def _startCollector(queue, port, certificateFile, userAgent):

    def proxy(request):
        Publisher(queue, request, userAgent)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # https://pythonhosted.org/watchdog/quickstart.html#a-simple-example
    # http://stackoverflow.com/questions/19991033/generating-multiple-observers-with-python-watchdog
    # http://stackoverflow.com/questions/21892080/combining-python-watchdog-with-multiprocessing-or-threading

    event_handler = LoggingEventHandler()
    streamWatcher = Observer()

    streamWatcher.schedule(event_handler, getLongPathname(r'\\DiskStation\Movies'), recursive=True)

    collectorStreamManager = None
    streamGenerator = None

    global publisherInstance
    publisherInstance = None

    sslOptions = dict(do_handshake_on_connect=False, server_side=True, certfile=certificateFile, ssl_version=3, ciphers=ENFORCED_CIPHERS)
    HTTPServer(proxy).startSSL(sslOptions).listen(port)

    engine = Engine.instance()

    syncFinished = False
    streamWatcherStarted = False

    while True:
        try:
            command = queue.get_nowait()

            if command == 'collector:start':
                if collectorStreamManager is None:
                    # print 'is publisher ready?', publisherInstance
                    collectorStreamManager = StreamManager()

                    # TODO: remove !!!
                    # collectorStreamManager.deleteStreams()

                    streamGenerator = getMoviePathnames(getLongPathname(r'\\Diskstation\Movies'))



                queue.task_done()
            elif command == 'collector:watch':
                print 'starting to watch filesystem'
                streamWatcher.start()
                streamWatcherStarted = True
                queue.task_done()
            elif command == 'collector:stop':
                print 'collector:stop received'
                if streamWatcherStarted:
                    print 'stopping streamWatcher'

                    streamWatcher.stop()
                    streamWatcher.join()
                    print 'stopped streamWatcher!'

                if engine is not None and collectorStreamManager is not None:
                    print 'attempting to close publisherInstance'
                    publisherInstance.close()
                    publisherInstance = None
                    engine.stop()
                    engine = None
                    print 'closed publisherInstance'

                if collectorStreamManager is not None:
                    print 'attempting to shut down collector stream manager ...'
                    collectorStreamManager.shutdown()
                    print '... shut down collector stream manager!'

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
                    syncFinished = True
                else:
                    basedata = getBaseDataFromDirName(container)

                    for filename in files:
                        # print 'processing file'
                        streamLocation = os.path.join(path, filename)

                        # if collectorStreamManager.isStreamKnown(streamLocation):
                        #     movie = collectorStreamManager.getMovieFromStreamLocation(streamLocation)
                        # else:
                        if not collectorStreamManager.isStreamKnown(streamLocation):
                            movieRecord = identifyMovieByTitleYear('en', 'us', basedata.get('title'), basedata.get('year'))
                            if movieRecord is None:
                                print 'unknown stream:', streamLocation

                            # TODO: call getEditVersionFromFilename(filename, year)

                            movie = collectorStreamManager.addMovieStream(movieRecord, streamLocation)
                            # else:
                            #     movie = None

                            if movie is not None:
                                publisherInstance.write(unicode('["receive:movie:item", %s]'
                                    % collectorStreamManager.getMovieAsJson(movie.uuid)))

                                # collectorStreamManager.deleteMovie(movie.uuid)

            elif syncFinished is True:
                syncFinished = None

                queue.put('collector:watch')
                queue.put('downloader:start')
            else:
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
    print 'putting collector:stop ...'
    globalInterProcessQueue.put('collector:stop')
