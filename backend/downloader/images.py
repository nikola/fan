# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import time
from subprocess import Popen, PIPE, call
from uuid import uuid4
from contextlib import closing
from cStringIO import StringIO

import requests

from settings import ASSETS_PATH, APP_STORAGE_PATH
from settings import ENTROPY_SEED


from . import logger


def _downloadChunks(url):
    stream = StringIO()
    try:
        with closing(requests.get(url, headers={'User-Agent': ENTROPY_SEED}, stream=True)) as response:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    stream.write(chunk)
                    time.sleep(0)
    except requests.ConnectionError:
        logger.error('Could not connect to image host URL: %s', url)
    else:
        return stream.getvalue()


def downloadBackdrop(streamManager, imageBaseUrl, movieUuid, discard=False):
    logger.info('Downloading backdrop for "%s" ...' % streamManager.getMovieTitleByUuid(movieUuid))

    imageModified, imageBlob = None, None

    time.sleep(0)
    isBackdropDownloading = streamManager.isBackdropDownloading(movieUuid)
    time.sleep(0)
    if isBackdropDownloading is False:
        streamManager.startBackdropDownload(movieUuid)

        url = '%soriginal%s' % (imageBaseUrl, streamManager.getMovieByUuid(movieUuid).urlBackdrop)
        time.sleep(0)
        blob = _downloadChunks(url)
        time.sleep(0)

        if blob is not None:
            imageModified, imageBlob = streamManager.saveImageData(movieUuid, 1920, blob, False, 'Backdrop', 'JPEG', url)
            time.sleep(0)

        streamManager.endBackdropDownload(movieUuid)
        time.sleep(0)
    elif isBackdropDownloading is True:
        while True:
            imageModified, imageBlob = streamManager.getImageByUuid(movieUuid, 'Backdrop')
            if imageBlob is None:
                time.sleep(0.5)
            else:
                break

    if not discard:
        return imageModified, imageBlob


def downscalePoster(streamManager, movieUuid, urlOriginal):
    logger.info('Starting production of downscaled poster image for "%s" ...' % streamManager.getMovieTitleByUuid(movieUuid))

    isPosterDownloading = streamManager.isPosterDownloading(movieUuid)
    time.sleep(0)
    if isPosterDownloading is False:
        streamManager.startPosterDownload(movieUuid)

        logger.info('Downloading image data from %s ...', urlOriginal)
        time.sleep(0)
        blobOriginal = _downloadChunks(urlOriginal)
        time.sleep(0)

        blobAtWidth200 = _downscaleImage(blobOriginal, 200, 300)
        time.sleep(0)
        if blobAtWidth200 is not None:
            streamManager.saveImageData(movieUuid, 200, blobAtWidth200, True, 'Poster', 'WebP', urlOriginal)
            time.sleep(0)
        else:
            logger.error('Could not downscale image to 200x300!')

        blobAtWidth300 = _downscaleImage(blobOriginal, 300, 450)
        time.sleep(0)
        if blobAtWidth300 is not None:
            streamManager.saveImageData(movieUuid, 300, blobAtWidth300, True, 'Poster', 'WebP', urlOriginal)
            time.sleep(0)
        else:
            logger.error('Could not downscale image to 300x450!')

        streamManager.endPosterDownload(movieUuid)
        time.sleep(0)

        return True
    else:
        return False

    # TODO: complete this
    # elif isPosterDownloading is True:
    #     while True:
    #         blob = streamManager.getImageBlobByUuid(movieUuid, 'Backdrop')
    #         if blob is None:
    #             time.sleep(0.5)
    #         else:
    #             break
    # else:
    #     blob = None


def _downscaleImage(blob, width, height):
    blobOut = None

    convertExe = os.path.join(ASSETS_PATH, 'tools', 'convert.exe')
    convertProcess = Popen([convertExe, 'jpg:-', '-resize', '%dx%d' % (width, height), 'png:-'], stdout=PIPE, stdin=PIPE)
    time.sleep(0)
    try:
        convertProcess.stdin.write(blob)
    except IOError:
        logger.error('Could not execute image downscaler!')
    else:
        convertProcess.stdin.close()
        time.sleep(0)
        resizedImage = convertProcess.stdout.read()
        time.sleep(0)
        convertProcess.wait()

        filenameIn = os.path.join(APP_STORAGE_PATH, uuid4().hex)
        filenameOut = os.path.join(APP_STORAGE_PATH, uuid4().hex)
        with open(filenameIn, 'wb') as fd:
            fd.write(resizedImage)
        time.sleep(0)

        try:
            encodeExe = os.path.join(ASSETS_PATH, 'tools', 'cwebp.exe')
            call([encodeExe, '-preset', 'icon', '-sns', '0', '-f', '0', '-m', '0', '-mt', '-lossless', '-noalpha', '-quiet', filenameIn, '-o', filenameOut])
            time.sleep(0)
            with open(filenameOut, 'rb') as fp:
                blobOut = fp.read()
            time.sleep(0)
        finally:
            os.remove(filenameIn)
            time.sleep(0)
            os.remove(filenameOut)
            time.sleep(0)

    return blobOut
