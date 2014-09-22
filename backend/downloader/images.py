# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import time
from subprocess import call
from uuid import uuid4
from contextlib import closing
from cStringIO import StringIO

import requests

from settings import ASSETS_PATH, APP_STORAGE_PATH
from settings import ENTROPY_SEED


from . import logger


def downloadChunks(url, pollCallback=None):

    def _yield():
        if pollCallback is not None:
            pollCallback()
        else:
            time.sleep(0)

    stream = StringIO()
    try:
        with closing(requests.get(url, headers={'User-Agent': ENTROPY_SEED}, stream=True)) as response:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    stream.write(chunk)
                    _yield()
    except requests.ConnectionError:
        logger.error('Could not connect to image host URL: %s', url)
    else:
        _yield()
        blob = stream.getvalue()
        _yield()
        return blob


def downloadBackdrop(streamManager, imageBaseUrl, movieUuid, pollCallback=None):

    def _yield(period=0):
        if pollCallback is not None:
            pollCallback()
        time.sleep(period)

    logger.info('Downloading backdrop for "%s" ...' % streamManager.getMovieTitleByUuid(movieUuid))

    _yield()
    isBackdropDownloading = streamManager.isBackdropDownloading(movieUuid)
    _yield()
    if isBackdropDownloading is True:
        while True:
            isBackdropStored = streamManager.isImageAvailable(movieUuid, 'Backdrop', 1920)
            if not isBackdropStored:
                _yield(0.5)
            else:
                _yield()
                break
    elif isBackdropDownloading is False:
        streamManager.startBackdropDownload(movieUuid)
        _yield()

        url = '%soriginal%s' % (imageBaseUrl, streamManager.getMovieByUuid(movieUuid).urlBackdrop)
        _yield()
        blob = downloadChunks(url, pollCallback)
        _yield()

        if blob is not None:
            streamManager.saveImageData(movieUuid, 1920, blob, False, 'Backdrop', 'JPEG', url)
            _yield()

        streamManager.endBackdropDownload(movieUuid)
        _yield()


def downscalePoster(streamManager, movieUuid, urlOriginal):
    logger.info('Starting production of downscaled poster image for "%s" ...' % streamManager.getMovieTitleByUuid(movieUuid))

    isPosterDownloading = streamManager.isPosterDownloading(movieUuid)
    time.sleep(0)
    time.sleep(0)
    if isPosterDownloading is True:
        while True:
            imageModified, imageIsScaled = streamManager.getImageMetadataByUuid(movieUuid, 'Poster')
            if imageModified is None:
                time.sleep(0.5)
            else:
                time.sleep(0)
                break
    elif isPosterDownloading is False:
        streamManager.startPosterDownload(movieUuid)

        logger.info('Downloading image data from %s ...', urlOriginal)
        time.sleep(0)
        blobOriginal = downloadChunks(urlOriginal)
        time.sleep(0)

        if len(blobOriginal) < 5000:
            streamManager.endPosterDownload(movieUuid)
            return False
        else:
            filenameRaw = _saveRawImage(blobOriginal)
            time.sleep(0)

            try:
                for width, height in [(150, 225), (200, 300), (300, 450)]:
                    blobResized = _downscaleImage(filenameRaw, width, height)
                    time.sleep(0)
                    if blobResized is not None:
                        streamManager.saveImageData(movieUuid, width, blobResized, True, 'Poster', 'WebP', urlOriginal)
                        time.sleep(0)
                    else:
                        logger.error('Could not downscale image to %dx%d!', width, height)
            finally:
                os.remove(filenameRaw)
                time.sleep(0)

            streamManager.endPosterDownload(movieUuid)
            time.sleep(0)

    return True


def _saveRawImage(blob):
    filenameRaw = os.path.join(APP_STORAGE_PATH, uuid4().hex)
    with open(filenameRaw, 'wb') as fp:
        fp.write(blob)

    return filenameRaw


def _downscaleImage(filenameRaw, width, height):
    blobOut = None

    # filenameRaw = os.path.join(APP_STORAGE_PATH, uuid4().hex)
    filenameResized = os.path.join(APP_STORAGE_PATH, uuid4().hex)
    filenameRecoded = os.path.join(APP_STORAGE_PATH, uuid4().hex)

    # with open(filenameRaw, 'wb') as fd:
    #     fd.write(blob)
    # time.sleep(0)

    try:
        # shell = ['cmd', '/c', 'start', '/MIN', '/LOW', '/B', '/WAIT']

        convertExe = os.path.join(ASSETS_PATH, 'tools', 'convert.exe')
        # call([convertExe, 'jpg:%s' % filenameRaw, '-colorspace', 'RGB', '-define', 'filter:window=Quadratic', '-distort', 'Resize', '%dx%d' % (width, height), '-colorspace', 'sRGB', 'png:%s' % filenameResized], shell=True)
        # call([convertExe, 'jpg:%s' % filenameRaw, '-colorspace', 'RGB', '-filter', 'Lanczos', '-define', 'filter:blur=.9891028367558475', '-distort', 'Resize', '%dx%d' % (width, height), '-colorspace', 'sRGB', 'png:%s' % filenameResized], shell=True)
        call([convertExe, 'jpg:%s' % filenameRaw, '-colorspace', 'RGB', '-filter', 'RobidouxSharp', '-distort', 'Resize', '%dx%d' % (width, height), '-colorspace', 'sRGB', 'png:%s' % filenameResized],
             shell=True)
        time.sleep(0)

        encodeExe = os.path.join(ASSETS_PATH, 'tools', 'cwebp.exe')
        call([encodeExe, '-preset', 'picture', '-hint', 'picture', '-sns', '0', '-f', '0', '-q', '0', '-m', '0', '-lossless', '-af', '-noalpha', '-quiet', filenameResized, '-o', filenameRecoded],
             shell=True)
        time.sleep(0)
        try:
            with open(filenameRecoded, 'rb') as fp:
                blobOut = fp.read()
        except IOError:
            logger.error('Could not convert image.')
        time.sleep(0)
    finally:
        try:
            # os.remove(filenameRaw)
            # time.sleep(0)
            os.remove(filenameResized)
            time.sleep(0)
            os.remove(filenameRecoded)
            time.sleep(0)
        except WindowsError:
            pass

    return blobOut
