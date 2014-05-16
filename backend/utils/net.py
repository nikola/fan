# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import socket
import bz2
import base64
import win32file
from os import fdopen
from uuid import uuid4
from tempfile import mkstemp

from config import DEBUG, CERTIFICATE, PROJECT_PATH
from utils.win32 import isNtfsFilesystem


def getVacantPort():
    s = socket.socket()
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def getCertificateLocation():
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
