# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@klaric.org)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

from sqlalchemy import ForeignKey, Column, SmallInteger, Integer, BigInteger, String, Unicode, Boolean
from sqlalchemy.orm import relationship, backref

from models import Base, GUID, createUuid



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
    compilationId = Column(Integer, ForeignKey('compilations.id'))

    uuid = Column(GUID, default=createUuid)
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

    genres = Column(String(convert_unicode=False))

    # sourceBackdrop = Column(String(convert_unicode=False))
    keyBackdrop = Column(String(convert_unicode=False))
    isBackdropCached = Column(Boolean, default=False)
    # isBackdropDownloading = Column(Boolean, default=False)

    # sourcePoster = Column(String(convert_unicode=False))
    keyPoster = Column(String(convert_unicode=False))
    primaryColorPoster = Column(String(length=6, convert_unicode=False))


    # urlPoster = Column(String(convert_unicode=False))

    # isPosterDownloading = Column(Boolean, default=False)

    # Many-to-many Movies <-> Genres.
    # genres = relationship('Genre', secondary=movie_genres, backref='movies')

    compilation = relationship('Compilation', backref=backref('movies', order_by=id), cascade='all, delete, delete-orphan', single_parent=True)

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self):
        return "<Movie('%s')>" % self.id
