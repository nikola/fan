# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import time
from multiprocessing import Process
from Queue import Empty

from pants.web import Application
from pants.http import HTTPServer
from pants import Engine as HttpServerEngine

from settings import DEBUG
from settings.net import ENFORCED_CIPHERS
from server.routes import module as appRoutes
from models import ImageManager


def _startHttpServer(queue, port, certificateFile, userAgent):

    def proxy(request):
        if DEBUG or (request.is_secure and request.protocol == 'HTTP/1.1' and request.headers.get('User-Agent', None) == userAgent):
            app(request)
        else:
            request.finish()
            request.connection.close()

    imageManager = ImageManager()

    appRoutes.interProcessQueue = queue
    appRoutes.presented = False
    appRoutes.imageManager = imageManager

    app = Application(debug=DEBUG)
    app.add('/', appRoutes)

    sslOptions = dict(do_handshake_on_connect=False, server_side=True, certfile=certificateFile, ssl_version=3, ciphers=ENFORCED_CIPHERS)
    HTTPServer(proxy).startSSL(sslOptions).listen(('', port))

    engine = HttpServerEngine.instance()



    while True:
        try:
            command = queue.get_nowait()
            if command == 'stop:server':
                if engine is not None:
                    print 'stopping server'
                    engine.stop()
                    engine = None

                imageManager.shutdown()

                queue.task_done()
                break
            else:
                queue.put(command)
                queue.task_done()
        except Empty:
            if engine is not None:
                engine.poll(poll_timeout=0.015)
            time.sleep(0.015)


def start(*args):
    global globalInterProcessQueue
    globalInterProcessQueue = args[0]

    process = Process(target=_startHttpServer, args=args)
    process.start()

    return process


def stop():
    global globalInterProcessQueue
    globalInterProcessQueue.put('stop:server')
