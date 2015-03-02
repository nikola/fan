# coding: utf-8
"""
fan - A movie compilation and playback app for Windows. Fast. Lean. No weather widget.
Copyright (C) 2013-2015 Nikola Klaric.

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
__copyright__ = 'Copyright (C) 2013-2015 Nikola Klaric'

import os

import simplejson as json

from settings import APP_STORAGE_PATH, ASSETS_PATH


def processCurrentUserConfig(profile, config=None):
    userConfigFile = os.path.join(APP_STORAGE_PATH, profile + '.config', 'fan-config.json')

    with open(os.path.join(ASSETS_PATH, 'config', 'default.json'), 'rU') as fp:
        configDefaults = json.load(fp)

    configUser = configDefaults.copy()

    if os.path.exists(userConfigFile):
        with open(userConfigFile, 'rU') as fp:
            configUser.update(json.load(fp))

    if config is not None:
        configUser.update(config)

    with open(userConfigFile, 'w') as fp:
        json.dump(configUser, fp, indent=4, sort_keys=True)

    return configUser.copy()
