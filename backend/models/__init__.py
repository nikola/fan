# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

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


def _getSqliteDsn():
    """
    """
    directory = getAppStoragePathname("ka-boom", "Generic Company")

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = "sqlite:///" + (directory + "\\data.accdr").replace("\\", r"\\\\")

    return filename


class StreamManager(object):
    """
    """
    @contextmanager
    def _session(self, session=None):
        """
        """
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

    def __init__(self, pathname):
        """
        """
        self._persistenceFile = pathname
        self.engine = create_engine("sqlite://", echo=False, module=sqlite)
        self.engine.execute("select 1").scalar()
        self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
        Base.metadata.drop_all(self.engine, checkfirst=True)

        if os.path.exists(self._persistenceFile):
            self._restore()
            # TO DO: migrate schema
        else:
            Base.metadata.create_all(self.engine)

    def shutdown(self):
        """
        """
        self._persist()

    def addMovieStream(self, movieRecord, streamLocation):
        """
        """
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
        """
        """
        compressor = bz2.BZ2Compressor()
        connection = self.engine.raw_connection()
        fp = open(self._persistenceFile, "wb")
        try:
            for line in connection.iterdump():
                fp.write(compressor.compress(line.encode("iso-8859-1")))
            fp.write(compressor.flush())
        finally:
            fp.close()
            connection.close()

    def _restore(self):
        """
        """
        connection = self.engine.raw_connection()
        try:
            with open(self._persistenceFile, "rb") as fp:
                connection.cursor().executescript(bz2.decompress(fp.read()).decode("iso-8859-1"))
        except:
            raise
        else:
            connection.commit()
        finally:
            connection.close()
