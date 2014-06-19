# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

from sqlalchemy import ForeignKey, Column, Boolean, Integer, SmallInteger, LargeBinary, String, Enum, TIMESTAMP, func
from sqlalchemy.orm import relationship, backref

from models import Base, createNamedTuple


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)

    movie = relationship('Movie', backref=backref('tracks', order_by=id))

    def __init__(self, **kwargs):
        vars(self).update(kwargs)

    def __repr__(self):
        return "<Track('%s')>" % self.id