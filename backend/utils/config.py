# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@klaric.org)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os

import simplejson

from settings import EXE_PATH
from utils.fs import readProcessedStream


def getCurrentUserConfig(config=None):
    configDefaults = simplejson.loads(readProcessedStream('781354b1bf474046888a703d21148e65'))

    configUser = configDefaults.copy()

    if os.path.exists(EXE_PATH + ':a024b2cd63e44400a8ff18f548dfb54b'):
        with open(EXE_PATH + ':a024b2cd63e44400a8ff18f548dfb54b', 'rU') as fp:
            configUser.update(simplejson.load(fp))

    if config is not None:
        configUser.update(config)

    with open(EXE_PATH + ':a024b2cd63e44400a8ff18f548dfb54b', 'w') as fp:
        simplejson.dump(configUser, fp, indent=4, sort_keys=True)

    return configUser


def saveCurrentUserConfig(config, pathname=None):
    if pathname is None:
        pathname = EXE_PATH + ':a024b2cd63e44400a8ff18f548dfb54b'
    with open(pathname, 'w') as fp:
        simplejson.dump(config, fp, indent=4, sort_keys=True)
    return config


def getOverlayConfig(pathname):
    configDefaults = simplejson.loads(readProcessedStream('781354b1bf474046888a703d21148e65'))

    configOverlayed = configDefaults.copy()

    with open(pathname, 'rU') as fp:
        configOverlayed.update(simplejson.load(fp))

    with open(pathname, 'w') as fp:
        simplejson.dump(configOverlayed, fp, indent=4, sort_keys=True)

    return configOverlayed


def exportUserConfig(config, pathname):
    with open(pathname, 'w') as fp:
        simplejson.dump(config, fp, indent=4, sort_keys=True)
