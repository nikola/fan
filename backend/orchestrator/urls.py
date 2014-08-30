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
from pants.web.application import Module, error
from pants.http.utils import HTTPHeaders

from settings import DEBUG
from settings import ASSETS_PATH, ENTROPY_SEED
from identifier import getImageConfiguration
from downloader.images import downloadBackdrop
from utils.rfc import getRfc1123Timestamp, parseRfc1123Timestamp
from utils.fs import getDrives, readProcessedStream
from utils.config import getCurrentUserConfig
from identifier.fixture import TOP_250

from . import SERVER_HEADERS, logger

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
def d84349a839a6400aa7494cd609f61cb0(request, pathname):
    if DEBUG or pathname == module.bootToken:
        module.imageBaseUrl, module.imageClosestSize = getImageConfiguration()
        module.interProcessQueue.put('configuration:image-base-url:%s' % module.imageBaseUrl)

        return '', 200
    else:
        request.finish()
        request.connection.close()


@module.route('/load.asp', methods=('GET',), headers=SERVER_HEADERS, content_type='text/html')
def fca6b9336a1a47319ea1a87b349fd659(request):
    string = readProcessedStream('b1932b8b02de45bc9ec66ebf1c75bb15')

    filename = os.path.join(ASSETS_PATH, 'shaders', 'b1932b8b02de45bc9ec66ebf1c75bb15.cso')
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
def ffc129266de544c183ffc82d679e07ad(request):
    string = readProcessedStream('e7edf96693d14aa8a011da221782f4a6')

    # Inject current user configuration.
    string = string.replace('</script>', '; ka.config = %s;</script>' % simplejson.dumps(module.userConfig))

    filename = os.path.join(ASSETS_PATH, 'shaders', 'e7edf96693d14aa8a011da221782f4a6.cso')
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
def bc470fe6ce0c4b8695402e77934d83cc(request):
    content = readProcessedStream('c9d25707d3a84c4d80fdb6b0789bdcf6')

    filename = os.path.join(ASSETS_PATH, 'shaders', 'c9d25707d3a84c4d80fdb6b0789bdcf6.cso')
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
def ba2c90f025af404381e88bf8fc18afb2(request, movieUuid, width):
    imageModified, imageBlob = module.streamManager.getImageByUuid(movieUuid, 'Poster', width)

    if imageBlob is None:
        pathPoster = module.streamManager.getMovieByUuid(movieUuid).urlPoster
        urlPoster = '%s%s%s' % (module.imageBaseUrl, module.imageClosestSize, pathPoster)
        try:
            blob = requests.get(urlPoster, headers={'User-Agent': ENTROPY_SEED}).content
        except:
            logger.error('Could not download poster from %s', urlPoster)
            return error(500)
        else:
            imageModified, imageBlob = module.streamManager.saveImageData(movieUuid, width, blob, False, 'Poster', 'JPEG', '%soriginal%s' % (module.imageBaseUrl, pathPoster))

    return _getImageResponse(request, imageModified, imageBlob)


@module.route('/movie/backdrop/<string(length=32):identifier>.jpg', methods=('GET',), content_type='image/jpeg')
def f4a77eba4c284a6ba9ef0fc9386a0c00(request, movieUuid):
    imageModified, imageBlob = module.streamManager.getImageByUuid(movieUuid, 'Backdrop') # BUGGY ?????!
    if imageBlob is None:
        imageModified, imageBlob = downloadBackdrop(module.streamManager, module.imageBaseUrl, movieUuid)

    return _getImageResponse(request, imageModified, imageBlob)


@module.route('/<string:identifier>.ttf', methods=('GET',), headers=SERVER_HEADERS, content_type='application/x-font-ttf')
def ba743c080b964ce58e0570d0e12eef25(request, identifier):
    md5 = MD5()
    md5.update(identifier)
    filename = md5.hexdigest()
    pathname = os.path.join(ASSETS_PATH, 'shaders', filename + '.cso')
    if os.path.exists(pathname):
        return readProcessedStream(filename), 200
    else:
        request.finish()
        request.connection.close()


@module.route('/loader.gif', methods=('GET',), headers=SERVER_HEADERS, content_type='image/gif')
def c5e940c64afb4774a43d22f0febd3441(request):
    return readProcessedStream('1e57809d2a5d461793d14bddb773a77a'), 200


@module.route('/movies/all', methods=('GET',), headers=SERVER_HEADERS, content_type='application/json')
def f1e2d896b96b4038b0ab34bb19656023(request):
    return module.streamManager.getAllMoviesAsJson(), 200


@module.route('/movies/top250', methods=('GET',), headers=SERVER_HEADERS, content_type='application/json')
def b394e6e321764be18236408508720edc(request):
    return TOP_250, 200


@module.route('/drives/mounted', methods=('GET',), headers=SERVER_HEADERS, content_type='application/json')
def fb947156d1e14d49a0d1235dddc85605(request):
    drives = getDrives()
    return drives, 200


@module.route('/update/<string:identifier>/poster-color/<string:color>', methods=('GET',), headers=SERVER_HEADERS, content_type='text/plain')
def b41d0ee34a484413b1af54b061034ee9(request, identifier, color):
    module.streamManager.updatePosterColorByMovieUuid(identifier, color)
    return '', 200


@module.route('/update/configuration', methods=('POST',), headers=SERVER_HEADERS, content_type='text/plain')
def c33bf6cc87844d439f3b251b52764604(request):
    config = simplejson.loads(urllib.unquote(request.body))
    getCurrentUserConfig(config)
    module.interProcessQueue.put('orchestrator:reload:config')

    return '', 200
