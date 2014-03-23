# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

from collections import namedtuple
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def createNamedTuple(*values):
    """
    """
    return namedtuple("NamedTuple", values)(*values)
