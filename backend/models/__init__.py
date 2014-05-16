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
from sqlalchemy.sql import exists
from utils.win32 import getAppStoragePathname
from models.common import Base, createNamedTuple
from models.streams import Stream
from models.genres import Genre
from models.movies import Movie
from models.variants import Variant
from config import DEBUG

# TODO: use named tuples ?
#   https://docs.python.org/2/library/collections.html#collections.namedtuple

def _getSqliteDsn():
    if DEBUG:
        directory = getAppStoragePathname()
        if not os.path.exists(directory): os.makedirs(directory)

        dsn = 'sqlite:///' + (directory + '\\db.sqlite3').replace('\\', r'\\\\')
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

    def __init__(self): # ), pathname):
        # self._persistencePathname = pathname
        self.engine = create_engine(_getSqliteDsn(), echo=False, module=sqlite)
        self.engine.execute('select 1').scalar()
        self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
        Base.metadata.drop_all(self.engine, checkfirst=True)

        # if not DEBUG and os.path.exists(os.path.join(self._persistencePathname, 'data.accdb')):
        if not DEBUG and os.path.exists(os.path.join(getAppStoragePathname(), 'data.accdb')):
            self._restore()
            # TODO: migrate schema
            # https://sqlalchemy-migrate.readthedocs.org/en/latest/
        else:
            Base.metadata.create_all(self.engine)

    def shutdown(self):
        print 'streamManager.shutdown()'
        if not DEBUG:
            self._persist()

    def addMovieStream(self, movieRecord, streamLocation):
        if not movieRecord or not streamLocation: return

        with self._session() as session:
            try:
                stream = session.query(Stream).filter_by(location=streamLocation).one()
            except NoResultFound:
                streamFormat = "Matroska" if streamLocation.lower().endswith(".mkv") else "BD"
                stream = Stream(
                    format = streamFormat,
                    location = streamLocation,
                )
                session.add(stream)

            try:
                movie = session.query(Movie).filter("titleOriginal=:title and releaseYear=:year").params(title=movieRecord["titleOriginal"], year=movieRecord["releaseYear"]).one()
            except NoResultFound:
                movie = Movie(**movieRecord)
                variant = Variant(**movieRecord)
                variant.movie = movie
                session.add_all([movie, variant])

            stream.movie = movie

            session.commit()

    def _persist(self):
        compressor = bz2.BZ2Compressor()
        connection = self.engine.raw_connection()
        if not os.path.exists(getAppStoragePathname()): # self._persistencePathname):
            # os.makedirs(self._persistencePathname)
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
