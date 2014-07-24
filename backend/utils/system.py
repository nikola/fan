# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import sys
import platform
import ctypes
import multiprocessing
import multiprocessing.forking

import win32api

from settings import BASE_DIR


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


class _Popen(multiprocessing.forking.Popen):
    def __init__(self, *args, **kw):
        if hasattr(sys, 'frozen'):
            os.putenv('_MEIPASS2', sys._MEIPASS)
        try:
            super(_Popen, self).__init__(*args, **kw)
        finally:
            if hasattr(sys, 'frozen'):
                os.unsetenv('_MEIPASS2')


class Process(multiprocessing.Process):
    _Popen = _Popen


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
    return bool(win32api.GetVolumeInformation(os.path.splitdrive(BASE_DIR)[0] + '/')[3] & 0x00040000) # FILE_NAMED_STREAMS


def getScreenResolution():
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)


def isDesktopCompositionEnabled():
    # dwm.DwmEnableComposition(0|1)
    b = ctypes.c_bool()
    retcode = ctypes.windll.dwmapi.DwmIsCompositionEnabled(ctypes.byref(b))
    return retcode == 0 and b.value
