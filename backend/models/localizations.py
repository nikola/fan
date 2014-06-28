# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

from sqlalchemy import ForeignKey, Column, Unicode, Integer, String
from sqlalchemy.orm import relationship, backref

from models import Base


class Localization(Base):
    __tablename__ = 'localizations'

    id = Column(Integer, primary_key=True)
    movieId = Column(Integer, ForeignKey('movies.id'))

    locale = Column(String(length=2, convert_unicode=False))
    title = Column(Unicode)
    storyline = Column(Unicode)

    movie = relationship('Movie', backref=backref('localizations', order_by=id))

    def __repr__(self):
        return "<Localization('%s')>" % self.id