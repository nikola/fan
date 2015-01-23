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
__copyright__ = 'Copyright (C) 2013-2015 Nikola Klaric'

import os
import sys
import platform
import ctypes
import multiprocessing
import multiprocessing.forking
from hashlib import md5 as MD5
from array import array

import win32api
import win32con
import win32process

from settings import EXE_PATH, ASSETS_PATH


PRIORITIES = {
    'idle': win32process.IDLE_PRIORITY_CLASS,
    'lower': win32process.BELOW_NORMAL_PRIORITY_CLASS,
    'normal': win32process.NORMAL_PRIORITY_CLASS,
    'higher': win32process.ABOVE_NORMAL_PRIORITY_CLASS,
}

INSTANCE_ID = None

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


def setPriority(priority='normal'):
    pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, PRIORITIES.get(priority))


def getSystemVersion():
    return '%d.%d' % sys.getwindowsversion()[:2]


def getPlatformToken():
    return VERSION_TO_TOKEN.get(getSystemVersion())


def isCompatiblePlatform():
    return getPlatformToken() in COMPATIBLE_PLATFORMS \
        and not platform.win32_ver()[-1].endswith(" Checked") \
        and platform.architecture()[0] == "32bit"


def getScreenResolution():
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)


def isDesktopCompositionEnabled():
    # dwm.DwmEnableComposition(0|1)
    b = ctypes.c_bool()
    retcode = ctypes.windll.dwmapi.DwmIsCompositionEnabled(ctypes.byref(b))
    return retcode == 0 and b.value


def getCurrentInstanceIdentifier():
    global INSTANCE_ID

    if INSTANCE_ID is None:
        version = getProductVersion(os.path.join(ASSETS_PATH, 'thirdparty', 'cef', 'libcef.dll'))

        md5 = MD5()
        md5.update('%s:%s:DB-Schema-0002' % (EXE_PATH, version))
        INSTANCE_ID = md5.hexdigest()[:16]

    return INSTANCE_ID


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
