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

from models import StreamManager

from config import DEBUG, ENFORCED_CIPHERS
from settings.net import SERVER_HEADERS


class Publisher(WebSocket):

    def __init__(self, request, userAgent, bridgeToken, *args):
        print '__init__', args
        self.userAgent = userAgent
        self.bridgeToken = bridgeToken

        super(Publisher, self).__init__(request)

    def on_handshake(self, request, headers=SERVER_HEADERS):
        print 'on_handshake'

        if DEBUG or (request.is_secure and request.protocol == 'HTTP/1.1' and request.headers.get('Accept-Language', None) == 'en-us,en' and request.headers.get('User-Agent', None) == self.userAgent):
            return True
        else:
            return False


    def on_connect(self, *args):
        print 'on_connect'
        self.ping() # data=self.bridgeToken)


    def on_pong(self, data):
        print 'data ponged:', data
        global publisherInstance
        publisherInstance = self
        print 'sending:', repr(self.bridgeToken)
        self.write(unicode(self.bridgeToken), flush=True)


    def on_read(self, data):
        print 'on_read'
        self.write(data)


    def on_close(self):
        print 'on_close'
        global publisherInstance
        publisherInstance = None


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
    observer = Observer()
    observer.schedule(event_handler, r'M:\\', recursive=True)

    counter = 0

    sslOptions = dict(do_handshake_on_connect=False, server_side=True, certfile=certificateFile, ssl_version=3, ciphers=ENFORCED_CIPHERS)
    HTTPServer(proxy).startSSL(sslOptions).listen(port)

    engine = Engine.instance()

    global publisherInstance
    publisherInstance = None



    counter = 0
    while True:
        try:
            command = queue.get_nowait()
            if command == 'start:collector':
                streamManager = StreamManager()
                observer.start()
                queue.task_done()
            elif command == 'stop:collector':
                streamManager.shutdown()

                observer.stop()
                observer.join()

                if engine is not None:
                    engine.stop()
                    engine = None

                queue.task_done()
                break
            else:
                queue.put(command)
                queue.task_done()
        except Empty:
            if publisherInstance is not None:
                publisherInstance.write(unicode(counter))
                counter += 1
            if engine is not None:
                engine.poll(poll_timeout=0.015)
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
# def start(interProcessQueue, port, certificateLocation):
    global globalInterProcessQueue
    globalInterProcessQueue = args[0]

    process = Process(target=_startCollector, args=args)
    process.start()

    return process


def stop():
    global globalInterProcessQueue
    globalInterProcessQueue.put('stop:collector')
