# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

from sqlalchemy import Column, SmallInteger, Integer, BigInteger, String, Unicode, Boolean

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
    uuid = Column(GUID, default=createUuid)

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

    urlBackdrop = Column(String(convert_unicode=False))
    isBackdropDownloading = Column(Boolean, default=False)

    urlPoster = Column(String(convert_unicode=False))
    isPosterDownloading = Column(Boolean, default=False)

    # Many-to-many Movies <-> Genres.
    # genres = relationship('Genre', secondary=movie_genres, backref='movies')

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self):
        return "<Movie('%s')>" % self.id
