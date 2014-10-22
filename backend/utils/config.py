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

from settings import EXE_PATH, BASE_DIR


def getCurrentUserConfig(config=None):
    with open(os.path.join(BASE_DIR, 'config', 'default.json'), 'rU') as fp:
        configDefaults = simplejson.load(fp)

    configUser = configDefaults.copy()

    if os.path.exists(EXE_PATH + ':a024b2cd63e44400a8ff18f548dfb54b'):
        with open(EXE_PATH + ':a024b2cd63e44400a8ff18f548dfb54b', 'rU') as fp:
            configUser.update(simplejson.load(fp))

    if config is not None:
        configUser.update(config)

    with open(EXE_PATH + ':a024b2cd63e44400a8ff18f548dfb54b', 'w') as fp:
        simplejson.dump(configUser, fp, indent=4, sort_keys=True)

    return configUser


def saveCurrentUserConfig(config, pathname=None):
    if pathname is None:
        pathname = EXE_PATH + ':a024b2cd63e44400a8ff18f548dfb54b'
    with open(pathname, 'w') as fp:
        simplejson.dump(config, fp, indent=4, sort_keys=True)
    return config


def getOverlayConfig(pathname):
    with open(os.path.join(BASE_DIR, 'config', 'default.json'), 'rU') as fp:
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
