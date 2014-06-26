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

from config import PROJECT_PATH
from settings import APP_STORAGE_PATH
from settings.presenter import CEF_REAL_AGENT
# from utils.fs import createTemporaryFile, writeTemporaryFile
# from utils.win32 import getAppStoragePathname


def downloadBackdrop(streamManager, imageBaseUrl, movieUuid, discard=False):
    isBackdropDownloading = streamManager.isBackdropDownloading(movieUuid)
    if isBackdropDownloading is False:
        streamManager.startBackdropDownload(movieUuid)

        url = '%soriginal%s' % (imageBaseUrl, streamManager.getMovieByUuid(movieUuid).urlBackdrop)
        blob = requests.get(url, headers={'User-agent': CEF_REAL_AGENT}).content
        image = streamManager.saveImageData(movieUuid, 1920, blob, False, 'Backdrop', 'JPEG', url)

        streamManager.endBackdropDownload(movieUuid)
    elif isBackdropDownloading is True:
        while True:
            image = streamManager.getImageByUuid(movieUuid, 'Backdrop')
            if image is None:
                time.sleep(0.5)
            else:
                # blob = image.blob
                break
    else:
        # blob = None
        image = None

    if not discard:
        return image


def downscalePoster(streamManager, image):
    movieUuid = image.movie.uuid

    isPosterDownloading = streamManager.isPosterDownloading(movieUuid)
    if isPosterDownloading is False:
        streamManager.startPosterDownload(movieUuid)

        # url = '%soriginal%s' % (imageBaseUrl, streamManager.getMovieByUuid(movieUuid).urlBackdrop)
        blobOriginal = requests.get(image.urlOriginal, headers={'User-agent': CEF_REAL_AGENT}).content

        blobAtWidth200 = _downscaleImage(blobOriginal, 200, 300)
        streamManager.saveImageData(movieUuid, 200, blobAtWidth200, True, 'Poster', 'WebP', image.urlOriginal)
        del blobAtWidth200
        time.sleep(0.0001)

        blobAtWidth300 = _downscaleImage(blobOriginal, 300, 450)
        streamManager.saveImageData(movieUuid, 300, blobAtWidth300, True, 'Poster', 'WebP', image.urlOriginal)

        streamManager.endPosterDownload(movieUuid)

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
    convertExe = os.path.join(PROJECT_PATH, 'tools', 'convert.exe')
    convertProcess = Popen([convertExe, 'jpg:-', '-resize', '%dx%d' % (width, height), 'png:-'], stdout=PIPE, stdin=PIPE)
    convertProcess.stdin.write(blob)
    convertProcess.stdin.close()
    resizedImage = convertProcess.stdout.read()
    convertProcess.wait()

    filenameIn = os.path.join(APP_STORAGE_PATH, uuid4().hex)
    filenameOut = os.path.join(APP_STORAGE_PATH, uuid4().hex)
    with open(filenameIn, 'wb') as fd: fd.write(resizedImage)

    blobOut = None
    try:
        encodeExe = os.path.join(PROJECT_PATH, 'tools', 'cwebp.exe')
        call([encodeExe, '-preset', 'icon', '-sns', '0', '-f', '0', '-m', '0', '-mt', '-lossless', '-noalpha', '-quiet', filenameIn, '-o', filenameOut])
        with open(filenameOut, 'rb') as fp:
            blobOut = fp.read()
    finally:
        os.remove(filenameIn)
        os.remove(filenameOut)

    return blobOut
