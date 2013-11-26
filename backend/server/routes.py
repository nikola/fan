# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

import os.path
from config import PROJECT_PATH, SERVER_HEADERS
from pants.web.application import Module

module = Module()


@module.route("/", headers=SERVER_HEADERS, content_type="text/html")
def serveRoot(request):
    if not request.is_secure or request.headers.get("User-Agent", None) != module.userAgent:
        request.connection.close()
    else:
        pathname = os.path.join(PROJECT_PATH, "frontend", "app", "index.html")
        with open(pathname) as fp: content = fp.read()
        return content, 203


@module.route("/partials/<string:filename>.html", headers=SERVER_HEADERS, content_type="text/html")
def serveStylesheet(request, filename):
    pathname = os.path.join(PROJECT_PATH, "frontend", "app", "partials", "%s.html" % filename)
    if os.path.exists(pathname):
        with open(pathname) as fp: content = fp.read()
        return content, 203
    else:
        return None, 404


@module.route("/<string:filename>.css", headers=SERVER_HEADERS, content_type="text/css")
def serveStylesheet(request, filename):
    pathname = os.path.join(PROJECT_PATH, "frontend", "app", "css", "%s.css" % filename)
    if os.path.exists(pathname):
        with open(pathname) as fp: content = fp.read()
        return content, 203
    else:
        return None, 404


@module.route("/<string:filename>.js", headers=SERVER_HEADERS, content_type="application/javascript")
def serveScript(request, filename):
    pathname = os.path.join(PROJECT_PATH, "frontend", "app", "js", "%s.js" % filename)
    if os.path.exists(pathname):
        with open(pathname) as fp: content = fp.read()
        return content, 203
    else:
        return None, 404
