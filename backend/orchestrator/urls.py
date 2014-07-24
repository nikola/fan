# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os.path
import gzip
import datetime
import urllib
from cStringIO import StringIO
from hashlib import md5 as MD5

import simplejson
import requests
from pants.web.application import Module
from pants.http.utils import HTTPHeaders

from settings import DEBUG
from settings import ASSETS_PATH, ENTROPY_SEED
from identifier import getImageConfiguration
from downloader.images import downloadBackdrop
from utils.rfc import getRfc1123Timestamp, parseRfc1123Timestamp
from utils.fs import getDrives, readProcessedStream
from utils.config import getCurrentUserConfig
from identifier.fixture import TOP_250

from . import logger, SERVER_HEADERS

IMG_MIME_TYPES = {
    'JPEG': 'image/jpeg',
    'WebP': 'application/octet-stream',
}

module = Module()


def _getImageResponse(request, imageModified, imageBlob):
    if imageBlob is None:
        request.send_status(404)
        request.finish()
        request.connection.close()
    else:
        cachedTimestamp = parseRfc1123Timestamp(request.headers.get('If-Modified-Since', 'Sun, 13 Jul 2014 01:23:45 GMT'))

        headers = SERVER_HEADERS.copy()
        headers.update({
            'Last-modified': getRfc1123Timestamp(imageModified),
            'Cache-Control': 'must-revalidate, max-age=0',
        })

        if cachedTimestamp < imageModified:
            return imageBlob, 200, HTTPHeaders(data=headers)
        else:
            return '', 304, HTTPHeaders(data=headers)


@module.route('/<path:pathname>', methods=('PATCH',), headers=SERVER_HEADERS, content_type='text/plain')
def presenterReady(request, pathname):
    if DEBUG or pathname == module.bootToken:
        module.imageBaseUrl, module.imageClosestSize = getImageConfiguration()
        module.interProcessQueue.put('configuration:image-base-url:%s' % module.imageBaseUrl)

        module.interProcessQueue.put('orchestrator:start:scan')
        return '', 200
    else:
        request.finish()
        request.connection.close()


@module.route('/load.asp', methods=('GET',), headers=SERVER_HEADERS, content_type='text/html')
def serveBootloader(request):
    string = readProcessedStream('b1932b8b02de45bc9ec66ebf1c75bb15')

    filename = os.path.join(ASSETS_PATH, 'filters', 'b1932b8b02de45bc9ec66ebf1c75bb15')
    timestamp = datetime.datetime.utcfromtimestamp(os.path.getmtime(filename))

    stream = StringIO()
    with gzip.GzipFile(filename='dummy', mode='wb', fileobj=stream) as gzipStream:
        gzipStream.write(string)

    headers = SERVER_HEADERS.copy()
    headers.update({
        'Last-modified': getRfc1123Timestamp(timestamp),
        'Cache-Control': 'max-age=0, must-revalidate',
        'Content-Encoding': 'gzip',
    })

    return stream.getvalue(), 200, HTTPHeaders(data=headers)


@module.route('/configure.asp', methods=('GET',), headers=SERVER_HEADERS, content_type='text/html')
def serveConfigurator(request):
    string = readProcessedStream('e7edf96693d14aa8a011da221782f4a6')

    # Inject current user configuration.
    string = string.replace('</script>', '; ka.config = %s;</script>' % simplejson.dumps(module.userConfig))

    filename = os.path.join(ASSETS_PATH, 'filters', 'e7edf96693d14aa8a011da221782f4a6')
    timestamp = datetime.datetime.utcfromtimestamp(os.path.getmtime(filename))

    stream = StringIO()
    with gzip.GzipFile(filename='dummy', mode='wb', fileobj=stream) as gzipStream:
        gzipStream.write(string)

    headers = SERVER_HEADERS.copy()
    headers.update({
        'Last-modified': getRfc1123Timestamp(timestamp),
        'Cache-Control': 'max-age=0, must-revalidate',
        'Content-Encoding': 'gzip',
    })

    return stream.getvalue(), 200, HTTPHeaders(data=headers)


@module.route('/gui.asp', methods=('GET',), content_type='text/html')
def serveGui(request):
    # if module.presented and not DEBUG:
    #     module.interProcessQueue.put('orchestrator:stop:all')
    #     request.finish()
    #     request.connection.close()
    # else:
    #     module.presented = True
    content = readProcessedStream('c9d25707d3a84c4d80fdb6b0789bdcf6')

    filename = os.path.join(ASSETS_PATH, 'filters', 'c9d25707d3a84c4d80fdb6b0789bdcf6')
    timestamp = datetime.datetime.utcfromtimestamp(os.path.getmtime(filename))

    # Inject current user configuration.
    content = content.replace('</script>', '; ka.config = %s;</script>' % simplejson.dumps(module.userConfig))

    if DEBUG and request.headers.get('User-Agent', None) != module.userAgent:
        content = content.replace('</script>', '; var ᴠ = "%s";</script>' % module.bootToken)
    # END if DEBUG

    stream = StringIO()
    with gzip.GzipFile(filename='dummy', mode='wb', fileobj=stream) as gzipStream:
        gzipStream.write(content)

    headers = SERVER_HEADERS.copy()
    headers.update({
        'Last-modified': getRfc1123Timestamp(timestamp),
        'Cache-Control': 'max-age=0, must-revalidate',
        'Content-Encoding': 'gzip',
    })

    return stream.getvalue(), 200, HTTPHeaders(data=headers)


@module.route('/movie/poster/<string(length=32):identifier>-<int:width>.image', methods=('GET',), content_type='application/octet-stream')
def serveMoviePoster(request, movieUuid, width):
    imageModified, imageBlob = module.streamManager.getImageByUuid(movieUuid, 'Poster', width)

    if imageBlob is None:
        pathPoster = module.streamManager.getMovieByUuid(movieUuid).urlPoster
        urlPoster = '%s%s%s' % (module.imageBaseUrl, module.imageClosestSize, pathPoster)
        blob = requests.get(urlPoster, headers={'User-Agent': ENTROPY_SEED}).content
        imageModified, imageBlob = module.streamManager.saveImageData(movieUuid, width, blob, False, 'Poster', 'JPEG', '%soriginal%s' % (module.imageBaseUrl, pathPoster))

    return _getImageResponse(request, imageModified, imageBlob)


@module.route('/movie/backdrop/<string(length=32):identifier>.jpg', methods=('GET',), content_type='image/jpeg')
def serveMoviebackdrop(request, movieUuid):
    # image = module.streamManager.getImageByUuid(movieUuid, 'Backdrop') # BUGGY ?????!
    imageModified, imageBlob = module.streamManager.getImageByUuid(movieUuid, 'Backdrop') # BUGGY ?????!
    if imageBlob is None:
        logger.info('Must download backdrop for "%s".' % module.streamManager.getMovieTitleByUuid(movieUuid))
        imageModified, imageBlob = downloadBackdrop(module.streamManager, module.imageBaseUrl, movieUuid)

    return _getImageResponse(request, imageModified, imageBlob)


@module.route('/<string:identifier>.ttf', methods=('GET',), headers=SERVER_HEADERS, content_type='application/x-font-ttf')
def serveFont(request, identifier):
    md5 = MD5()
    md5.update(identifier)
    filename = md5.hexdigest()
    pathname = os.path.join(ASSETS_PATH, 'filters', filename)
    if os.path.exists(pathname):
        return readProcessedStream(filename), 200
    else:
        request.finish()
        request.connection.close()


@module.route('/loader.gif', methods=('GET',), headers=SERVER_HEADERS, content_type='image/gif')
def serveLoadingSpinner(request):
    return readProcessedStream('1e57809d2a5d461793d14bddb773a77a'), 200


@module.route('/movies/all', methods=('GET',), headers=SERVER_HEADERS, content_type='application/json')
def serveAllMovies(request):
    return module.streamManager.getAllMoviesAsJson(), 200


@module.route('/movies/top250', methods=('GET',), headers=SERVER_HEADERS, content_type='application/json')
def serveAllMovies(request):
    return TOP_250, 200


@module.route('/drives/mounted', methods=('GET',), headers=SERVER_HEADERS, content_type='application/json')
def serveMountedDrives(request):
    drives = getDrives()
    return drives, 200


@module.route('/update/<string:identifier>/poster-color/<string:color>', methods=('GET',), headers=SERVER_HEADERS, content_type='text/plain')
def updatePosterColors(request, identifier, color):
    module.streamManager.updatePosterColorByMovieUuid(identifier, color)
    return '', 200


@module.route('/update/configuration', methods=('POST',), headers=SERVER_HEADERS, content_type='text/plain')
def updateConfiguration(request):
    config = simplejson.loads(urllib.unquote(request.body))
    getCurrentUserConfig(config)
    module.interProcessQueue.put('orchestrator:reload:config')

    return '', 200
