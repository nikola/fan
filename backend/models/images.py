# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

from sqlalchemy import Column, Integer, LargeBinary, String

from models import Base


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    idTheMovieDb = Column(Integer)
    blob = Column(LargeBinary)
    primaryColor = Column(String(length=6, convert_unicode=False))

    def __repr__(self):
        return "<Image('%s')>" % self.id