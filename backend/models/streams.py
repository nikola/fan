# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

from sqlalchemy import Column, Integer, Unicode, Enum, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from models import Base, createNamedTuple
# from vendor.sqlalchemy_utils.types.choice import ChoiceType

class Stream(Base):
    __tablename__ = 'streams'

    id = Column(Integer, primary_key=True)
    movieId = Column(Integer, ForeignKey('movies.id'))

    format = Column(Enum(*createNamedTuple('Matroska', 'BD')._asdict().values()))
    version = Column(String(convert_unicode=False))
    location = Column(Unicode)

    movie = relationship('Movie', backref=backref('streams', order_by=id), cascade='all, delete, delete-orphan', single_parent=True)

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __repr__(self):
        return "<Stream('%s')>" % self.id
