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
            imageModified, imageBlob, imageIsScaled = streamManager.getImageByUuid(movieUuid, 'Backdrop')
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

        if len(blobOriginal) < 5000:
            streamManager.endPosterDownload(movieUuid)
            return False
        else:
            filenameRaw = _saveRawImage(blobOriginal)
            time.sleep(0)

            try:
                blobAtWidth150 = _downscaleImage(filenameRaw, 150, 225)
                time.sleep(0)
                if blobAtWidth150 is not None:
                    streamManager.saveImageData(movieUuid, 150, blobAtWidth150, True, 'Poster', 'WebP', urlOriginal)
                    time.sleep(0)
                else:
                    logger.error('Could not downscale image to 150x225!')

                blobAtWidth200 = _downscaleImage(filenameRaw, 200, 300)
                time.sleep(0)
                if blobAtWidth200 is not None:
                    streamManager.saveImageData(movieUuid, 200, blobAtWidth200, True, 'Poster', 'WebP', urlOriginal)
                    time.sleep(0)
                else:
                    logger.error('Could not downscale image to 200x300!')

                blobAtWidth300 = _downscaleImage(filenameRaw, 300, 450)
                time.sleep(0)
                if blobAtWidth300 is not None:
                    streamManager.saveImageData(movieUuid, 300, blobAtWidth300, True, 'Poster', 'WebP', urlOriginal)
                    time.sleep(0)
                else:
                    logger.error('Could not downscale image to 300x450!')
            finally:
                os.remove(filenameRaw)
                time.sleep(0)

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
        shell = ['cmd', '/c', 'start', '/MIN', '/LOW', '/B', '/WAIT']

        convertExe = os.path.join(ASSETS_PATH, 'tools', 'convert.exe')
        # call([convertExe, 'jpg:%s' % filenameRaw, '-colorspace', 'RGB', '-define', 'filter:window=Quadratic', '-distort', 'Resize', '%dx%d' % (width, height), '-colorspace', 'sRGB', 'png:%s' % filenameResized], shell=True)
        # call([convertExe, 'jpg:%s' % filenameRaw, '-colorspace', 'RGB', '-filter', 'Lanczos', '-define', 'filter:blur=.9891028367558475', '-distort', 'Resize', '%dx%d' % (width, height), '-colorspace', 'sRGB', 'png:%s' % filenameResized], shell=True)
        call(shell + [convertExe, 'jpg:%s' % filenameRaw, '-colorspace', 'RGB', '-filter', 'RobidouxSharp', '-distort', 'Resize', '%dx%d' % (width, height), '-colorspace', 'sRGB', 'png:%s' % filenameResized],
             shell=False)
        time.sleep(0)

        encodeExe = os.path.join(ASSETS_PATH, 'tools', 'cwebp.exe')
        call(shell + [encodeExe, '-preset', 'picture', '-hint', 'picture', '-sns', '0', '-f', '0', '-m', '0', '-lossless', '-af', '-noalpha', '-quiet', filenameResized, '-o', filenameRecoded],
             shell=False)
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
