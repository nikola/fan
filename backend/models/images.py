# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

from sqlalchemy import ForeignKey, Column, Boolean, Integer, SmallInteger, LargeBinary, String, Enum, TIMESTAMP, func
from sqlalchemy.orm import relationship, backref

from models import Base, createNamedTuple


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    movieId = Column(Integer, ForeignKey('movies.id'))

    isScaled = Column(Boolean, default=False)
    width = Column(SmallInteger)
    modified = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    primaryColor = Column(String(length=6, convert_unicode=False))
    imageType = Column(Enum(*createNamedTuple('Poster', 'Backdrop')._asdict().values()), nullable=False)
    imageFormat = Column(Enum(*createNamedTuple('JPEG', 'WebP')._asdict().values()), nullable=False, default='JPEG')
    urlOriginal = Column(String(convert_unicode=False))

    blob = Column(LargeBinary)

    movie = relationship('Movie', backref=backref('images', order_by=id), lazy='joined', cascade='all, delete, delete-orphan', single_parent=True)

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __repr__(self):
        return "<Image('%s')>" % self.id
