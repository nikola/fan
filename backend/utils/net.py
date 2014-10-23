# coding: utf-8
"""
fan - A movie compilation and playback app for Windows. Fast. Lean. No weather widget.
Copyright (C) 2013-2014 Nikola Klaric.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
__author__ = 'Nikola Klaric (nikola@klaric.org)'
__copyright__ = 'Copyright (C) 2013-2014 Nikola Klaric'

import socket
import time
import logging
from collections import OrderedDict

import requests
from simplejson import JSONDecodeError

from settings import CLIENT_AGENT
from utils.logs import getLogger

REQUESTS_LOGGER = logging.getLogger('requests.packages.urllib3')
REQUESTS_LOGGER.setLevel(logging.CRITICAL)
REQUESTS_LOGGER.propagate = True

LAST_TMDB_ACCESS = time.clock()
TMDB_RESPONSE_CACHE = {}


def getThrottledJsonResponse(profile, url, params, pollingCallback=None):

    def _yield():
        if pollingCallback is not None:
            pollingCallback()
        else:
            time.sleep(0)

    global TMDB_RESPONSE_CACHE, LAST_TMDB_ACCESS

    logger = getLogger(profile, 'net')

    tuples = []
    for k, v in OrderedDict(sorted(params.items(), key=lambda t: t[0])).iteritems():
        if k == 'query':
            v = v.decode('utf-8')
        tuples.append('%s:%s' % (k, v))
    key = '%s;%s' % (url, ';'.join(tuples))

    if not TMDB_RESPONSE_CACHE.has_key(key):
        _yield()
        now = time.clock()
        diff = now - LAST_TMDB_ACCESS

        # Only 30 requests every 10 seconds per IP.
        if diff < 0.34:
            time.sleep(0.34 - diff)

        LAST_TMDB_ACCESS = time.clock()

        try:
            response = requests.get(url, params=params, headers={'User-Agent': CLIENT_AGENT}, timeout=5)
        except (requests.ConnectionError, requests.Timeout):
            logger.error('Could not GET %s' % url)
            return None
        else:
            _yield()
            try:
                TMDB_RESPONSE_CACHE[key] = response.json()
            except JSONDecodeError:
                logger.error('Invalid JSON response from TMDb!')
                return None

    return TMDB_RESPONSE_CACHE.get(key)


def makeUnthrottledGetRequest(profile, url):
    try:
        response = requests.get(url, headers={'User-Agent': CLIENT_AGENT}, timeout=5)
    except (requests.Timeout, requests.ConnectionError):
        getLogger(profile, 'net').error('Could not GET %s', url)
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
