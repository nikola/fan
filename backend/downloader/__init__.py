# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import logging

from settings import LOG_CONFIG
from utils.fs import getLogFileHandler

logging.basicConfig(**LOG_CONFIG)
logger = logging.getLogger('downloader')
logger.addHandler(getLogFileHandler('downloader'))
