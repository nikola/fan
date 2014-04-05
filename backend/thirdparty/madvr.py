# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

import _winreg
from comtypes import client
import pefile
from config import MADVR_CLSID


def getInstalledVersion():
    """
    """
    try:
        client.CreateObject(MADVR_CLSID)

        registry = _winreg.ConnectRegistry(None, _winreg.HKEY_CLASSES_ROOT)
        key = _winreg.OpenKey(registry, r"CLSID\%s\InprocServer32" % MADVR_CLSID)
        pathname = _winreg.QueryValueEx(key, None)[0]
        key.Close()

        fields = pefile.PE(pathname)
        version = fields.FileInfo[0].StringTable[0].entries['ProductVersion']
    except WindowsError:
        return None
    else:
        return version
