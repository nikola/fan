# coding: utf-8
"""
"""
from __future__ import division

__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import time
from subprocess import call
# from uuid import uuid4
from contextlib import closing
from cStringIO import StringIO

import requests

from settings import ASSETS_PATH, APP_STORAGE_PATH
from settings import ENTROPY_SEED


from . import logger


CONVERT_EXE = os.path.join(ASSETS_PATH, 'tools', 'convert.exe')
CWEBP_EXE = os.path.join(ASSETS_PATH, 'tools', 'cwebp.exe')


def downloadArtwork(imageUrl, imageType, imageId):

    def _yield(period=0):
        time.sleep(period)

    imageName = imageType[:imageType.find('@')] if imageType.find('@') != -1 else imageType

    imageDirectory = os.path.join(APP_STORAGE_PATH, 'artwork', imageName + 's', imageId)
    incompleteImagePath = os.path.join(imageDirectory, imageType + '.incomplete')
    completeImagePath = os.path.join(imageDirectory, imageType + '.jpg')

    if not os.path.exists(completeImagePath):
        try:
            os.makedirs(imageDirectory)
        except OSError:
            pass
        _yield()

        localStream = open(incompleteImagePath, 'wb')
        _yield()

        chunks = 0
        try:
            logger.info('Starting download of %s from %s', imageName, imageUrl)
            with closing(requests.get(imageUrl, headers={'User-Agent': ENTROPY_SEED}, stream=True)) as response:
                timeStart = time.clock()
                for chunk in response.iter_content(chunk_size=4096):
                    if chunk:
                        chunks += 1
                        localStream.write(chunk)
                        _yield()
                duration = time.clock() - timeStart
                _yield()
        except requests.ConnectionError:
            logger.error('Could not connect to image host server at URL: %s', imageUrl)
            _yield()
            return False
        else:
            logger.info('... finished download of %s, avg. transfer rate: %.0f KiB/s.', imageName, (chunks * 4) / duration)
        finally:
            localStream.flush()
            _yield()
            localStream.close()
            _yield()

        # TODO: check file size of image to be > 5000
        os.rename(incompleteImagePath, completeImagePath)

    return True


def getBacklogEntry(artworkType):
    backlogItems = os.listdir(os.path.join(APP_STORAGE_PATH, 'backlog', artworkType + 's'))
    time.sleep(0)
    return backlogItems[0] if len(backlogItems) else None


def processBacklogEntry(artworkType, key):
    link = open(os.path.join(APP_STORAGE_PATH, 'artwork', artworkType + 's', key, 'source.url'), 'rU').read()
    time.sleep(0)
    sourceUrl = link[link.find('=') + 1:].strip()

    result = downloadArtwork(sourceUrl, artworkType, key)
    if artworkType == 'poster':
        if result:
            pathname = os.path.join(APP_STORAGE_PATH, 'artwork', 'posters', key)
            filename = os.path.join(pathname, 'poster')
            kwargs = {'creationflags': 0x00000040} # IDLE_PRIORITY_CLASS

            for width, height in [(150, 225), (200, 300), (300, 450)]:
                call([CONVERT_EXE, 'jpg:%s.jpg' % filename, '-colorspace', 'RGB', '-filter', 'RobidouxSharp', '-distort', 'Resize', '%dx%d' % (width, height), '-colorspace', 'sRGB', 'png:%s@%d.png' % (filename, width)],
                     shell=True, **kwargs)
                time.sleep(0)

                call([CWEBP_EXE, '-preset', 'picture', '-hint', 'picture', '-sns', '0', '-f', '0', '-q', '0', '-m', '0', '-lossless', '-af', '-noalpha', '-quiet', filename + ('@%d.png' % width), '-o', filename + ('@%d.webp' % width)],
                     shell=True, **kwargs)
                time.sleep(0)
        else:
            pass # TODO: handle failure

    if result:
        os.remove(os.path.join(APP_STORAGE_PATH, 'backlog', artworkType + 's', key))
    return result
