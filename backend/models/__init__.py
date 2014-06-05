# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import bz2
from contextlib import contextmanager
from sqlite3 import dbapi2 as sqlite

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


from settings import DEBUG
from utils.win32 import getAppStoragePathname
from models.common import Base, GUID, createNamedTuple, createUuid # , DictSerializable
from models.streams import Stream
from models.genres import Genre
from models.movies import Movie
from models.variants import Variant
from models.images import Image


# TODO: use named tuples ?
#   https://docs.python.org/2/library/collections.html#collections.namedtuple

def _getSqliteDsn(identifier):
    if DEBUG:
        directory = getAppStoragePathname()
        if not os.path.exists(directory): os.makedirs(directory)

        dsn = 'sqlite:///' + (directory + '\\%s.sqlite3' % identifier).replace('\\', r'\\\\')
    else:
        dsn = 'sqlite://'

    return dsn


class StreamManager(object):

    @contextmanager
    def _session(self, session=None):
        if session:
            yield session
        else:
            session = self.session_factory()
            try:
                yield session
            except:
                session.rollback()
                raise
            else:
                session.commit()


    def __init__(self):
        self.engine = create_engine(_getSqliteDsn('db'), echo=False, module=sqlite)
        self.engine.execute('select 1').scalar()
        self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
        # Base.metadata.drop_all(self.engine, checkfirst=True)

        if not DEBUG and os.path.exists(os.path.join(getAppStoragePathname(), 'data.accdb')):
            self._restore()
            # TODO: migrate schema
            # https://sqlalchemy-migrate.readthedocs.org/en/latest/
        else:
            Base.metadata.create_all(self.engine)


    def shutdown(self):
        print 'StreamManager.shutdown()'
        # if not DEBUG:
        #     self._persist()


    def getMovieByUuid(self, identifier):
        with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.uuid == identifier).one()
            except NoResultFound:
                return None
            else:
                return movie


    def addMovieStream(self, movieRecord, streamLocation):
        if not streamLocation: return

        movie = None
        with self._session() as session:
            try:
                stream = session.query(Stream).filter_by(location=streamLocation).one()
            except NoResultFound:
                streamFormat = 'Matroska' if streamLocation.lower().endswith('.mkv') else 'BD'
                stream = Stream(
                    format = streamFormat,
                    location = streamLocation,
                )
                session.add(stream)

            if movieRecord is not None:
                try:
                    movie = session.query(Movie).filter("titleOriginal=:title and releaseYear=:year").params(title=movieRecord["titleOriginal"], year=movieRecord["releaseYear"]).one()
                except NoResultFound:
                    movie = Movie(**movieRecord)
                    variant = Variant(**movieRecord)
                    variant.movie = movie
                    session.add_all([movie, variant])

                stream.movie = movie

            session.commit()

        return movie


    def deleteStreams(self):
        with self._session() as session:
            session.query(Stream).delete()
            session.query(Movie).delete()


    def deleteMovie(self, identifier):
        with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.uuid == identifier).one()
            except NoResultFound:
                return None
            else:
                movie.delete()
                session.commit()


    def isStreamKnown(self, streamLocation):
        with self._session() as session:
            try:
                session.query(Stream).filter(Stream.location == streamLocation).one()
            except NoResultFound:
                return False
            else:
                return True


    def getMovieFromStreamLocation(self, streamLocation):
        with self._session() as session:
            try:
                stream = session.query(Stream).filter(Stream.location == streamLocation).one()
            except NoResultFound:
                return None
            else:
                return stream.movie


    def getImageBlobByUuid(self, identifier, imageType='Poster'):
        with self._session() as session:
            try:
                image = session.query(Image).filter(Image.movie.has(Movie.uuid == identifier), Image.imageType == imageType).first()
            except NoResultFound:
                return None
            else:
                if image is not None:
                    return image.blob
                else:
                    return None


    def saveImageData(self, identifier, width, blob, imageType='Poster'):
        with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.uuid == identifier).one()
            except NoResultFound:
                return None
            else:
                image = Image(
                    imageType = imageType,
                    movie = movie,
                    width = width,
                    blob = blob,
                )
                session.add(image)
                session.commit()


    def getAllMovies(self):
        with self._session() as session:
            movies = []
            for movie in session.query(Movie).values(Movie.uuid, Movie.titleOriginal, Movie.releaseYear, Movie.runtime):
                movies.append({
                    'uuid': movie[0],
                    'titleOriginal': movie[1],
                    'releaseYear': movie[2],
                    'runtime': movie[3],
                })
            return movies
            # return list(session.query(Movie).values(
            #     Movie.uuid,
            #     Movie.titleOriginal,
            #     Movie.releaseYear,
            # ))


    def getMovieAsJson(self, identifier):
        with self._session() as session:
            try:
                movie = list(session.query(Movie).filter(Movie.uuid == identifier).values(Movie.uuid, Movie.titleOriginal, Movie.releaseYear, Movie.runtime))[0]
            except NoResultFound:
                return None
            else:
                return {
                    'uuid': movie[0],
                    'titleOriginal': movie[1],
                    'releaseYear': movie[2],
                    'runtime': movie[3],
                }


    def _persist(self):
        compressor = bz2.BZ2Compressor()
        connection = self.engine.raw_connection()
        if not os.path.exists(getAppStoragePathname()):
            os.makedirs(getAppStoragePathname())
        fp = open(os.path.join(getAppStoragePathname(), 'data.accdb'), 'wb')
        try:
            for line in connection.iterdump():
                fp.write(compressor.compress(line.encode('utf-8')))
            fp.write(compressor.flush())
        finally:
            fp.close()
            connection.close()


    def _restore(self):
        connection = self.engine.raw_connection()
        try:
            with open(os.path.join(getAppStoragePathname(), 'data.accdb'), 'rb') as fp:
                connection.cursor().executescript(bz2.decompress(fp.read()).decode('utf-8'))
        except:
            raise
        else:
            connection.commit()
        finally:
            connection.close()
