# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

import os
import socket
import bz2
import base64
import ctypes
from multiprocessing import Process
from os import fdopen
from tempfile import mkstemp

from pants.web import Application
from pants.http import HTTPServer
from pants import Engine

from config import DEBUG, ENFORCED_CIPHERS, CERTIFICATE
from server.routes import module as appRoutes


def _startHttpServer(userAgent, port, certificateFile):
    """
    """
    def _verifyUserAgent(request):
        if DEBUG or (request.is_secure and request.protocol == 'HTTP/1.1' and request.headers.get('Accept-Language', None) == 'en-us,en' and request.headers.get('User-Agent', None) == userAgent):
            app(request)
        else:
            request.finish()
            request.connection.close()

    app = Application(debug=True)
    app.add("/", appRoutes)

    sslOptions = dict(do_handshake_on_connect=False, server_side=True, certfile=certificateFile, ssl_version=3, ciphers=ENFORCED_CIPHERS)
    HTTPServer(_verifyUserAgent).startSSL(sslOptions).listen(('', port))
    Engine.instance().start()


def _getVacantPort():
    """
    """
    s = socket.socket()
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _getCertificateLocation():
    """
    """
    certificate = bz2.decompress(base64.decodestring(CERTIFICATE))

    fd, pathname = mkstemp(suffix=".tmp", prefix="ASPNETSetup_")
    if not DEBUG:
        # FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM | FILE_ATTRIBUTE_TEMPORARY | FILE_ATTRIBUTE_NOT_CONTENT_INDEXED
        ctypes.windll.kernel32.SetFileAttributesW(unicode(pathname), 2 | 4 | 256 | 8192)

    fp = fdopen(fd, "w")
    fp.write(certificate)
    fp.close()

    return pathname


def start(*args):
    """
    """
    global globalProcess, globalCertificateLocation

    port = _getVacantPort()
    args += port,

    globalCertificateLocation = _getCertificateLocation()
    args += globalCertificateLocation,

    globalProcess = Process(target=_startHttpServer, args=args)
    globalProcess.start()

    return port


def stop():
    """
    """
    global globalProcess, globalCertificateLocation

    os.remove(globalCertificateLocation)
    globalProcess.terminate()
