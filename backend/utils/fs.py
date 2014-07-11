# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import re
import logging
from os import fdopen
from tempfile import mkstemp
from win32file import FindStreams, SetFileAttributesW

from settings import APP_STORAGE_PATH


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
    elif re.search('^[a-z]]:\\\\', pathname, re.I) is not None:
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
