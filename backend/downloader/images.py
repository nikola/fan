# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import time
from subprocess import Popen, PIPE, call
from uuid import uuid4

import requests

from settings import ASSETS_PATH, APP_STORAGE_PATH
from settings import ENTROPY_SEED


from . import logger


def downloadBackdrop(streamManager, imageBaseUrl, movieUuid, discard=False):
    imageModified, imageBlob = None, None

    isBackdropDownloading = streamManager.isBackdropDownloading(movieUuid)
    if isBackdropDownloading is False:
        streamManager.startBackdropDownload(movieUuid)

        url = '%soriginal%s' % (imageBaseUrl, streamManager.getMovieByUuid(movieUuid).urlBackdrop)
        blob = requests.get(url, headers={'User-Agent': ENTROPY_SEED}).content
        # image = streamManager.saveImageData(movieUuid, 1920, blob, False, 'Backdrop', 'JPEG', url)
        imageModified, imageBlob = streamManager.saveImageData(movieUuid, 1920, blob, False, 'Backdrop', 'JPEG', url)

        streamManager.endBackdropDownload(movieUuid)
    elif isBackdropDownloading is True:
        while True:
            # image = streamManager.getImageByUuid(movieUuid, 'Backdrop')
            imageModified, imageBlob = streamManager.getImageByUuid(movieUuid, 'Backdrop')
            if imageBlob is None:
                time.sleep(0.5)
            else:
                # blob = image.blob
                break
    else:
        # blob = None
        image = None

    if not discard:
        # return image
        return imageModified, imageBlob


def downscalePoster(streamManager, image):
    movieUuid = image.movie.uuid

    isPosterDownloading = streamManager.isPosterDownloading(movieUuid)
    if isPosterDownloading is False:
        streamManager.startPosterDownload(movieUuid)

        logger.info('Downloading image data from %s ...' % image.urlOriginal)
        try:
            blobOriginal = requests.get(image.urlOriginal, headers={'User-Agent': ENTROPY_SEED}).content
        except requests.ConnectionError:
            logger.error('Could not connect to image host!')
            return None
        else:
            logger.info('... done.')

            logger.info('Downscaling image to 200x300 ...')
            blobAtWidth200 = _downscaleImage(blobOriginal, 200, 300)

            if blobAtWidth200 is not None:
                logger.info('... done.')
                streamManager.saveImageData(movieUuid, 200, blobAtWidth200, True, 'Poster', 'WebP', image.urlOriginal)
            else:
                logger.error('Could not downscale image!')
                # del blobAtWidth200
                # time.sleep(0.0001)

            logger.info('Downscaling image to 300x450 ...')
            blobAtWidth300 = _downscaleImage(blobOriginal, 300, 450)
            if blobAtWidth300 is not None:
                logger.info('... done.')
                streamManager.saveImageData(movieUuid, 300, blobAtWidth300, True, 'Poster', 'WebP', image.urlOriginal)
            else:
                logger.error('Could not downscale image!')

            streamManager.endPosterDownload(movieUuid)

            if blobAtWidth200 is not None:
                return movieUuid
    else:
        return # TODO: complete this
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
    try:
        convertProcess.stdin.write(blob)
    except IOError:
        logger.error('Could not execute image downscaler!')
    else:
        convertProcess.stdin.close()
        resizedImage = convertProcess.stdout.read()
        convertProcess.wait()

        filenameIn = os.path.join(APP_STORAGE_PATH, uuid4().hex)
        filenameOut = os.path.join(APP_STORAGE_PATH, uuid4().hex)
        with open(filenameIn, 'wb') as fd:
            fd.write(resizedImage)

        try:
            encodeExe = os.path.join(ASSETS_PATH, 'tools', 'cwebp.exe')
            call([encodeExe, '-preset', 'icon', '-sns', '0', '-f', '0', '-m', '0', '-mt', '-lossless', '-noalpha', '-quiet', filenameIn, '-o', filenameOut])
            with open(filenameOut, 'rb') as fp:
                blobOut = fp.read()
        finally:
            os.remove(filenameIn)
            os.remove(filenameOut)

    return blobOut
