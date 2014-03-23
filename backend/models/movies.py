# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

from sqlalchemy import Column, SmallInteger, Integer, BigInteger, String, Unicode
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

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
movie_genres = Table("movie_genres", Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id")),
    Column("genre_id", Integer, ForeignKey("genres.id")),
)


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    idImdb = Column(String)
    titleOriginal = Column(Unicode)
    runtime = Column(SmallInteger)
    budget = Column(Integer)
    revenue = Column(BigInteger)
    homepage = Column(String)
    releaseYear = Column(SmallInteger)
    urlBackdrop = Column(String)
    urlPoster = Column(String)

    # Many-to-many Movies <-> Genres.
    genres = relationship("Genre", secondary=movie_genres, backref="movies")

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __repr__(self):
        return "<Movie('%s')>" % (self.id)
