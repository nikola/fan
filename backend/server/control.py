# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import socket
import bz2
import base64
from uuid import uuid4
import win32file
from multiprocessing import Process
from os import fdopen
from tempfile import mkstemp

from pants.web import Application
from pants.http import HTTPServer # , WebSocket
from pants import Engine

from utils.win32 import isNtfsFilesystem
from config import DEBUG, ENFORCED_CIPHERS, CERTIFICATE, PROJECT_PATH
from server.routes import module as appRoutes

"""
class EchoSocket(WebSocket):
    def on_read(self, data):
        self.write(data)
"""

def _startHttpServer(queue, userAgent, port, certificateFile):

    def _verifyUserAgent(request):
        if DEBUG or (request.is_secure and request.protocol == 'HTTP/1.1' and request.headers.get('Accept-Language', None) == 'en-us,en' and request.headers.get('User-Agent', None) == userAgent):
            # if request.path.endswith('.socket'):
            #     EchoSocket(request)
            # else:
            app(request)
        else:
            request.finish()
            request.connection.close()

    appRoutes.interProcessQueue = queue

    app = Application(debug=DEBUG)
    app.add('/', appRoutes)

    sslOptions = dict(do_handshake_on_connect=False, server_side=True, certfile=certificateFile, ssl_version=3, ciphers=ENFORCED_CIPHERS)
    HTTPServer(_verifyUserAgent).startSSL(sslOptions).listen(('', port))
    Engine.instance().start()
    # TODO: needs to stop?


def _getVacantPort():
    s = socket.socket()
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _getCertificateLocation():
    certificate = bz2.decompress(base64.decodestring(CERTIFICATE))

    if isNtfsFilesystem():
        executable = os.path.join(PROJECT_PATH, 'backend', 'boot.py')
        pathname = '%s:%s' % (executable, uuid4().hex)
        # if win32file.GetFileAttributesW(unicode(executable)) & 1:
        #     win32file.SetFileAttributesW(unicode(executable), 0)
        with open(pathname, 'wb') as fp:
            fp.write(certificate)
        # win32file.SetFileAttributesW(unicode(executable), 1) # FILE_ATTRIBUTE_READONLY
    else:
        fd, pathname = mkstemp(suffix='.tmp', prefix='ASPNETSetup_')
        if not DEBUG:
            # FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM | FILE_ATTRIBUTE_TEMPORARY | FILE_ATTRIBUTE_NOT_CONTENT_INDEXED
            win32file.SetFileAttributesW(unicode(pathname), 2 | 4 | 256 | 8192)

        fp = fdopen(fd, 'w')
        fp.write(certificate)
        fp.close()

    return pathname


def start(*args):
    port = _getVacantPort()
    args += port,

    global globalCertificateLocation
    globalCertificateLocation = _getCertificateLocation()
    args += globalCertificateLocation,

    process = Process(target=_startHttpServer, args=args)
    process.start()

    return process, port


def stop():
    global globalCertificateLocation
    os.remove(globalCertificateLocation)
