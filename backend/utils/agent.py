# coding: utf-8
""" http://msdn.microsoft.com/library/ms537503.aspx
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import sys
import random
import platform

VERSION_TO_TOKEN = {
    '6.3':  'Windows 8.1',
    '6.2':  'Windows 8',
    '6.1':  'Windows 7',
    '6.0':  'Windows Vista',
    '5.2':  'Windows Server 2003; Windows XP x64 Edition',
    '5.1':  'Windows XP',
    '5.01': 'Windows 2000, Service Pack 1 (SP1)',
    '5.0':  'Windows 2000',
}

COMPATIBLE_PLATFORMS = (
    'Windows 8', 'Windows 8.1',
    'Windows 7',
    'Windows Vista',
)


def getSystemVersion():
    return '%d.%d' % sys.getwindowsversion()[:2]


def getPlatformToken():
    return VERSION_TO_TOKEN.get(getSystemVersion())


def isCompatiblePlatform():
    return getPlatformToken() in COMPATIBLE_PLATFORMS


def getUserAgent():
    system = getSystemVersion()
    engine = random.randint(4, 7)
    wow = 'WOW64; ' if platform.architecture()[0] == '32bit' and platform.machine() == 'AMD64' else ''

    if engine == 7:
        return 'Mozilla/5.0 (Windows NT %s; Trident/7.0; rv:11.%d) like Gecko' % (system, random.randint(0, 2))
    else:
        return 'Mozilla/5.0 (compatible; MSIE %d.%d.%d; Windows NT %s; %sTrident/%d.0; .NET CLR 3.5.%d)' \
                % (engine + 4, random.randint(0, 1), random.randint(129, 843), system, wow, engine, random.randint(10817, 93560))
