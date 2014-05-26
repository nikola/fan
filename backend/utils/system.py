# coding: utf-8
"""
"""
import os
import win32api
from config import PROJECT_PATH

__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import sys
import platform


VERSION_TO_TOKEN = {
    '6.3':  'Windows 8.1',
    '6.2':  'Windows 8',
    '6.1':  'Windows 7',
    '6.0':  'Windows Vista',
    '5.2':  'Windows Server 2003; Windows XP x64 Edition',
    '5.1':  'Windows XP',
    '5.01': 'Windows 2000, Service Pack 1 (SP1)',
    '5.0':  'Windows 2000',
}

COMPATIBLE_PLATFORMS = (
    'Windows 8', 'Windows 8.1',
    'Windows 7',
    'Windows Vista',
)


def getSystemVersion():
    return '%d.%d' % sys.getwindowsversion()[:2]


def getPlatformToken():
    return VERSION_TO_TOKEN.get(getSystemVersion())


def isCompatiblePlatform():
    """ Must be Windows 7 or higher, non-debug revision, and 32-bit Python interpreter due to CEF dependency.
    """
    return getPlatformToken() in COMPATIBLE_PLATFORMS \
        and not platform.win32_ver()[-1].endswith(" Checked") \
        and platform.architecture()[0] == "32bit"


def isNtfsFilesystem():
    return bool(win32api.GetVolumeInformation(os.path.splitdrive(PROJECT_PATH)[0] + '/')[3] & 0x00040000) # FILE_NAMED_STREAMS
