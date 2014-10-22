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

import os
import json
from contextlib import contextmanager
from operator import itemgetter
from sqlite3 import dbapi2 as sqlite

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from settings import EXE_PATH
from models.common import Base, createNamedTuple
from models.movies import Movie
from models.localizations import Localization
from models.compilations import Compilation
from models.streams import Stream


# TODO: use named tuples ?
#   https://docs.python.org/2/library/collections.html#collections.namedtuple


def initialize():
    StreamManager(cleanUp=True).shutdown()


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


    def __init__(self, cleanUp=False):
        location = 'sqlite:///' + (EXE_PATH + ':b582b94058ff4bbea424c5af17f68586').replace('\\', r'\\\\')

        self.engine = create_engine(location, echo=False, module=sqlite)
        self.engine.execute('select 1').scalar()
        self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)

        Base.metadata.create_all(self.engine, checkfirst=True)


    def shutdown(self):
        self.engine.dispose()


    def purge(self):
        with self._session() as session:
            session.query(Localization).delete()
            session.query(Stream).delete()
            session.query(Movie).delete()

            session.commit()


    def deleteMovie(self, identifier):
        with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.id == identifier).one()
            except NoResultFound:
                return None
            else:
                movie.delete()
                session.commit()


    def getMovieTitleById(self, identifier):
        with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.id == identifier).one()
            except NoResultFound:
                return None
            else:
                return '%s (%d)' % (movie.titleOriginal, movie.releaseYear)


    def addMovieStream(self, movieDict, streamLocation, version):
        with self._session() as session:
            if streamLocation is not None:
                try:
                    streamObject = session.query(Stream).filter_by(location=streamLocation).one()
                except NoResultFound:
                    streamFormat = 'Matroska' if streamLocation.lower().endswith('.mkv') else 'BD'
                    streamObject = Stream(
                        format = streamFormat,
                        location = streamLocation,
                        space = version[0][::-1],
                        resolution = version[1],
                        edit = version[2],
                    )
                    session.add(streamObject)
            else:
                streamObject = None

            if movieDict is not None:
                try:
                    movieObject = session.query(Movie).filter("titleOriginal=:title and releaseYear=:year").params(title=movieDict["titleOriginal"], year=movieDict["releaseYear"]).one()
                except NoResultFound:
                    localizationObject = Localization(
                        locale = movieDict['locale'],
                        title = movieDict['title'],
                        storyline = movieDict['storyline'],
                    )
                    if not streamLocation.startswith('\\\\03cab2fbe3354d838578b09178ac2a1a\\fan\\'):
                        movieDict['streamless'] = False

                    movieObject = Movie(**movieDict)

                    if movieDict['compilationId'] is not None:
                        try:
                            compilationObject = session.query(Compilation).filter(Compilation.id == movieDict['compilationId']).one()
                        except NoResultFound:
                            compilationObject = Compilation(
                                id = movieDict['compilationId'],
                                name = movieDict['compilationName']
                            )
                            session.add(compilationObject)

                        movieObject.compilation = compilationObject

                    localizationObject.movie = movieObject
                    session.add_all([movieObject, localizationObject])

                if streamObject is not None:
                    movieObject.streams.append(streamObject)
            else:
                movieObject = None

            session.commit()

            if movieObject is not None:
                return movieObject.id


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


    def getAllMoviesAsJson(self):
        with self._session() as session:
            compilationNameById = {}
            compilationMovieCountById = {}
            for compilation in session.query(Compilation).all():
                compilationNameById[compilation.id] = compilation.name
                compilationMovieCountById[compilation.id] = len(compilation.movies)

            movieList = []
            for movie, localization in session.query(Movie, Localization).filter(Movie.id == Localization.movieId, Localization.locale == 'en').group_by(Movie.id).distinct():
                if movie.streamless or any([True for stream in movie.streams if os.path.exists(stream.location)]):
                    movieList.append({
                        'id': movie.id,
                        'titleOriginal': movie.titleOriginal,
                        'titleLocalized': localization.title,
                        'releaseYear': movie.releaseYear,
                        'runtime': movie.runtime,
                        'storyline': localization.storyline,
                        'rating': movie.rating,
                        'genres': movie.genres,
                        'budget': movie.budget,
                        'trailer': movie.idYoutubeTrailer,

                        'keyPoster': movie.keyPoster,
                        'primaryPosterColor': movie.primaryColorPoster,
                        'keyBackdrop': movie.keyBackdrop,
                        'isBackdropCached': movie.isBackdropCached,

                        'streamless': movie.streamless,

                        'compilation': compilationNameById.get(movie.compilationId),
                        'isCompiled': compilationMovieCountById.get(movie.compilationId, 0) > 1,
                    })
            return json.dumps(movieList, separators=(',',':'))


    def getMovieAsJson(self, identifier):
        with self._session() as session:
            try:
                movie = list(session.query(Movie, Localization).filter(Movie.id == identifier, Movie.id == Localization.movieId, Localization.locale == 'en').distinct() \
                    .values(Movie.id, Movie.titleOriginal, Localization.title, Movie.releaseYear, Movie.runtime, Localization.storyline, Movie.rating, Movie.genres, Movie.budget, Movie.idYoutubeTrailer, Movie.streamless,  Movie.keyPoster, Movie.keyBackdrop, Movie.primaryColorPoster))[0]
            except NoResultFound:
                return None
            else:
                record = {
                    'id': movie[0],
                    'titleOriginal': movie[1],
                    'titleLocalized': movie[2],
                    'releaseYear': movie[3],
                    'runtime': movie[4],
                    'storyline': movie[5],
                    'rating': movie[6],
                    'genres': movie[7],
                    'budget': movie[8],
                    'trailer': movie[9],
                    'streamless': movie[10],
                    'keyPoster': movie[11],
                    'keyBackdrop': movie[12],
                    'isBackdropCached': 0,
                    'primaryPosterColor': movie[13],
                }

                return json.dumps(record, separators=(',',':'))


    def getStreamLocationById(self, identifier):
        with self._session() as session:
            try:
                stream = session.query(Stream).filter(Stream.id == identifier).one()
            except NoResultFound:
                return None
            else:
                return stream.location


    def getVersionsByMovieId(self, identifier):
        with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.id == identifier).one()
            except NoResultFound:
                return None
            else:
                containers = []
                for stream in movie.streams:
                    containers.append({
                        'stream': stream.id,
                        'format': stream.format,
                        'space': stream.space[::-1],
                        'resolution': stream.resolution,
                        'edit': stream.edit,
                    })

                containers = sorted(containers, key=itemgetter('resolution'))

                if all(version.get('space') == '2D' for version in containers):
                    for version in containers:
                        del version['space']

                if all(version.get('edit') == 'Theatrical Cut' for version in containers):
                    for version in containers:
                        del version['edit']

                if all(version.get('format') == 'Matroska' for version in containers):
                    for version in containers:
                        del version['format']

                versions = []
                for container in containers:
                    versions.append([', '.join(filter(None, [
                        container.get('edit'),
                        container.get('resolution'),
                        container.get('space'),
                        container.get('format'),
                    ])), container.get('stream')])

                return versions


    def updatePosterColorByMovieId(self, identifier, color):
        with self._session() as session:
            session.query(Movie).filter(Movie.id == identifier).update({'primaryColorPoster': color}) # , synchronize_session=False)


    def setBackdropCachedByMovieId(self, identifier):
        with self._session() as session:
            session.query(Movie).filter(Movie.id == identifier).update({'isBackdropCached': True}) # , synchronize_session=False)


    # def getUnidentifiedTracksMovie(self):
    #     with self._session() as session:
    #         try:
    #             movie = session.query(Movie).join(Track).group_by(Movie.id).having(~Movie.tracks.any()).first()
    #         except NoResultFound:
    #             return None
    #         else:
    #             if movie is not None:
    #                 return movie.uuid
