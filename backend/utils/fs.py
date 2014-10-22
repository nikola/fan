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
import re
import logging
from itertools import izip_longest

import win32com.client
from win32file import FindStreams, GetDriveType
from win32api import GetLogicalDriveStrings, GetVolumeInformation

from settings import APP_STORAGE_PATH
from utils.system import getCurrentInstanceIdentifier


def createAppStorageStructure():
    prefix = getCurrentInstanceIdentifier()
    for pathname in [
        'amalgam',
        'thirdparty',
        prefix + '.data',
        prefix + '.cache',
        prefix + '.log',
        prefix + '.config',
        prefix + '.lock',
        os.path.join('artwork', 'backdrops'),
        os.path.join('artwork', 'posters'),
        os.path.join('backlog', 'backdrops'),
        os.path.join('backlog', 'posters'),
    ]:
        try:
            os.makedirs(os.path.join(APP_STORAGE_PATH, pathname))
        except OSError:
            pass


def getLogFileHandler(name):
    createAppStorageStructure()

    handler = logging.FileHandler(os.path.join(APP_STORAGE_PATH, getCurrentInstanceIdentifier() + '.log', '%(name)s.log' % locals()))
    handler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M'))
    handler.setLevel(logging.INFO)
    return handler


def getFileStreams(pathname):
    return [str(name[1:name.rindex(':')]) for length, name in FindStreams(unicode(pathname))[1:]]


def getLongPathname(pathname):
    if pathname.startswith('\\\\'):
        return pathname.replace(u'\\\\', u'\\\\?\\UNC\\')
    elif re.search('^[a-z]:\\\\', pathname, re.I) is not None:
        return u'\\\\?\\' + pathname
    else:
        return pathname


def getDrives():
    def _grouper(n, iterable):
        args = [iter(iterable)] * n
        return izip_longest(fillvalue=None, *args)

    detectedDrives = []

    networkPathsByLetter = dict(_grouper(2, win32com.client.Dispatch('WScript.Network').EnumNetworkDrives()))
    if '' in networkPathsByLetter:
        del networkPathsByLetter['']

    for driveLetter in GetLogicalDriveStrings().split('\000'):
        if driveLetter:
            driveType = GetDriveType(driveLetter)
            if driveType == 3:
                detectedDrives.append({
                    'drive':    driveLetter[0],
                    'label':    GetVolumeInformation(driveLetter)[0] or 'Local disk',
                    'pathname': getLongPathname(driveLetter + '\\'),
                })
            elif driveType == 4:
                detectedDrives.append({
                    'drive':    driveLetter[0],
                    'label':    networkPathsByLetter[driveLetter[:2]],
                    'pathname': getLongPathname(networkPathsByLetter[driveLetter[:2]]),
                })

    return detectedDrives
