# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os.path

import requests
import tmdb3 as themoviedb
from pants.web.application import Module
from PIL import Image
from cStringIO import StringIO

from settings import DEBUG
from settings.net import SERVER_HEADERS
from settings.presenter import CEF_REAL_AGENT
from settings.collector import THEMOVIEDB_API_KEY
from config import PROJECT_PATH, RESOURCES_SCRIPT, RESOURCES_STYLE

module = Module()

@module.route('ready', methods=('PATCH',), headers=SERVER_HEADERS, content_type='text/plain')
def presenterReady(request):
    module.interProcessQueue.put('start:collector')
    return '', 203


@module.route('', methods=('GET',), headers=SERVER_HEADERS, content_type='text/html')
def serveRoot(request):
    if module.presented and not DEBUG:
        module.interProcessQueue.put('stop:server')
        request.finish()
        request.connection.close()
    else:
        module.presented = True

        pathname = os.path.join(PROJECT_PATH, "frontend", "app", "index.html")
        with open(pathname, "rb") as fp:
            html = fp.read()

        stylesheetsAmalgamated = "\n".join([open(os.path.join(PROJECT_PATH, "frontend", pathname)).read() for pathname in RESOURCES_STYLE])

        # transformer = JSXTransformer()

        scriptContent = []
        for pathname in RESOURCES_SCRIPT:
            with open(os.path.join(PROJECT_PATH, 'frontend', pathname), 'rU') as fd:
                content = fd.read()

            # if pathname.endswith('.jsx'):
            #     content = transformer.transform(content)
            # if pathname.find("angular.") != -1:
            #     content = content.replace("navigator.userAgent", CHROME_USER_AGENT)
            scriptContent.append(content)
        scriptsAmalgamated = "\n".join(scriptContent)

        html = html.replace('</head>', '<script>%s</script><style>%s</style></head>' % (scriptsAmalgamated, stylesheetsAmalgamated))

        return html, 203


"""
@module.route("partials/<string:filename>.html", headers=SERVER_HEADERS, content_type="text/html")
def serveStylesheet(request, filename):
    pathname = os.path.join(PROJECT_PATH, "frontend", "app", "partials", "%s.html" % filename)
    if os.path.exists(pathname):
        with open(pathname, "rb") as fp: content = fp.read()
        return content, 203
    else:
        request.finish()
        request.connection.close()
"""

"""
@module.route('<string:filename>.min.js.map', headers=SERVER_HEADERS, content_type='application/javascript')
def serveScript(request, filename):
    if DEBUG:
        pathname = os.path.join(PROJECT_PATH, "frontend", "vendor", "angular", "%s.min.js.map" % filename)
        if os.path.exists(pathname):
            with open(pathname, "rb") as fp: content = fp.read()
            return content, 203

    request.finish()
    request.connection.close()
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


@module.route('<int:identifier>.jpg', methods=('GET',), headers=SERVER_HEADERS, content_type='image/jpg')
def serveCachedMoviePoster(request, identifier):
    themoviedb.set_key(THEMOVIEDB_API_KEY)
    themoviedb.set_cache('null')

    blob = module.imageManager.getImageBlobById(identifier)
    if blob is None:
        movie = themoviedb.Movie(identifier)
        poster = movie.poster
        sizes = poster.sizes()
        print
        print sizes
        if 'original' in sizes: sizes.remove('original')
        print sizes

        size = min(sizes, key=lambda x: abs(int(x[1:]) - 150))
        if int(size[1:]) < 150:
            size = sizes[sizes.index(size) + 1]
        print size
        print
        blob = requests.get(poster.geturl(size), headers={'User-agent': CEF_REAL_AGENT}).content
        module.imageManager.saveImageData(identifier, blob)

    # image = Image.open(StringIO(blob))
    # image.resize((150, 200), Image.ANTIALIAS)
    # blob = StringIO()
    # image.save(blob, 'JPEG')

    return blob, 203


@module.route('<path:pathname>', methods=('GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'OPTIONS', 'CONNECT'))
def serveAny(request, pathname):
    request.finish()
    request.connection.close()
