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
from hashlib import md5 as MD5
from array import array

import win32api

from settings import BASE_DIR, EXE_PATH, ASSETS_PATH


TRIDENT_ID = None


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


def getCurrentInstanceIdentifier():
    global TRIDENT_ID

    if TRIDENT_ID is None:
        version = getProductVersion(os.path.join(ASSETS_PATH, 'trident', 'libcef.dll'))

        md5 = MD5()
        md5.update(os.path.join(EXE_PATH, version))
        TRIDENT_ID = md5.hexdigest()[:16]

    return TRIDENT_ID


def getProductVersion(pathname):
    if os.path.exists(pathname) and os.path.isfile(pathname):
        filename = unicode(pathname)

        size = ctypes.windll.version.GetFileVersionInfoSizeW(filename, None)
        if size:
            res = ctypes.create_string_buffer(size)
            ctypes.windll.version.GetFileVersionInfoW(filename, None, size, res)
            r = ctypes.c_uint()
            l = ctypes.c_uint()
            ctypes.windll.version.VerQueryValueA(res, '\\VarFileInfo\\Translation', ctypes.byref(r), ctypes.byref(l))
            if l.value:
                ctypes.windll.version.VerQueryValueA(
                    res,
                    '\\StringFileInfo\\%04x%04x\\FileVersion' % tuple(array('H', ctypes.string_at(r.value, l.value))[:2].tolist()),
                    ctypes.byref(r), ctypes.byref(l),
                )
                return '.'.join([num.rstrip('\x00') for num in ctypes.string_at(r.value, l.value).split('.')])

    raise ValueError
