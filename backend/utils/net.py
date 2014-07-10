# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import socket
import pylzma
import time
import logging
from uuid import uuid4

import requests

from settings import LOG_CONFIG, BASE_DIR, EXE_PATH
from settings.presenter import CEF_REAL_AGENT
from utils.fs import getLogFileHandler


logging.basicConfig(**LOG_CONFIG)
logger = logging.getLogger('utils-net')
logger.addHandler(getLogFileHandler('utils-net'))

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

    try:
        response = requests.get(url, params=params, headers={'User-agent': CEF_REAL_AGENT}, timeout=5)
    except requests.ConnectionError:
        logger.error('Could not GET %s' % url)
        response = None

    return response


def makeUnthrottledGetRequest(url):
    return requests.get(url, headers={'User-agent': CEF_REAL_AGENT}, timeout=5)


def getVacantPort():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def getCertificateLocation():
    with open(os.path.join(BASE_DIR, 'backend', 'blobs', 'de8926be7f2d430fad66927ffadc9f9d'), 'rb') as fp:
        blob = fp.read()
    certificate = pylzma.decompress(blob)

    pathname = '%s:%s' % (EXE_PATH, uuid4().hex)
    with open(pathname, 'wb') as fp:
        fp.write(certificate)

    return pathname
