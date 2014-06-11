# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import time

import requests

from settings.presenter import CEF_REAL_AGENT


def downloadBackdrop(streamManager, imageBaseUrl, movieUuid, discard=False):
    isBackdropDownloading = streamManager.isBackdropDownloading(movieUuid)
    if isBackdropDownloading is False:
        streamManager.startBackdropDownload(movieUuid)

        url = '%soriginal%s' % (imageBaseUrl, streamManager.getMovieByUuid(movieUuid).urlBackdrop)
        blob = requests.get(url, headers={'User-agent': CEF_REAL_AGENT}).content
        streamManager.saveImageData(movieUuid, 1920, blob, False, 'Backdrop')

        streamManager.endBackdropDownload(movieUuid)
    elif isBackdropDownloading is True:
        while True:
            blob = streamManager.getImageBlobByUuid(movieUuid, 'Backdrop')
            if blob is None:
                time.sleep(0.5)
            else:
                break
    else:
        blob = None

    if not discard:
        return blob
