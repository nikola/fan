# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os.path
import re
import bz2
import gzip
import datetime
from cStringIO import StringIO

import requests
from pants.web.application import Module
from pants.http.utils import HTTPHeaders

from settings import DEBUG
from settings.net import SERVER_HEADERS
from settings.presenter import CEF_REAL_AGENT
from config import PROJECT_PATH
from identifier import getImageConfiguration
from downloader.images import downloadBackdrop
from utils.rfc import getRfc1123Timestamp

IMG_MIME_TYPES = {
    'JPEG': 'image/jpeg',
    'WebP': 'application/octet-stream',
}

module = Module()

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


@module.route('/boot.asp', methods=('GET',), headers=SERVER_HEADERS, content_type='text/html')
def serveBootloader(request):
    pathname = os.path.join(PROJECT_PATH, 'frontend', 'app', 'html', 'boot.html')
    with open(pathname, 'rb') as fp:
        html = fp.read()

    return html, 200


# @module.route('/gui.asp', methods=('GET',), headers=SERVER_HEADERS, content_type='text/html')
@module.route('/gui.asp', methods=('GET',), content_type='text/html')
def serveGui(request):
    if module.presented and not DEBUG:
        module.interProcessQueue.put('orchestrator:stop:all')
        request.finish()
        request.connection.close()
    else:
        module.presented = True

        filename = os.path.join(PROJECT_PATH, 'frontend', 'app', 'blob', 'gui')
        with open(filename, 'rb') as fp:
            compressed = fp.read()
        html = bz2.decompress(compressed)

        timestamp = datetime.datetime.utcfromtimestamp(os.path.getmtime(filename))

        if DEBUG and request.headers.get('User-Agent', None) != module.userAgent:
            html = html.replace(
                '</script>',
                '; HTTP_PORT = %d; WEBSOCKET_PORT = %d; BOOT_TOKEN = "%s";</script>' % (module.serverPort, module.serverPort, module.bootToken)
            )

        stream = StringIO()
        with gzip.GzipFile(filename='dummy', mode='wb', fileobj=stream) as gzipStream:
            gzipStream.write(html)

        headers = SERVER_HEADERS.copy()
        headers.update({
            'Last-modified': getRfc1123Timestamp(timestamp),
            'Cache-Control': 'max-age=0, must-revalidate',
            'Content-Encoding': 'gzip',
        })

        return stream.getvalue(), 200, HTTPHeaders(data=headers)


@module.route('/movie/poster/<string(length=32):identifier>-<int:width>.image', methods=('GET',), content_type='application/octet-stream')
def serveMoviePoster(request, movieUuid, width):
    image = module.streamManager.getImageByUuid(movieUuid, 'Poster', width)

    if image is None:
        pathPoster = module.streamManager.getMovieByUuid(movieUuid).urlPoster
        urlPoster = '%s%s%s' % (module.imageBaseUrl, module.imageClosestSize, pathPoster)
        blob = requests.get(urlPoster, headers={'User-agent': CEF_REAL_AGENT}).content
        image = module.streamManager.saveImageData(movieUuid, width, blob, False, 'Poster', 'JPEG', '%soriginal%s' % (module.imageBaseUrl, pathPoster))

    if image is not None:
        headers = SERVER_HEADERS.copy()
        headers.update({
            'Last-modified': getRfc1123Timestamp(image.modified),
            'Cache-Control': 'max-age=0, must-revalidate',
        })

        return image.blob, 200, HTTPHeaders(data=headers)
    else:
        request.send_status(404)
        request.finish()
        request.connection.close()


@module.route('/movie/backdrop/<string(length=32):identifier>.jpg', methods=('GET',), content_type='image/jpeg')
def serveMoviebackdrop(request, movieUuid):
    image = module.streamManager.getImageByUuid(movieUuid, 'Backdrop')
    if image is None:
        image = downloadBackdrop(module.streamManager, module.imageBaseUrl, movieUuid)

    if image is not None:
        # headers = SERVER_HEADERS
        # headers.update({'Last-modified': getRfc1123Timestamp(image.modified)})

        return image.blob, 200, HTTPHeaders(data=SERVER_HEADERS)
    else:
        request.send_status(404)
        request.finish()
        request.connection.close()

    # return blob, 200


@module.route('/<string:identifier>.ttf', methods=('GET',), headers=SERVER_HEADERS, content_type='application/x-font-ttf')
def serveFont(request, identifier):
    pathname = os.path.join(PROJECT_PATH, 'frontend', 'fonts', '%s.ttf' % identifier)
    if os.path.exists(pathname):
        with open(pathname, 'rb') as fd:
            ttf = fd.read()
        return ttf, 200
    else:
        request.finish()
        request.connection.close()


@module.route('/<string:identifier>.gif', methods=('GET',), headers=SERVER_HEADERS, content_type='image/gif')
def serveGif(request, identifier):
    pathname = os.path.join(PROJECT_PATH, 'frontend', 'app', 'img', '%s.gif' % identifier)
    if os.path.exists(pathname):
        with open(pathname, 'rb') as fp:
            gif = fp.read()
        return gif, 200
    else:
        request.finish()
        request.connection.close()


@module.route('/movies/all', methods=('GET',), headers=SERVER_HEADERS, content_type='application/json')
def serveAllMovies(request):
    return module.streamManager.getAllMoviesAsJson(), 200


"""
# @module.route('<path:pathname>', methods=('GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'OPTIONS', 'CONNECT'))
@module.route("<regex('([\s\S]+)'):pathname>", methods=('GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'OPTIONS', 'CONNECT'))
def serveAny(request, pathname):
    print 'catch-all URL', pathname
    request.finish()
    request.connection.close()
"""
