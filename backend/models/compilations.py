# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@klaric.org)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

from sqlalchemy import Column, Unicode, Integer

from models import Base


class Compilation(Base):
    __tablename__ = 'compilations'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)

    def __repr__(self):
        return "<Compilation('%s')>" % self.id
