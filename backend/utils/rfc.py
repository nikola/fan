# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import datetime
from email.utils import parsedate


_WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
_MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def getRfc1123Timestamp(timestamp):
    return '%s, %02d %s %04d %02d:%02d:%02d GMT' \
        % (_WEEKDAYS[timestamp.weekday()], timestamp.day, _MONTHS[timestamp.month - 1], timestamp.year, timestamp.hour, timestamp.minute, timestamp.second)


def parseRfc1123Timestamp(timestamp):
    return datetime.datetime(*parsedate(timestamp)[:6])
