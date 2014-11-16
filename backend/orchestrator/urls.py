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

import os.path
import urllib
import datetime
import time

import simplejson as json
from pants.web.application import Module, abort
from pants.http.utils import HTTPHeaders

from settings import APP_STORAGE_PATH, STATIC_PATH
from identifier import getImageConfiguration
from downloader.images import downloadArtwork
from utils.rfc import getRfc1123Timestamp, parseRfc1123Timestamp
from utils.fs import getDrives
from utils.config import processCurrentUserConfig
from identifier.fixture import TOP_250


module = Module()


@module.route('/ready', methods=('PATCH',), content_type='text/plain')
def ready(request):
    module.imageBaseUrl, module.imageClosestSize = getImageConfiguration(module.profile, 300)

    if module.imageBaseUrl is not None:
        module.interProcessQueue.put('orchestrator:start:scan')
        # TODO: remame to orchestrator:start:sweep

    return '', 200


@module.route('/<string:screen>.html', methods=('GET',), content_type='text/html')
def present(request, screen):
    if screen in ('load', 'configure', 'gui'):
        with open(os.path.join(STATIC_PATH, 'html', '%s.html' % screen)) as fp:
            content = fp.read()
        if screen in ('configure', 'gui'):
            content = content.replace('</head>', '<script>var ka = ka || {}; ka.config = %s;</script></head>'
                % json.dumps(module.userConfig))

        return content, 200, HTTPHeaders(data={'Cache-Control': 'no-cache,max-age=0'})
    else:
        abort()


@module.route('/movie/poster/<string:key>-<int:width>.image', methods=('GET',), content_type='application/octet-stream')
def getScaledPosterByKey(request, key, width):
    pathname = os.path.join(APP_STORAGE_PATH, 'artwork', 'posters', key)
    filename = os.path.join(pathname, 'poster')

    imageIsScaled = os.path.exists(filename + '@%d.webp' % width)
    time.sleep(0)

    if imageIsScaled:
        filename += '@%d.webp' % width
    else:
        if not os.path.exists(filename + '@draft.jpg'):
            time.sleep(0)
            link = open(os.path.join(pathname, 'source.url'), 'rU').read()
            time.sleep(0)
            sourceUrl = link[link.find('=') + 1:].replace('original', module.imageClosestSize).strip()
            downloadArtwork(module.profile, sourceUrl, 'poster@draft', key)
            time.sleep(0)

        filename += '@draft.jpg'

    if not os.path.exists(filename):
        request.send_status(404)
        request.finish()
        request.connection.close()
    else:
        time.sleep(0)
        fileTimestamp = datetime.datetime.utcfromtimestamp(os.path.getmtime(filename))
        time.sleep(0)
        cachedTimestamp = parseRfc1123Timestamp(request.headers.get('If-Modified-Since', 'Sun, 13 Jul 2014 01:23:45 GMT'))

        headers = {
            'Last-modified': getRfc1123Timestamp(fileTimestamp),
            'Cache-Control': 'no-cache,max-age=0' if not imageIsScaled else 'must-revalidate,max-age=604800',
        }

        if cachedTimestamp < fileTimestamp:
            return open(filename, 'rb').read(), 200, HTTPHeaders(data=headers)
        else:
            return '', 304, HTTPHeaders(data=headers)


@module.route('/movie/backdrop/<string:key>.jpg', methods=('GET',), content_type='image/jpeg')
def getBackdropByKey(request, key):
    pathname = os.path.join(APP_STORAGE_PATH, 'artwork', 'backdrops', key)
    filename = os.path.join(pathname, 'backdrop.jpg')

    if not os.path.exists(filename):
        time.sleep(0)
        if os.path.exists(filename.replace('.jpg', '.incomplete')):
            time.sleep(0)
            while os.path.exists(filename.replace('.jpg', '.incomplete')):
                time.sleep(0.25)
        else:
            time.sleep(0)
            os.remove(os.path.join(APP_STORAGE_PATH, 'backlog', 'backdrops', key))
            time.sleep(0)
            link = open(os.path.join(pathname, 'source.url'), 'rU').read()
            time.sleep(0)
            sourceUrl = link[link.find('=') + 1:].strip()
            downloadArtwork(module.profile, sourceUrl, 'backdrop', key)
            time.sleep(0)

    if not os.path.exists(filename):
        request.send_status(404)
        request.finish()
        request.connection.close()
    else:
        fileTimestamp = datetime.datetime.utcfromtimestamp(os.path.getmtime(filename))
        time.sleep(0)
        cachedTimestamp = parseRfc1123Timestamp(request.headers.get('If-Modified-Since', 'Sun, 13 Jul 2014 01:23:45 GMT'))

        headers = {
            'Last-modified': getRfc1123Timestamp(fileTimestamp),
            'Cache-Control': 'must-revalidate,max-age=604800',
        }

        if cachedTimestamp < fileTimestamp:
            return open(filename, 'rb').read(), 200, HTTPHeaders(data=headers)
        else:
            return '', 304, HTTPHeaders(data=headers)


@module.route('/movies/all', methods=('GET',), content_type='application/json')
def getAllMovies(request):
    return module.streamManager.getAllMoviesAsJson(module.userConfig.get('language'), module.userConfig.get('country')), 200


@module.route('/movies/top250', methods=('GET',), content_type='application/json')
def getTop250(request):
    return TOP_250, 200


@module.route('/drives/mounted', methods=('GET',), content_type='application/json')
def getMountedDrives(request):
    return getDrives(), 200


@module.route('/update/<int:identifier>/poster-color/<string:color>', methods=('GET',), content_type='text/plain')
def updatePrimaryPosterColor(request, identifier, color):
    module.streamManager.updatePosterColorByMovieId(identifier, color)
    return '', 200


@module.route('/movie/<int:identifier>/set-backdrop-cached', methods=('GET',), content_type='text/plain')
def setBackdropAsCached(request, identifier):
    module.streamManager.setBackdropCachedByMovieId(identifier)
    return '', 200


@module.route('/movie/<int:identifier>/get-available-versions', methods=('GET',), content_type='application/json')
def getAvailableVersions(request, identifier):
    return module.streamManager.getVersionsByMovieId(identifier), 200


@module.route('/update/configuration', methods=('POST',), content_type='text/plain')
def updateConfiguration(request):
    module.userConfig = processCurrentUserConfig(module.profile, json.loads(urllib.unquote(request.body)))
    module.interProcessQueue.put('orchestrator:reload:config')

    return '', 200
