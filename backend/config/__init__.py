# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@generic.company)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

import os

from cert import *


DEBUG = True

APP_NAME = 'ka-BOOM'
APP_VENDOR = 'Generic Company'

THEMOVIEDB_API_KEY = 'ef89c0a371440a7226e1be2ddfe84318'

CHROME_BROWSER_SETTINGS = dict(
    # default_encoding = "",
    universal_access_from_file_urls_allowed = True,
    file_access_from_file_urls_allowed = True,
    javascript_open_windows_disallowed = True,
    javascript_close_windows_disallowed = True,
    javascript_access_clipboard_disallowed = True,
    java_disabled = True,
    plugins_disabled = True,
    text_area_resize_disabled = True,
    application_cache_disabled = True,
    # pack_loading_disabled = True,
)

PROJECT_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))
# DB_PERSISTENCE_PATH = getAppStoragePathname()

SERVER_HEADERS = {
    "Server": "Microsoft-IIS/7.5",
    "X-Powered-By": "ASP.NET",
    "X-AspNet-Version": "4.0.30319",
    "X-AspNetMvc-Version": "3.0",
}

RESOURCES_SCRIPT = [
    'vendor/jquery/jquery.min.js',
    "vendor/lodash/lodash.min.js",
    "vendor/angular/angular.min.js",
    "vendor/angular/angular-animate.min.js",
    "vendor/angular/angular-route.min.js",
    "app/js/services.js",
    "app/js/controllers.js",
    "app/js/filters.js",
    "app/js/directives.js",
    "app/js/app.js",
]

RESOURCES_STYLE = [
    "app/css/app.css",
    "app/css/animations.css",
]

CHROME_USER_AGENT = '"Mozilla/5.0 (Windows NT) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.80 Safari/537.36"'

ENFORCED_CIPHERS = 'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+3DES:!aNULL:!MD5:!DSS'

MADVR_CLSID = '{E1A8B82A-32CE-4B0D-BE0D-AA68C772E423}'
