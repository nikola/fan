# coding: utf-8
"""
fan - A movie compilation and playback app for Windows. Fast. Lean. No weather widget.
Copyright (C) 2013-2014 Nikola Klaric.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
__author__ = 'Nikola Klaric (nikola@klaric.org)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os

import simplejson

from settings import BASE_DIR, APP_STORAGE_PATH
from utils.system import getCurrentInstanceIdentifier

DEFAULT_CONFIG_FILE = os.path.join(BASE_DIR, 'config', 'default.json')
USER_CONFIG_FILE = os.path.join(APP_STORAGE_PATH, getCurrentInstanceIdentifier() + '.config', 'fan-config.json')


def getCurrentUserConfig(config=None):
    with open(DEFAULT_CONFIG_FILE, 'rU') as fp:
        configDefaults = simplejson.load(fp)

    configUser = configDefaults.copy()

    if os.path.exists(USER_CONFIG_FILE):
        with open(USER_CONFIG_FILE, 'rU') as fp:
            configUser.update(simplejson.load(fp))

    if config is not None:
        configUser.update(config)

    with open(USER_CONFIG_FILE, 'w') as fp:
        simplejson.dump(configUser, fp, indent=4, sort_keys=True)

    return configUser


def saveCurrentUserConfig(config, pathname=USER_CONFIG_FILE):
    with open(pathname, 'w') as fp:
        simplejson.dump(config, fp, indent=4, sort_keys=True)
    return config


def getOverlayConfig(pathname):
    with open(DEFAULT_CONFIG_FILE, 'rU') as fp:
        configDefaults = simplejson.load(fp)

    configOverlayed = configDefaults.copy()

    with open(pathname, 'rU') as fp:
        configOverlayed.update(simplejson.load(fp))

    with open(pathname, 'w') as fp:
        simplejson.dump(configOverlayed, fp, indent=4, sort_keys=True)

    return configOverlayed


def exportUserConfig(config, pathname):
    with open(pathname, 'w') as fp:
        simplejson.dump(config, fp, indent=4, sort_keys=True)
