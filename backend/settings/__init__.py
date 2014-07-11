# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import sys
import os
from utils.win32 import getAppStoragePathname

DEBUG = True # END DEBUG
BASE_DIR = os.path.dirname(sys.executable) if hasattr(sys, 'frozen') else os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))
RESOURCES_PATH = sys._MEIPASS if getattr(sys, 'frozen', None) else os.path.join(BASE_DIR, 'backend')
EXE_PATH = sys.executable if getattr(sys, 'frozen', None) else os.path.join(BASE_DIR, 'dummy.exe')
APP_STORAGE_PATH = getAppStoragePathname()
LOG_CONFIG = dict(
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M',
    level=20, # logging.INFO
    filemode='a',
)
