# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

import socket
from multiprocessing import Process
from pants.web import Application
from pants.http import HTTPServer
from pants.web.fileserver import FileServer
from pants import Engine
from server.routes import module as appRoutes


def _startHttpServer(userAgent, port):
    """
    """
    appRoutes.userAgent = userAgent

    app = Application()
    app.add("/", appRoutes)

    FileServer(r"C:/Users/Niko/Documents/GitHub/ka-BOOM/frontend/static").attach(app, "/static/")

    HTTPServer(app).startSSL(dict(
        do_handshake_on_connect = False,
        server_side = True,
        certfile = r"C:/Users/Niko/Documents/GitHub/ka-BOOM/cert/cert.pem",
    )).listen(("", port))

    Engine.instance().start()


def _getVacantPort():
    """
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    # s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def start(*args):
    """
    """
    port = _getVacantPort()
    args += port,

    global process
    process = Process(target=_startHttpServer, args=args)
    process.start()

    return port


def stop():
    """
    """
    global process
    process.terminate()
