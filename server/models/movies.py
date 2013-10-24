# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

from models import Base

from sqlalchemy import Column, SmallInteger, Integer, BigInteger, String, Unicode, Date
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship, backref

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
    titleLocal = Column(Unicode)
    taglineLocal = Column(Unicode)
    overviewLocal = Column(Unicode)
    runtime = Column(SmallInteger)
    budget = Column(Integer)
    revenue = Column(BigInteger)
    homepage = Column(String)
    # releaseDate = Column(Date)
    releaseYear = Column(SmallInteger)
    urlBackdrop = Column(String)
    urlPoster = Column(String)
    # genres = relationship("Genre", order_by="Genre.id", backref="movie")

    # Many-to-many Movies <-> Genres.
    genres = relationship("Genre", secondary=movie_genres, backref="movies")

    def __init__(self):
        pass

    def __repr__(self):
        return "<Movie('%s')>" % (self.id)
