# coding: utf-8
""" http://msdn.microsoft.com/library/ms537503.aspx
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import random
import platform
from utils.system import getSystemVersion


def getUserAgent():
    system = getSystemVersion()
    engine = random.randint(4, 7)
    wow = 'WOW64; ' if platform.architecture()[0] == '32bit' and platform.machine() == 'AMD64' else ''

    if engine == 7:
        return 'Mozilla/5.0 (Windows NT %s; Trident/7.0; rv:11.%d) like Gecko' % (system, random.randint(0, 2))
    else:
        return 'Mozilla/5.0 (compatible; MSIE %d.%d.%d; Windows NT %s; %sTrident/%d.0; .NET CLR 3.5.%d)' \
                % (engine + 4, random.randint(0, 1), random.randint(129, 843), system, wow, engine, random.randint(10817, 93560))
