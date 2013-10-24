# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

import _winreg
import hashlib


def _getChromeExePath():
    """
    """
    registry = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
    try:
        key = _winreg.OpenKey(registry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe")
    except WindowsError:
        return None
    else:
        exePath = _winreg.QueryValueEx(key, "Path")[0]
        key.Close()
        return exePath


def _getChromeApplicationId(pathname):
    """
    """
    if (len(pathname) > 1 and pathname[0].islower() and pathname[1] == ":"):
        pathname = pathname[0].upper() + pathname[1:]

    pathname = pathname.encode("utf-16le")

    offset = ord("a")
    applicationId = "".join([chr(int(digit, 16) + offset) for digit in hashlib.sha256(pathname).hexdigest()[:32]])

    return applicationId
