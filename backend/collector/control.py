# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import time
import logging
from Queue import Empty
from multiprocessing import Process

from pants.http import HTTPServer, WebSocket
from pants import Engine
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from settings import DEBUG
from settings.net import SERVER_HEADERS, ENFORCED_CIPHERS
from models import StreamManager
from collector.extractor import *


class Publisher(WebSocket):

    def __init__(self, request, userAgent, bridgeToken, *args):
        print '__init__', args
        self.userAgent = userAgent
        self.bridgeToken = bridgeToken

        super(Publisher, self).__init__(request)

    def on_handshake(self, request, headers=SERVER_HEADERS):
        print 'on_handshake'

        return DEBUG or (request.is_secure and request.protocol == 'HTTP/1.1' and request.headers.get('User-Agent', None) == self.userAgent)


    def on_connect(self, *args):
        print 'on_connect'
        self.ping() # data=self.bridgeToken)


    def on_pong(self, data):
        print 'data ponged:', data
        global publisherInstance
        publisherInstance = self
        # print 'sending:', repr(self.bridgeToken)
        # self.write(unicode(self.bridgeToken), flush=True)


    def on_read(self, data):
        print 'on_read'
        self.write(data)


    def on_close(self):
        print 'on_close'
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

    sslOptions = dict(do_handshake_on_connect=False, server_side=True, certfile=certificateFile, ssl_version=3, ciphers=ENFORCED_CIPHERS)
    HTTPServer(proxy).startSSL(sslOptions).listen(port)

    engine = Engine.instance()

    global publisherInstance
    publisherInstance = None

    streamGenerator = None

    while True:
        try:
            command = queue.get_nowait()
            if command == 'start:collector':
                streamManager = StreamManager()
                streamGenerator = getMoviePathnames(r'M:\\')

                streamWatcher.start()

                queue.task_done()
            elif command == 'stop:collector':
                streamManager.shutdown()

                streamWatcher.stop()
                streamWatcher.join()

                if engine is not None:
                    publisherInstance.close()
                    publisherInstance = None
                    engine.stop()
                    engine = None

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
                        # print basedata.get('title').ljust(70) + getEditVersionFromFilename(filename, basedata.get('year')).ljust(30) + streamLocation
                        publisherInstance.write(unicode('["receive:movie:item", "%s"]' % basedata.get('title')))
            elif False:
                pass # TODO: implement here kickoff of filewatcher
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
    globalInterProcessQueue.put('stop:collector')
