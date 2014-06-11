# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os.path
import time
import json

import requests
from pants.web.application import Module
# from PIL import Image
# from cStringIO import StringIO

from settings import DEBUG
from settings.net import SERVER_HEADERS
from settings.presenter import CEF_REAL_AGENT
from config import PROJECT_PATH, RESOURCES_SCRIPT, RESOURCES_STYLE
from collector import getImageConfiguration
from downloader.images import downloadBackdrop

module = Module()

@module.route('/<path:pathname>', methods=('PATCH',), headers=SERVER_HEADERS, content_type='text/plain')
def presenterReady(request, pathname):
    if DEBUG or pathname == module.frontendToken:
        module.imageBaseUrl, module.imageClosestSize = getImageConfiguration()
        module.interProcessQueue.put('configuration:image-base-url:%s' % module.imageBaseUrl)

        module.interProcessQueue.put('collector:start')
        return '', 203
    else:
        request.finish()
        request.connection.close()


@module.route('/', methods=('GET',), headers=SERVER_HEADERS, content_type='text/html')
def serveRoot(request):
    if module.presented and not DEBUG:
        module.interProcessQueue.put('server:stop')
        request.finish()
        request.connection.close()
    else:
        module.presented = True

        pathname = os.path.join(PROJECT_PATH, "frontend", "app", "index.html")
        with open(pathname, "rb") as fp:
            html = fp.read()

        stylesheetsAmalgamated = "\n".join([open(os.path.join(PROJECT_PATH, "frontend", pathname)).read() for pathname in RESOURCES_STYLE])

        scriptContent = []
        for pathname in RESOURCES_SCRIPT:
            with open(os.path.join(PROJECT_PATH, 'frontend', pathname), 'rU') as fd:
                content = fd.read()
            scriptContent.append(content)
        scriptsAmalgamated = '\n'.join(scriptContent)
        if DEBUG and request.headers.get('User-Agent', None) != module.userAgent:
            scriptsAmalgamated += """
                ; HTTP_PORT = %d; WEBSOCKET_PORT = %d; BOOT_TOKEN = '%s';
            """ % (module.httpPort, module.websocketPort, module.frontendToken)
        # END DEBUG

        html = html.replace('</head>', '<script>%s</script><style>%s</style></head>' % (scriptsAmalgamated, stylesheetsAmalgamated))

        return html, 203


@module.route('/movie/poster/<string(length=32):identifier>.jpg/<int:width>', methods=('GET',), headers=SERVER_HEADERS, content_type='image/jpeg')
def serveMoviePoster(request, movieId, width):
    blob = module.serverStreamManager.getImageBlobByUuid(movieId)
    if blob is None:
        url = '%s%s%s' % (module.imageBaseUrl, module.imageClosestSize, module.serverStreamManager.getMovieByUuid(movieId).urlPoster)
        blob = requests.get(url, headers={'User-agent': CEF_REAL_AGENT}).content
        module.serverStreamManager.saveImageData(movieId, width, blob, False, 'Poster')

    # TODO: send correct cache headers

    return blob, 203


@module.route('/movie/backdrop/<string(length=32):identifier>.jpg', methods=('GET',), headers=SERVER_HEADERS, content_type='image/jpeg')
def serveMoviebackdrop(request, movieUuid):
    blob = module.serverStreamManager.getImageBlobByUuid(movieUuid, 'Backdrop')
    if blob is not None:
        pass
    else:
        blob = downloadBackdrop(module.serverStreamManager, module.imageBaseUrl, movieUuid)

        if blob is None:
            pass
        """
        isBackdropDownloading = module.serverStreamManager.isBackdropDownloading(movieUuid)
        if isBackdropDownloading is False:
            module.serverStreamManager.startBackdropDownload(movieUuid)

            url = '%soriginal%s' % (module.imageBaseUrl, module.serverStreamManager.getMovieByUuid(movieUuid).urlBackdrop)
            blob = requests.get(url, headers={'User-agent': CEF_REAL_AGENT}).content
            module.serverStreamManager.saveImageData(movieUuid, 1920, blob, False, 'Backdrop')

            module.serverStreamManager.endBackdropDownload(movieUuid)
        elif isBackdropDownloading is True:
            while True:
                blob = module.serverStreamManager.getImageBlobByUuid(movieUuid, 'Backdrop')
                if blob is None:
                    time.sleep(0.5)
                else:
                    break
        """

    return blob, 203


@module.route('/<string:identifier>.ttf', methods=('GET',), headers=SERVER_HEADERS, content_type='application/x-font-ttf')
def serveFont(request, identifier):
    pathname = os.path.join(PROJECT_PATH, 'frontend', 'fonts', '%s.ttf' % identifier)
    if os.path.exists(pathname):
        with open(pathname, 'rb') as fd:
            ttf = fd.read()
        return ttf, 203
    else:
        request.finish()
        request.connection.close()


@module.route('/movies/all', methods=('GET',), headers=SERVER_HEADERS, content_type='application/json')
def serveAllMovies(request):
    movies = module.serverStreamManager.getAllMovies()
    return json.dumps(movies, separators=(',',':')), 203


"""
# @module.route('<path:pathname>', methods=('GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'OPTIONS', 'CONNECT'))
@module.route("<regex('([\s\S]+)'):pathname>", methods=('GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'OPTIONS', 'CONNECT'))
def serveAny(request, pathname):
    print 'catch-all URL', pathname
    request.finish()
    request.connection.close()
"""
