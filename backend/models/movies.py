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
__author__ = 'Nikola Klaric (nikola@klaric.org)'
__copyright__ = 'Copyright (C) 2013-2014 Nikola Klaric'

from sqlalchemy import ForeignKey, Column, SmallInteger, Integer, BigInteger, String, Unicode, Boolean
from sqlalchemy.orm import relationship, backref

from models import Base


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    compilationId = Column(Integer, ForeignKey('compilations.id'))

    streamless = Column(Boolean, default=True)

    idTheMovieDb = Column(Integer)
    idImdb = Column(String(convert_unicode=False))
    idYoutubeTrailer = Column(String(convert_unicode=False))

    titleOriginal = Column(Unicode)
    releaseYear = Column(SmallInteger)
    runtime = Column(SmallInteger)

    homepage = Column(String(convert_unicode=False))
    budget = Column(Integer)
    revenue = Column(BigInteger)

    rating = Column(SmallInteger)

    keyBackdrop = Column(String(convert_unicode=False))
    isBackdropCached = Column(Boolean, default=False)

    keyPoster = Column(String(convert_unicode=False))
    primaryColorPoster = Column(String(length=6, convert_unicode=False))

    compilation = relationship('Compilation', backref=backref('movies', order_by=id), cascade='all, delete, delete-orphan', single_parent=True)

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self):
        return "<Movie('%s')>" % self.id
