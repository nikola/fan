# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

import os.path
from config import DEBUG, PROJECT_PATH, SERVER_HEADERS, RESOURCES_SCRIPT, RESOURCES_STYLE, CHROME_USER_AGENT
from pants.web.application import Module

module = Module()


def check(function):
    def wrapper(*args, **kwargs):
        if DEBUG:
            args += True,
        else:
            request = args[0]
            args += bool(request.is_secure and request.headers.get("User-Agent", None) == module.userAgent),
        return function(*args, **kwargs)
    return wrapper


@module.route("/", headers=SERVER_HEADERS, content_type="text/html")
@check
def serveRoot(request, isAllowed):
    if isAllowed:
        pathname = os.path.join(PROJECT_PATH, "frontend", "app", "index.html")
        with open(pathname, "rb") as fp:
            html = fp.read()

        stylesheetsAmalgamated = "\n".join([open(os.path.join(PROJECT_PATH, "frontend", pathname)).read() for pathname in RESOURCES_STYLE])
        html = html.replace("</head>", "<style>" + stylesheetsAmalgamated + "</style></head>")

        scriptContent = []
        for pathname in RESOURCES_SCRIPT:
            with open(os.path.join(PROJECT_PATH, "frontend", pathname)) as fp:
                content = fp.read()
            if pathname.find("angular.") != -1:
                content = content.replace("navigator.userAgent", CHROME_USER_AGENT)
            scriptContent.append(content)
        scriptsAmalgamated = "\n".join(scriptContent)
        html = html.replace("</body>", "<script>" + scriptsAmalgamated + "</script></body>")

        return html, 203

    request.connection.close()


@module.route("/partials/<string:filename>.html", headers=SERVER_HEADERS, content_type="text/html")
@check
def serveStylesheet(request, filename, isAllowed):
    if isAllowed:
        pathname = os.path.join(PROJECT_PATH, "frontend", "app", "partials", "%s.html" % filename)
        if os.path.exists(pathname):
            with open(pathname, "rb") as fp: content = fp.read()
            return content, 203

    request.connection.close()


@module.route("/<string:filename>.min.js.map", headers=SERVER_HEADERS, content_type="application/javascript")
@check
def serveScript(request, filename, isAllowed):
    if isAllowed:
        pathname = os.path.join(PROJECT_PATH, "frontend", "vendor", "angular", "%s.min.js.map" % filename)
        if os.path.exists(pathname):
            with open(pathname, "rb") as fp: content = fp.read()
            return content, 203

    request.connection.close()
