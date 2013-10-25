# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

import os
from utils.win32 import getAppStoragePathname


def getSqliteDsn():
    """
    """
    directory = getAppStoragePathname("ka-boom", "Generic Company")

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = "sqlite:///" + (directory + "\\data").replace("\\", r"\\\\")

    return filename
