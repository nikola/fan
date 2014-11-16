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
import copy
from contextlib import contextmanager
from operator import itemgetter
from sqlite3 import dbapi2 as sqlite

import simplejson as json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from settings import APP_STORAGE_PATH
from models.common import Base, createNamedTuple
from models.movies import Movie
from models.localizations import Localization
from models.compilations import Compilation
from models.streams import Stream
from models.certifications import Certification
from models.genres import GenresString


# TODO: use named tuples ?
#   https://docs.python.org/2/library/collections.html#collections.namedtuple


def initialize(profile):
    StreamManager(profile, cleanUp=True).shutdown()


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


    def __init__(self, profile, cleanUp=False):
        location = 'sqlite:///' + os.path.join(APP_STORAGE_PATH, profile + '.data', 'fan-db.sqlite').replace('\\', r'\\\\')

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
                movieDict = copy.deepcopy(movieDict)

                try:
                    movieObject = session.query(Movie).filter('titleOriginal=:title and releaseYear=:year').params(title=movieDict['titleOriginal'], year=movieDict['releaseYear']).one()
                except NoResultFound:
                    if movieDict['certificationDict'].has_key(movieDict['country']):
                        certificationObject = Certification(
                            country = movieDict['country'],
                            certification = movieDict['certificationDict'][movieDict['country']] or u'',
                        )
                    else:
                        certificationObject = Certification(
                            country = movieDict['country'],
                            certification = u'',
                        )
                    genresObject = GenresString(
                        country = movieDict['country'],
                        genresAsString = movieDict['genres'],
                    )
                    del movieDict['genres']

                    localizationObject = Localization(
                        locale = movieDict['language'],
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
                                name = movieDict['compilationName'],
                                language = movieDict['language'],
                            )
                            session.add(compilationObject)

                        movieObject.compilation = compilationObject

                    certificationObject.movie = movieObject
                    genresObject.movie = movieObject
                    localizationObject.movie = movieObject
                    session.add_all([movieObject, localizationObject])

                if streamObject is not None:
                    movieObject.streams.append(streamObject)
            else:
                movieObject = None

            session.commit()

            return movieObject.id if movieObject is not None else None


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


    def getAllMoviesAsJson(self, language, country):
        with self._session() as session:
            compilationNameById = {}
            compilationMovieCountById = {}
            for compilation in session.query(Compilation).filter(Compilation.language == language):
                compilationNameById[compilation.id] = compilation.name
                compilationMovieCountById[compilation.id] = len(compilation.movies)

            movieList = []
            for movie, localization, certification, genreObject in session.query(Movie, Localization, Certification, GenresString).filter(Movie.id == Localization.movieId, Movie.id == Certification.movieId, Movie.id == GenresString.movieId, Localization.locale == language, Certification.country == country, GenresString.country == country).group_by(Movie.id).distinct():
                if movie.streamless or any([True for stream in movie.streams if os.path.exists(stream.location)]):
                    movieList.append({
                        'id': movie.id,
                        'titleOriginal': movie.titleOriginal,
                        'titleLocalized': localization.title,
                        'releaseYear': movie.releaseYear,
                        'runtime': movie.runtime,
                        'storyline': localization.storyline,
                        'rating': movie.rating,
                        'genres': genreObject.genresAsString,
                        'budget': movie.budget,
                        'trailer': movie.idYoutubeTrailer,
                        'certification': certification.certification,

                        'keyPoster': movie.keyPoster,
                        'primaryPosterColor': movie.primaryColorPoster,
                        'keyBackdrop': movie.keyBackdrop,
                        'isBackdropCached': movie.isBackdropCached,

                        'streamless': movie.streamless,

                        'compilation': compilationNameById.get(movie.compilationId),
                        'isCompiled': compilationMovieCountById.get(movie.compilationId, 0) > 1,
                    })
            return json.dumps(movieList, separators=(',',':'))


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
                    if os.path.exists(stream.location):
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

                if all(version.get('resolution') == '1080p24' for version in containers) or len(containers) == 1:
                    for version in containers:
                        del version['resolution']

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
