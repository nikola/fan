# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

from sqlalchemy import Column, Integer, Unicode, Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from models import Base, createNamedTuple
# from vendor.sqlalchemy_utils.types.choice import ChoiceType

class Stream(Base):
    __tablename__ = "streams"

    id = Column(Integer, primary_key=True)
    format = Column(Enum(*createNamedTuple("Matroska", "BD")._asdict().values()))
    location = Column(Unicode)
    movieId = Column(Integer, ForeignKey("movies.id"))

    movie = relationship("Movie", backref=backref("streams", order_by=id))

    def __init__(self, format, location, **kwargs):
        self.format = format
        self.location = location

    def __repr__(self):
        return "<Stream('%s')>" % (self.id)
