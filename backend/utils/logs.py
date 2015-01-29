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

import sys
import os
import logging

from settings import APP_STORAGE_PATH

LOG_CONFIG = dict(
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M',
    level=logging.INFO,
    filemode='a',
)
HANDLERS = {}

def getLogger(profile, name):
    if not HANDLERS.has_key(name):
        handler = logging.FileHandler(os.path.join(APP_STORAGE_PATH, profile + '.log', name + '.log'))
        handler.setFormatter(logging.Formatter(LOG_CONFIG.get('format'), LOG_CONFIG.get('datefmt')))
        handler.setLevel(LOG_CONFIG.get('level'))
        HANDLERS[name] = handler
    else:
        handler = HANDLERS[name]

    logging.basicConfig(**LOG_CONFIG)
    logger = logging.getLogger(name)
    logger.propagate = not getattr(sys, 'frozen', False)
    logger.addHandler(handler)

    return logger
