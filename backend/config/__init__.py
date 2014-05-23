# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os

from cert import *

APP_NAME = 'ka-BOOM'
APP_VENDOR = 'Generic Company'

PROJECT_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

RESOURCES_SCRIPT = [

    # "vendor/lodash/lodash.min.js",
    'vendor/jquery/jquery.min.js',
    'app/js/app.js',
    'app/js/lib/sockets.js',
]


RESOURCES_STYLE = [
    "app/css/app.css",
    "app/css/animations.css",
]
