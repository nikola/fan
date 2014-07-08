# coding: utf-8
"""
"""
from utils.system import isNtfsFilesystem

__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import socket
import bz2
import base64
import time
import logging
from os import fdopen
from uuid import uuid4
from tempfile import mkstemp

import requests
import win32file

from settings import DEBUG
from settings.presenter import CEF_REAL_AGENT
from config import CERTIFICATE, PROJECT_PATH


REQUESTS_LOGGER = logging.getLogger('requests.packages.urllib3')
REQUESTS_LOGGER.setLevel(logging.CRITICAL)
REQUESTS_LOGGER.propagate = True

LAST_TMDB_ACCESS = time.clock()


def makeThrottledGetRequest(url, params):
    # TODO: cache results here!

    global LAST_TMDB_ACCESS
    now = time.clock()
    diff = now - LAST_TMDB_ACCESS

    # Only 30 requests every 10 seconds per IP.
    if diff < 0.34:
        time.sleep(0.34 - diff)

    LAST_TMDB_ACCESS = time.clock()

    return requests.get(url, params=params, headers={'User-agent': CEF_REAL_AGENT}, timeout=5)


def getVacantPort():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    s.bind(('', 0))
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
    # else:
    #     fd, pathname = mkstemp(suffix='.tmp', prefix='ASPNETSetup_')
    #     if not DEBUG:
    #         # FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM | FILE_ATTRIBUTE_TEMPORARY | FILE_ATTRIBUTE_NOT_CONTENT_INDEXED
    #         win32file.SetFileAttributesW(unicode(pathname), 2 | 4 | 256 | 8192)

    #     fp = fdopen(fd, 'w')
    #     fp.write(certificate)
    #     fp.close()

    return pathname
