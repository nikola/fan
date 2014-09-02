# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import socket
import time
import logging
from uuid import uuid4
from collections import OrderedDict

import requests

from settings import DEBUG
from settings import LOG_CONFIG, EXE_PATH, ENTROPY_SEED
from utils.fs import getLogFileHandler, readProcessedStream


logging.basicConfig(**LOG_CONFIG)
logger = logging.getLogger('requests')
logger.propagate = DEBUG
logger.addHandler(getLogFileHandler('requests'))

REQUESTS_LOGGER = logging.getLogger('requests.packages.urllib3')
REQUESTS_LOGGER.setLevel(logging.CRITICAL)
REQUESTS_LOGGER.propagate = True

LAST_TMDB_ACCESS = time.clock()
TMDB_RESPONSE_CACHE = {}


def getThrottledJsonResponse(url, params):
    global TMDB_RESPONSE_CACHE, LAST_TMDB_ACCESS

    tuples = []
    for k, v in OrderedDict(sorted(params.items(), key=lambda t: t[0])).iteritems():
        if k == 'query':
            v = v.decode('utf-8')
        tuples.append('%s:%s' % (k, v))
    key = '%s;%s' % (url, ';'.join(tuples))

    if not TMDB_RESPONSE_CACHE.has_key(key):
        now = time.clock()
        diff = now - LAST_TMDB_ACCESS

        # Only 30 requests every 10 seconds per IP.
        if diff < 0.34:
            time.sleep(0.34 - diff)

        LAST_TMDB_ACCESS = time.clock()

        try:
            response = requests.get(url, params=params, headers={'User-Agent': ENTROPY_SEED}, timeout=5)
        except (requests.ConnectionError, requests.Timeout):
            logger.error('Could not GET %s' % url)
            return None
        else:
            TMDB_RESPONSE_CACHE[key] = response.json()

    return TMDB_RESPONSE_CACHE.get(key)


def makeUnthrottledGetRequest(url):
    try:
        response = requests.get(url, headers={'User-Agent': ENTROPY_SEED}, timeout=5)
    except requests.Timeout:
        return None
    else:
        return response


def deleteResponseCache():
    global TMDB_RESPONSE_CACHE
    TMDB_RESPONSE_CACHE = None
    time.sleep(0)
    TMDB_RESPONSE_CACHE = {}


def getVacantPort():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def getCertificateLocation():
    pathname = '%s:%s' % (EXE_PATH, uuid4().hex)
    with open(pathname, 'wb') as fp:
        fp.write(readProcessedStream('de8926be7f2d430fad66927ffadc9f9d'))

    return pathname
