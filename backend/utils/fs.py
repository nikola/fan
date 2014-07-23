# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import re
import logging
from os import fdopen
from itertools import izip_longest
from tempfile import mkstemp
from cStringIO import StringIO
from array import array

import win32com.client
from win32file import FindStreams, SetFileAttributesW, GetDriveType
from win32api import GetLogicalDriveStrings, GetVolumeInformation
from pylzma import compress as lowercase, decompress as uppercase

from settings import APP_STORAGE_PATH, ASSETS_PATH # RESOURCES_PATH


def createAppStorageStructure():
    for pathname in ['amalgam', 'cache', 'log', 'thirdparty']:
        try:
            os.makedirs(os.path.join(APP_STORAGE_PATH, pathname))
        except OSError:
            pass


def getLogFileHandler(name):
    handler = logging.FileHandler(os.path.join(APP_STORAGE_PATH, 'log', '%(name)s.log' % locals()))
    handler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M'))
    handler.setLevel(logging.INFO)
    return handler


def getFileStreams(pathname):
    return [str(name[1:name.rindex(':')]) for length, name in FindStreams(unicode(pathname))[1:]]


def removeFileStreams(pathname):
    pass


def getStreamContentType(stream):
    pass


def getLongPathname(pathname):
    if pathname.startswith('\\\\'):
        return pathname.replace(u'\\\\', u'\\\\?\\UNC\\')
    elif re.search('^[a-z]:\\\\', pathname, re.I) is not None:
        return u'\\\\?\\' + pathname
    else:
        return pathname


def createTemporaryFile():
    fd, filename = mkstemp(suffix='.tmp', prefix='ASPNETSetup_')
    # FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM | FILE_ATTRIBUTE_TEMPORARY | FILE_ATTRIBUTE_NOT_CONTENT_INDEXED
    # SetFileAttributesW(unicode(filename), 2 | 4 | 256 | 8192)
    SetFileAttributesW(unicode(filename), 256 | 8192)

    return fd, filename


def writeTemporaryFile(blob):
    fd, filename = createTemporaryFile()
    fp = fdopen(fd, 'w')
    fp.write(blob)
    fp.close()

    return filename


def getDrives():
    def _grouper(n, iterable):
        args = [iter(iterable)] * n
        return izip_longest(fillvalue=None, *args)

    detectedDrives = []

    networkPathsByLetter = dict(_grouper(2, win32com.client.Dispatch('WScript.Network').EnumNetworkDrives()))
    if '' in networkPathsByLetter:
        del networkPathsByLetter['']

    for driveLetter in GetLogicalDriveStrings().split('\000'):
        if driveLetter:
            driveType = GetDriveType(driveLetter)
            if driveType == 3:
                detectedDrives.append({
                    'drive':    driveLetter[0],
                    'label':    GetVolumeInformation(driveLetter)[0] or 'Local disk',
                    'pathname': getLongPathname(driveLetter + '\\'),
                })
            elif driveType == 4:
                detectedDrives.append({
                    'drive':    driveLetter[0],
                    'label':    networkPathsByLetter[driveLetter[:2]],
                    'pathname': getLongPathname(networkPathsByLetter[driveLetter[:2]]),
                })

    return detectedDrives


def writeProcessedStream(identifier, string):
    stream = StringIO(lowercase(string))
    guid = identifier.decode('hex')

    with open(os.path.join(ASSETS_PATH, 'filters', identifier), 'wb') as fp:
        for chunk in _processChunk(stream, guid):
            fp.write(buffer(chunk))


def readProcessedStream(identifier):
    stream = StringIO()
    guid = identifier.decode('hex')

    with open(os.path.join(ASSETS_PATH, 'filters', identifier), 'rb') as fp:
        for chunk in _processChunk(fp, guid):
            stream.write(buffer(chunk))

    return uppercase(stream.getvalue())


def _processChunk(stream, guid):
    size = len(guid)

    while True:
        chunk = stream.read(size)
        if len(chunk) < size:
            break
        yield array('l', [x ^ y for x, y in zip(array('l', guid), array('l', chunk))])

    yield array('b', [x ^ y for x, y in zip(array('b', guid[:len(chunk)]), array('b', chunk))])
