# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

from sqlalchemy import Table, ForeignKey, Column, SmallInteger, Integer, BigInteger, String, Unicode, Boolean
from sqlalchemy.orm import relationship

from models import Base, GUID, createUuid # , DictSerializable

GENRES_EN = (
    "Action",
    "Adventure",
    "Animation",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Family",
    "Fantasy",
    "Foreign",
    "History",
    "Horror",
    "Music",
    "Mystery",
    "Romance",
    "Science Fiction",
    "TV movie",
    "Thriller",
    "War",
    "Western",
)


# Association table.
# movie_genres = Table('movie_genres', Base.metadata,
#     Column('movie_id', Integer, ForeignKey('movies.id')),
#     Column('genre_id', Integer, ForeignKey('genres.id')),
# )


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    uuid = Column(GUID, default=createUuid)
    idImdb = Column(String)
    idTheMovieDb = Column(Integer)
    titleOriginal = Column(Unicode)
    overview = Column(Unicode)
    runtime = Column(SmallInteger)
    budget = Column(Integer)
    revenue = Column(BigInteger)
    homepage = Column(String)
    releaseYear = Column(SmallInteger)
    urlBackdrop = Column(String)
    isBackdropDownloading = Column(Boolean, default=False)
    urlPoster = Column(String)
    isPosterDownloading = Column(Boolean, default=False)

    # Many-to-many Movies <-> Genres.
    # genres = relationship('Genre', secondary=movie_genres, backref='movies')

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    # def as_dict(self):
    #     # print 'as_dict'
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return "<Movie('%s')>" % self.id
