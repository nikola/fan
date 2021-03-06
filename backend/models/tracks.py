# coding: utf-8
"""
fan - A movie compilation and playback app for Windows. Fast. Lean. No weather widget.
Copyright (C) 2013-2015 Nikola Klaric.

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
__author__ = 'Nikola Klaric (nikola@klaric.org)'
__copyright__ = 'Copyright (C) 2013-2015 Nikola Klaric'

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship, backref

from models import Base


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)

    movie = relationship('Movie', backref=backref('tracks', order_by=id))

    def __init__(self, **kwargs):
        vars(self).update(kwargs)

    def __repr__(self):
        return "<Track('%s')>" % self.id