# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os.path
import json

import requests
import tmdb3 as themoviedb
from pants.web.application import Module
# from PIL import Image
# from cStringIO import StringIO

from settings import DEBUG
from settings.net import SERVER_HEADERS
from settings.presenter import CEF_REAL_AGENT
from settings.collector import THEMOVIEDB_API_KEY
from config import PROJECT_PATH, RESOURCES_SCRIPT, RESOURCES_STYLE

module = Module()

@module.route('/<path:pathname>', methods=('PATCH',), headers=SERVER_HEADERS, content_type='text/plain')
def presenterReady(request, pathname):
    if DEBUG or pathname == module.frontendToken:
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


"""
@module.route('<string:filename>.png', methods=('GET',), headers=SERVER_HEADERS, content_type='image/png')
def serveImage(request, filename):
    pathname = os.path.join(PROJECT_PATH, 'frontend', 'app', 'img', '%s.png' % filename)
    if os.path.exists(pathname):
        with open(pathname, 'rb') as fp: content = fp.read()
        return content, 203
    else:
        request.finish()
        request.connection.close()
"""


# @module.route("/movie/poster/<regex('([a-z0-9]{32})'):identifier>.jpg/<int:width>", methods=('GET',), headers=SERVER_HEADERS, content_type='image/jpeg')
@module.route("/movie/poster/<string(length=32):identifier>.jpg/<int:width>", methods=('GET',), headers=SERVER_HEADERS, content_type='image/jpeg')
def serveMoviePoster(request, identifier, width):
    themoviedb.set_key(THEMOVIEDB_API_KEY)
    themoviedb.set_cache('null')

    blob = module.serverStreamManager.getImageBlobById(identifier)
    if blob is None:
        movie = themoviedb.Movie(module.serverStreamManager.getMovieByUuid(identifier).idTheMovieDb)
        poster = movie.poster
        sizes = poster.sizes()
        if 'original' in sizes: sizes.remove('original')

        size = min(sizes, key=lambda x: abs(int(x[1:]) - width))
        if int(size[1:]) < width:
            size = sizes[sizes.index(size) + 1]
        blob = requests.get(poster.geturl(size), headers={'User-agent': CEF_REAL_AGENT}).content
        module.serverStreamManager.saveImageData(identifier, size[1:], blob)

    # image = Image.open(StringIO(blob))
    # image.thumbnail(200, Image.ANTIALIAS) -> maximum height of 200px
    # blob = StringIO()
    # image.save(blob, 'JPEG')

    return blob, 203

"""

"""


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
