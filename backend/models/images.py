# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

from sqlalchemy import ForeignKey, Column, Boolean, Integer, SmallInteger, LargeBinary, String, Enum
from sqlalchemy.orm import relationship, backref

from models import Base, createNamedTuple


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    isScaled = Column(Boolean, default=False)
    idTheMovieDb = Column(Integer)
    movieId = Column(Integer, ForeignKey('movies.id'))
    width = Column(SmallInteger)
    primaryColor = Column(String(length=6, convert_unicode=False))
    imageType = Column(Enum(*createNamedTuple('Poster', 'Backdrop')._asdict().values()), nullable=False)
    blob = Column(LargeBinary)

    movie = relationship('Movie', backref=backref('images', order_by=id))

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __repr__(self):
        return "<Image('%s')>" % self.id