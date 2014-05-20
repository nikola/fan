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
