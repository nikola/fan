# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

import os
import ctypes

def getAppStoragePathname(appName, appVendor):
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

    pathname = os.path.join(os.path.normpath(bufferUnicode.value), appVendor, appName)

    return pathname
