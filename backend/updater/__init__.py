# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

import types
import inspect
from operator import itemgetter


class Component(object):

    def __init__(self, *args, **kwargs):
        self._identifier = args[0]
        for method in map(itemgetter(0), inspect.getmembers(self, predicate=inspect.ismethod)):
            if method in kwargs: setattr(self, method, types.MethodType(kwargs.get(method), self))

    def getLatestReleaseVersion(self, *args, **kwargs):
        raise NotImplementedError

    def getInstalledVersion(self, *args, **kwargs):
        raise NotImplementedError

    def installLatestReleaseVersion(self, *args, **kwargs):
        raise NotImplementedError
