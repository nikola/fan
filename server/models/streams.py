# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from models import Base, createNamedTuple


class Stream(Base):
    __tablename__ = "streams"

    id = Column(Integer, primary_key=True)
    streamFormat = Column(Enum(*createNamedTuple("Matroska")._asdict().values()))

    def __init__(self):
        pass

    def __repr__(self):
        return "<Stream('%s')>" % (self.id)
