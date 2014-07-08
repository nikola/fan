# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os

from cert import *


PROJECT_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

RESOURCES_SCRIPT = [
    # 'vendor/lodash/lodash.min.js',
    # 'vendor/bacon/bacon.min.js',
    'vendor/cortex/cortex.min.js',
    'vendor/jquery/jquery.min.js',
    # 'vendor/jquery/jquery.swipe-events.js',

    'vendor/jquery/jquery.waitforimages.min.js',
    'vendor/misc/color-thief.min.js',
    'vendor/misc/keypress.min.js',

    'vendor/velocity/velocity.min.js',
    'vendor/velocity/velocity.ui.js',

    'app/js/lib/sockets.js',
    'app/js/lib/colors.js',
    'app/js/lib/l10n.js',
    'app/js/lib/receiver.js',
    'app/js/lib/hotkeys.js',
    'app/js/lib/lang.js',
    'app/js/lib/config.js',
    'app/js/lib/grid.js',
    'app/js/lib/detail.js',
    'app/js/app.js',
]

RESOURCES_STYLE = [
    'app/css/fonts.css',
    'app/css/icons.css',

    'app/css/app.css',

    'app/css/buttons.css',
    'app/css/config.css',
    'app/css/grid.css',
    'app/css/detail.css',
]
