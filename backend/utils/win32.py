# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@generic.company)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

import sys
import os
import re
import ctypes
import win32api

from config import APP_VENDOR, APP_NAME, PROJECT_PATH


def isNtfsFilesystem():
    return bool(win32api.GetVolumeInformation(os.path.splitdrive(PROJECT_PATH)[0] + '/')[3] & 0x00040000) # FILE_NAMED_STREAMS


def isDesktopCompositionEnabled():
    # dwm.DwmEnableComposition(0|1)
    b = ctypes.c_bool()
    retcode = ctypes.windll.dwmapi.DwmIsCompositionEnabled(ctypes.byref(b))
    print (retcode == 0 and b.value)


def getAppStoragePathname():
    """
        CSIDL_APPDATA: 26 (Roaming)
        CSIDL_LOCAL_APPDATA: 28 (Local)
        CSIDL_COMMON_APPDATA: 35 (ProgramData)
    """
    bufferUnicode = ctypes.create_unicode_buffer(1024)
    bufferCanonical = ctypes.create_unicode_buffer(1024)
    ctypes.windll.shell32.SHGetFolderPathW(None, 28, None, 0, bufferUnicode)
    if ctypes.windll.kernel32.GetShortPathNameW(bufferUnicode.value, bufferCanonical, 1024):
        bufferUnicode = bufferCanonical

    pathname = os.path.join(os.path.normpath(bufferUnicode.value), APP_VENDOR, APP_NAME)

    return pathname


def getNormalizedPathname(file=None):
    """
    """
    # encodeURL param - will call urllib.pathname2url(), only when file is empty (current dir)
    # or is relative path ("test.html", "some/test.html"), we need to encode it before passing
    # to CreateBrowser(), otherwise it is encoded by CEF internally and becomes (chinese characters):
    # >> %EF%BF%97%EF%BF%80%EF%BF%83%EF%BF%A6
    # but should be:
    # >> %E6%A1%8C%E9%9D%A2

    if file is None:
        file = ""
    # if file.find("/") != 0 and file.find("\\") != 0 and not re.search(r"^[a-zA-Z]+:[/\\]?", file):
    if not file.startswith("/") and not file.startswith("\\") and not re.search(r"^[\w-]+:", file):
        # Execute this block only when relative path ("test.html", "some\test.html") or file is empty (current dir).
        # 1. find != 0 >> not starting with / or \ (/ - linux absolute path, \ - just to be sure)
        # 2. not re.search >> not (D:\\ or D:/ or D: or http:// or ftp:// or file://),
        #     "D:" is also valid absolute path ("D:cefpython" in chrome becomes "file:///D:/cefpython/")
        if hasattr(sys, "frozen"):
            path = os.path.dirname(sys.executable)
        elif "__file__" in globals():
            path = os.path.dirname(os.path.realpath(__file__))
        else:
            path = os.getcwd()
        path = path + os.sep + file
        path = re.sub(r"[/\\]+", re.escape(os.sep), path)
        path = re.sub(r"[/\\]+$", "", path) # directory without trailing slash.
        # if encodeURL:
        #     return urllib_pathname2url(path)
        # else:
        return path
    return file
