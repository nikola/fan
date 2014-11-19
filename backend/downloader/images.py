# coding: utf-8
"""
fan - A movie compilation and playback app for Windows. Fast. Lean. No weather widget.
Copyright (C) 2013-2014 Nikola Klaric.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
from __future__ import division

__author__ = 'Nikola Klaric (nikola@klaric.org)'
__copyright__ = 'Copyright (C) 2013-2014 Nikola Klaric'

import os
import time
import shutil
from socket import error as SocketError
from subprocess import call
from contextlib import closing
from hashlib import md5 as MD5

import requests

from settings import ASSETS_PATH, APP_STORAGE_PATH, CLIENT_AGENT
from utils.logs import getLogger

CONVERT_EXE = os.path.join(ASSETS_PATH, 'thirdparty', 'convert', 'convert.exe')
CWEBP_EXE = os.path.join(ASSETS_PATH, 'thirdparty', 'cwebp', 'cwebp.exe')


def processInitialArtwork(profile, movieRecord, containerLocation, imageBaseUrl, imageClosestSize, pollingCallback):
    logger = getLogger(profile, 'downloader')

    for imageType in ('Poster', 'Backdrop'):
        pathnameOverlay = os.path.join(os.path.dirname(containerLocation), imageType.lower() + '.jpg')
        pollingCallback()
        if os.path.exists(pathnameOverlay):
            pollingCallback()

            logger.info('Using local ' + imageType.lower() + ' for "%s (%d)" found in %s' % (movieRecord['title'], movieRecord['releaseYear'], os.path.dirname(containerLocation)))
            pollingCallback()

            identifier = getHashFromImage(pathnameOverlay, pollingCallback)
            pathnameArtwork = os.path.join(APP_STORAGE_PATH, 'artwork', imageType.lower() + 's', identifier, imageType.lower() + '.jpg')
            if not os.path.exists(pathnameArtwork):
                try:
                    pollingCallback()
                    os.makedirs(os.path.dirname(pathnameArtwork))
                except OSError:
                    pass
                pollingCallback()
                shutil.copy(pathnameOverlay, pathnameArtwork)
                pollingCallback()
            movieRecord['key' + imageType] = identifier

            if imageType == 'Poster':
                processBacklogEntry(profile, 'poster', identifier, False, pollingCallback)
            elif imageType == 'Backdrop':
                pass
        else:
            movieRecord['key' + imageType] = movieRecord['url' + imageType].replace('/', '').replace('.jpg', '')
            pathname = os.path.join(APP_STORAGE_PATH, 'artwork', imageType.lower() + 's', movieRecord['key' + imageType])
            try:
                os.makedirs(pathname)
            except OSError:
                pass
            pollingCallback()
            with open(os.path.join(pathname, 'source.url'), 'wb+') as fp:
                fp.write('[InternetShortcut]\r\nURL=%soriginal%s\r\n' % (imageBaseUrl, movieRecord['url' + imageType]))
            pollingCallback()
            closing(open(os.path.join(APP_STORAGE_PATH, 'backlog', imageType.lower() + 's', movieRecord['key' + imageType]), 'w+'))
            pollingCallback()

            if imageType == 'Poster':
                downloadArtwork(profile, '%s%s/%s.jpg' % (imageBaseUrl,  imageClosestSize, movieRecord.get('keyPoster')), 'poster@draft', movieRecord.get('keyPoster'), pollingCallback)
            elif imageType == 'Backdrop':
                processBacklogEntry(profile, 'backdrop', movieRecord.get('keyBackdrop'), True, pollingCallback)


def downloadArtwork(profile, imageUrl, imageType, imageId, pollingCallback=None):

    def _yield(period=0):
        if pollingCallback is not None:
            pollingCallback()
        else:
            time.sleep(period)

    logger = getLogger(profile, 'downloader')

    imageName = imageType[:imageType.find('@')] if imageType.find('@') != -1 else imageType

    imageDirectory = os.path.join(APP_STORAGE_PATH, 'artwork', imageName + 's', imageId)
    incompleteImagePath = os.path.join(imageDirectory, imageType + '.incomplete')
    completeImagePath = os.path.join(imageDirectory, imageType + '.jpg')

    if os.path.exists(incompleteImagePath):
        os.remove(incompleteImagePath)

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
            with closing(requests.get(imageUrl, headers={'User-Agent': CLIENT_AGENT}, stream=True)) as response:
                timeStart = time.clock()
                for chunk in response.iter_content(chunk_size=4096):
                    if chunk:
                        chunks += 1
                        localStream.write(chunk)
                        _yield()
                duration = time.clock() - timeStart
                _yield()
        except (requests.ConnectionError, SocketError):
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

        # TODO: check if file size of image > 5000 bytes
        os.rename(incompleteImagePath, completeImagePath)

    return True


def getBacklogEntry(artworkType):
    backlogItems = os.listdir(os.path.join(APP_STORAGE_PATH, 'backlog', artworkType + 's'))
    time.sleep(0)
    return backlogItems[0] if len(backlogItems) else None


def processBacklogEntry(profile, artworkType, key, isRemoteSource=True, pollingCallback=None):

    def _yield(period=0):
        if pollingCallback is not None:
            pollingCallback()
        else:
            time.sleep(period)

    if isRemoteSource:
        os.remove(os.path.join(APP_STORAGE_PATH, 'backlog', artworkType + 's', key))
        _yield()

        link = open(os.path.join(APP_STORAGE_PATH, 'artwork', artworkType + 's', key, 'source.url'), 'rU').read()
        _yield()
        sourceUrl = link[link.find('=') + 1:].strip()

        result = downloadArtwork(profile, sourceUrl, artworkType, key)
    else:
        result = True

    if artworkType == 'poster':
        if result:
            pathname = os.path.join(APP_STORAGE_PATH, 'artwork', 'posters', key)
            filename = os.path.join(pathname, 'poster')

            kwargs = {'creationflags': 0x00000040} # IDLE_PRIORITY_CLASS

            for width, height in [(150, 225), (200, 300), (300, 450)]:
                if not os.path.exists(os.path.join(pathname, '%s@%d.webp' % (filename, width))):
                    _yield()

                    call([CONVERT_EXE, 'jpg:%s.jpg' % filename, '-colorspace', 'RGB', '-filter', 'RobidouxSharp', '-distort', 'Resize', '%dx%d' % (width, height), '-colorspace', 'sRGB', 'png:%s@%d.png' % (filename, width)],
                         shell=True, **kwargs)
                    _yield()

                    # https://developers.google.com/speed/webp/gallery1
                    # https://developers.google.com/speed/webp/docs/cwebp
                    call([CWEBP_EXE, '-preset', 'picture', '-hint', 'picture', '-sns', '0', '-f', '0', '-q', '0', '-m', '0', '-lossless', '-af', '-noalpha', '-quiet', filename + ('@%d.png' % width), '-o', filename + ('@%d.webp' % width)],
                         shell=True, **kwargs)
                    _yield()
        else:
            closing(open(os.path.join(APP_STORAGE_PATH, 'backlog', artworkType + 's', key), 'w+'))
            _yield()

    return result


def getHashFromImage(filename, pollingCallback):
    md5 = MD5()
    with open(filename, 'rb') as fp:
        for chunk in iter(lambda: fp.read(32 * md5.block_size), b''):
            md5.update(chunk)
            pollingCallback()
    return md5.hexdigest()
