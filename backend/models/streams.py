# coding: utf-8
"""
fan - A movie compilation and playback app for Windows. Fast. Lean. No weather widget.
Copyright (C) 2013-2014 Nikola Klaric.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

from sqlalchemy import Column, Integer, Unicode, Enum, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from models import Base, createNamedTuple


class Stream(Base):
    __tablename__ = 'streams'

    id = Column(Integer, primary_key=True)
    movieId = Column(Integer, ForeignKey('movies.id'))

    format = Column(Enum(*createNamedTuple('Matroska', 'BD')._asdict().values()))
    space = Column(Enum(*createNamedTuple('D2', 'D3')._asdict().values()))
    resolution = Column(String(length=7, convert_unicode=False))
    edit = Column(String(convert_unicode=False))
    location = Column(Unicode)

    movie = relationship('Movie', backref=backref('streams', order_by=id), lazy='joined', cascade='all, delete, delete-orphan', single_parent=True)

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __repr__(self):
        return "<Stream('%s')>" % self.id
