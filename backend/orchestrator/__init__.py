# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@klaric.org)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import logging

from settings import DEBUG
from settings import LOG_CONFIG
from utils.fs import getLogFileHandler

logging.basicConfig(**LOG_CONFIG)
logger = logging.getLogger('scanner')
logger.propagate = DEBUG
logger.addHandler(getLogFileHandler('scanner'))

SERVER_HEADERS = {'Server': 'Microsoft-IIS/7.5', 'X-Powered-By': 'ASP.NET', 'X-AspNet-Version': '4.0.30319', 'X-AspNetMvc-Version': '3.0'}
