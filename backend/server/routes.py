# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os.path

from pants.web.application import Module
from pants.http import WebSocket

from config import PROJECT_PATH, SERVER_HEADERS, RESOURCES_SCRIPT, RESOURCES_STYLE, CHROME_USER_AGENT
# from watcher.control import work as startStreamManager


module = Module()


@module.route('', headers=SERVER_HEADERS, content_type='text/html')
def serveRoot(request):
    # print serveRoot
    pathname = os.path.join(PROJECT_PATH, "frontend", "app", "index.html")
    with open(pathname, "rb") as fp:
        html = fp.read()

    stylesheetsAmalgamated = "\n".join([open(os.path.join(PROJECT_PATH, "frontend", pathname)).read() for pathname in RESOURCES_STYLE])

    scriptContent = []
    for pathname in RESOURCES_SCRIPT:
        with open(os.path.join(PROJECT_PATH, "frontend", pathname)) as fp:
            content = fp.read()
        if pathname.find("angular.") != -1:
            content = content.replace("navigator.userAgent", CHROME_USER_AGENT)
        scriptContent.append(content)
    scriptsAmalgamated = "\n".join(scriptContent)

    html = html.replace('</head>', '<script>%s</script><style>%s</style></head>' % (scriptsAmalgamated, stylesheetsAmalgamated))

    return html, 203


@module.route('ready', headers=SERVER_HEADERS, content_type='text/plain')
def presenterReady(request):
    module.interProcessQueue.put('start:collector')
    return '', 203


@module.route("partials/<string:filename>.html", headers=SERVER_HEADERS, content_type="text/html")
def serveStylesheet(request, filename):
    pathname = os.path.join(PROJECT_PATH, "frontend", "app", "partials", "%s.html" % filename)
    if os.path.exists(pathname):
        with open(pathname, "rb") as fp: content = fp.read()
        return content, 203
    else:
        request.finish()
        request.connection.close()


@module.route("<string:filename>.min.js.map", headers=SERVER_HEADERS, content_type="application/javascript")
def serveScript(request, filename):
    pathname = os.path.join(PROJECT_PATH, "frontend", "vendor", "angular", "%s.min.js.map" % filename)
    if os.path.exists(pathname):
        with open(pathname, "rb") as fp: content = fp.read()
        return content, 203
    else:
        request.finish()
        request.connection.close()


@module.route('<string:filename>.png', headers=SERVER_HEADERS, content_type='image/png')
def serveImage(request, filename):
    pathname = os.path.join(PROJECT_PATH, 'frontend', 'app', 'img', '%s.png' % filename)
    if os.path.exists(pathname):
        with open(pathname, 'rb') as fp: content = fp.read()
        return content, 203
    else:
        request.finish()
        request.connection.close()


@module.route('<string:name>.socket')
class EchoSocket(WebSocket):

    # def on_handshake(self, request, headers):
    #     return True # self.is_secure and 'X-Pizza' in request.headers

    def on_connect(self, name):
        print 1
        print name
        self.read_delimiter = u'\n' # TODO: oder '\n' ???
        self.write(u"Hello, {name}!".format(name=name))

    def on_read(self, data):
        print 2
        print data
        self.write(data)


"""
@module.route("<path:pathname>", headers=SERVER_HEADERS)
def serveAny(request, pathname):
    request.finish()
    request.connection.close()
"""
