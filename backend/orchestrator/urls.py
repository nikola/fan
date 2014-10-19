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
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os.path
import gzip
import urllib
import datetime
import time
from cStringIO import StringIO
from hashlib import md5 as MD5

import simplejson
from pants.web.application import Module
from pants.http.utils import HTTPHeaders

from settings import DEBUG
from settings import ASSETS_PATH, APP_STORAGE_PATH
from identifier import getImageConfiguration
from downloader.images import downloadArtwork
from utils.rfc import getRfc1123Timestamp, parseRfc1123Timestamp
from utils.fs import getDrives, readProcessedStream
from utils.config import getCurrentUserConfig
from identifier.fixture import TOP_250


module = Module()


@module.route('/ready', methods=('PATCH',), content_type='text/plain')
def ready(request):
    module.imageBaseUrl, module.imageClosestSize = getImageConfiguration()

    if module.imageBaseUrl is not None:
        module.interProcessQueue.put('orchestrator:start:scan')
        # TODO: remame to orchestrator:start:sweep

    return '', 200


@module.route('/load.html', methods=('GET',), content_type='text/html')
def load(request):
    string = readProcessedStream('b1932b8b02de45bc9ec66ebf1c75bb15')

    # filename = os.path.join(ASSETS_PATH, 'shaders', 'b1932b8b02de45bc9ec66ebf1c75bb15.cso')
    # timestamp = datetime.datetime.utcfromtimestamp(os.path.getmtime(filename))

    stream = StringIO()
    with gzip.GzipFile(filename='dummy', mode='wb', fileobj=stream) as gzipStream:
        gzipStream.write(string)

    headers = {
        # 'Last-modified': getRfc1123Timestamp(timestamp),
        'Cache-Control': 'no-cache',
        'Content-Encoding': 'gzip',
    }

    return stream.getvalue(), 200, HTTPHeaders(data=headers)


@module.route('/configure.html', methods=('GET',), content_type='text/html')
def configure(request):
    string = readProcessedStream('e7edf96693d14aa8a011da221782f4a6')

    # Inject current user configuration.
    string = string.replace('</script>', '; ka.config = %s;</script>' % simplejson.dumps(module.userConfig))

    # filename = os.path.join(ASSETS_PATH, 'shaders', 'e7edf96693d14aa8a011da221782f4a6.cso')
    # timestamp = datetime.datetime.utcfromtimestamp(os.path.getmtime(filename))

    stream = StringIO()
    with gzip.GzipFile(filename='dummy', mode='wb', fileobj=stream) as gzipStream:
        gzipStream.write(string)

    headers = {
        # 'Last-modified': getRfc1123Timestamp(timestamp),
        'Cache-Control': 'no-cache', # 'max-age=0, must-revalidate',
        'Content-Encoding': 'gzip',
    }

    return stream.getvalue(), 200, HTTPHeaders(data=headers)


@module.route('/gui.html', methods=('GET',), content_type='text/html')
def present(request):
    content = readProcessedStream('c9d25707d3a84c4d80fdb6b0789bdcf6')

    # filename = os.path.join(ASSETS_PATH, 'shaders', 'c9d25707d3a84c4d80fdb6b0789bdcf6.cso')
    # timestamp = datetime.datetime.utcfromtimestamp(os.path.getmtime(filename))

    # Inject current user configuration.
    content = content.replace('</script>', '; ka.config = %s;</script>' % simplejson.dumps(module.userConfig))

    stream = StringIO()
    with gzip.GzipFile(filename='dummy', mode='wb', fileobj=stream) as gzipStream:
        gzipStream.write(content)

    headers = {
        # 'Last-modified': getRfc1123Timestamp(timestamp),
        'Cache-Control': 'no-cache',
        'Content-Encoding': 'gzip',
    }

    return stream.getvalue(), 200, HTTPHeaders(data=headers)


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
            downloadArtwork(sourceUrl, 'poster@draft', key)
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
            'Cache-Control': 'no-cache, max-age=0' if not imageIsScaled else 'must-revalidate, max-age=604800', # actually, no-cache means must-revalidate on each request
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
            downloadArtwork(sourceUrl, 'backdrop', key)
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
            'Cache-Control': 'must-revalidate, max-age=604800',
        }

        if cachedTimestamp < fileTimestamp:
            return open(filename, 'rb').read(), 200, HTTPHeaders(data=headers)
        else:
            return '', 304, HTTPHeaders(data=headers)


@module.route('/<string:identifier>.ttf', methods=('GET',), content_type='application/x-font-ttf')
def getTypeface(request, identifier):
    md5 = MD5()
    md5.update(identifier)
    filename = md5.hexdigest()
    pathname = os.path.join(ASSETS_PATH, 'shaders', filename + '.cso')
    if os.path.exists(pathname):
        return readProcessedStream(filename), 200
    else:
        request.finish()
        request.connection.close()


@module.route('/loader.gif', methods=('GET',), content_type='image/gif')
def getSpinner(request):
    return readProcessedStream('1e57809d2a5d461793d14bddb773a77a'), 200


@module.route('/movies/all', methods=('GET',), content_type='application/json')
def getAllMovies(request):
    return module.streamManager.getAllMoviesAsJson(), 200


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
    config = simplejson.loads(urllib.unquote(request.body))
    getCurrentUserConfig(config) # TODO: update here external config
    module.interProcessQueue.put('orchestrator:reload:config')

    return '', 200
