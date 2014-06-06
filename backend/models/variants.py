# coding: utf-8
""" TODO: replace with https://github.com/kvesteri/sqlalchemy-i18n
"""
__author__ = "Nikola Klaric (nikola@generic.company)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy_utils import LocaleType
from sqlalchemy.orm import relationship, backref
from models import Base


class Variant(Base):
    __tablename__ = "variants"

    id = Column(Integer, primary_key=True)
    locale = Column(LocaleType)
    title = Column(Unicode)
    tagline = Column(Unicode)
    overview = Column(Unicode)

    movieId = Column(Integer, ForeignKey("movies.id"))
    movie = relationship("Movie", backref=backref("variants", order_by=id))

    def __init__(self, locale, titleLocal, taglineLocal, overview, **kwargs):
        self.locale = locale
        self.title = titleLocal
        self.tagline = taglineLocal
        self.overview = overview

    def __repr__(self):
        return "<Variant('%s')>" % (self.id)
