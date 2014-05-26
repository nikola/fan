# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

from sqlalchemy import ForeignKey, Column, Integer, SmallInteger, LargeBinary, String
from sqlalchemy.orm import relationship, backref

from models import Base


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    idTheMovieDb = Column(Integer)
    width = Column(SmallInteger)
    primaryColor = Column(String(length=6, convert_unicode=False))
    blob = Column(LargeBinary)
    movieId = Column(Integer, ForeignKey('movies.id'))

    movie = relationship('Movie', backref=backref('images', order_by=id))

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __repr__(self):
        return "<Image('%s')>" % self.id