# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

import socket
import os
from multiprocessing import Process
from pants.web import Application
from pants.http import HTTPServer
from pants import Engine
from server.routes import module as appRoutes
from server.cert import getCertificateFile


def _startHttpServer(userAgent, port , certfile):
    """
    """
    appRoutes.userAgent = userAgent

    app = Application(debug=True)

    app.add("/", appRoutes)
    HTTPServer(app).startSSL(dict(do_handshake_on_connect=False, server_side=True, certfile=certfile)).listen(("", port))

    Engine.instance().start()


def _getVacantPort():
    """
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def start(*args):
    """
    """
    global process, certfile

    port = _getVacantPort()
    args += port,

    certfile = getCertificateFile()
    args += certfile,

    process = Process(target=_startHttpServer, args=args)
    process.start()

    return port


def stop():
    """
    """
    global process, certfile

    os.remove(certfile)
    process.terminate()
