# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

from utils.win32 import getAppStoragePathname

DEBUG = True

APP_STORAGE_PATH = getAppStoragePathname()
LOG_CONFIG = dict(
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M',
    level=20, # logging.INFO
    filemode='a',
)
