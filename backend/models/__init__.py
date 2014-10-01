# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
# import logging
import json
from contextlib import contextmanager
from sqlite3 import dbapi2 as sqlite

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from settings import EXE_PATH #, LOG_CONFIG
# from utils.fs import getLogFileHandler
from models.common import Base, GUID, createNamedTuple, createUuid
from models.streams import Stream
from models.movies import Movie
from models.images import Image
from models.localizations import Localization
from models.compilations import Compilation


# logging.basicConfig(**LOG_CONFIG)
# logger = logging.getLogger('orm')
# logger.propagate = False
# logger.addHandler(getLogFileHandler('orm'))


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

        # if cleanUp:
        #     with self._session() as session:
        #         session.query(Movie).filter(Movie.isPosterDownloading == True).update({'isPosterDownloading': False})
        #         session.query(Movie).filter(Movie.isBackdropDownloading == True).update({'isBackdropDownloading': False})


    def shutdown(self):
        self.engine.dispose()


    def purge(self):
        with self._session() as session:
            session.query(Localization).delete()
            session.query(Image).delete()
            session.query(Stream).delete()
            session.query(Movie).delete()

            session.commit()


    def deleteMovie(self, identifier):
        with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.uuid == identifier).one()
            except NoResultFound:
                return None
            else:
                movie.delete()
                session.commit()


    def getMovieByUuid(self, identifier):
        with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.uuid == identifier).one()
            except NoResultFound:
                return None
            else:
                return movie


    def getMovieTitleById(self, identifier):
        with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.id == identifier).one()
            except NoResultFound:
                return None
            else:
                return '%s (%d)' % (movie.titleOriginal, movie.releaseYear)


    def getMovieTitleByUuid(self, identifier):
        with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.uuid == identifier).one()
            except NoResultFound:
                return None
            else:
                return '%s (%d)' % (movie.titleOriginal, movie.releaseYear)


    def addMovieStream(self, movieDict, streamLocation):
        with self._session() as session:
            if streamLocation is not None:
                try:
                    streamObject = session.query(Stream).filter_by(location=streamLocation).one()
                except NoResultFound:
                    streamFormat = 'Matroska' if streamLocation.lower().endswith('.mkv') else 'BD'
                    streamObject = Stream(
                        format = streamFormat,
                        location = streamLocation,
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
                    if not streamLocation.startswith('\\\\03cab2fbe3354d838578b09178ac2a1a\\ka-BOOM\\'):
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
                return movieObject.uuid


    def isStreamKnown(self, streamLocation):
        with self._session() as session:
            try:
                session.query(Stream).filter(Stream.location == streamLocation).one()
            except NoResultFound:
                return False
            else:
                return True


    def getCompilationById(self, identifier):
        with self._session() as session:
            try:
                compilation = session.query(Compilation).filter(Compilation.id == identifier).one()
            except NoResultFound:
                return None
            else:
                return compilation


    def getMovieFromStreamLocation(self, streamLocation):
        with self._session() as session:
            try:
                stream = session.query(Stream).filter(Stream.location == streamLocation).one()
            except NoResultFound:
                return None
            else:
                return stream.movie


    def getUnscaledPosterImage(self):
        with self._session() as session:
            try:
                image = session.query(Image).filter(Image.isScaled == False, Image.imageType == 'Poster', Image.urlOriginal != None).first()
            except NoResultFound:
                return None, None
            else:
                if image is not None:
                    return image.movie.uuid, image.urlOriginal
                else:
                    return None, None


    def getMissingBackdropMovieUuid(self):
        with self._session() as session:
            try:
                movie = session.query(Movie).join(Image).filter(Movie.images.any(Image.imageType == 'Poster')).group_by(Movie.id).having(func.count(Movie.images) == 1).first()
            except NoResultFound:
                return None
            else:
                if movie is not None:
                    return movie.uuid


    def startPosterDownload(self, identifier):
         with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.uuid == identifier).one()
            except NoResultFound:
                pass
            else:
                movie.isPosterDownloading = True
                session.commit()


    def isPosterDownloading(self, identifier):
         with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.uuid == identifier).one()
            except NoResultFound:
                return None
            else:
                return movie.isPosterDownloading


    def endPosterDownload(self, identifier):
         with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.uuid == identifier).one()
            except NoResultFound:
                pass
            else:
                movie.isPosterDownloading = False
                session.commit()


    def startBackdropDownload(self, identifier):
         with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.uuid == identifier).one()
            except NoResultFound:
                pass
            else:
                movie.isBackdropDownloading = True
                session.commit()


    def isBackdropDownloading(self, identifier):
         with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.uuid == identifier).one()
            except NoResultFound:
                return None
            else:
                return movie.isBackdropDownloading


    def endBackdropDownload(self, identifier):
         with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.uuid == identifier).one()
            except NoResultFound:
                pass
            else:
                movie.isBackdropDownloading = False
                session.commit()


    def isImageAvailable(self, identifier, imageType, width):
        with self._session() as session:
            try:
                session.query(Image).filter(Image.movie.has(Movie.uuid == identifier), Image.imageType == imageType, Image.width == width).one()
            except NoResultFound:
                return False
            else:
                return True


    def getImageMetadataByUuid(self, identifier, imageType, width):
        with self._session() as session:
            try:
                image = session.query(Image).filter(Image.movie.has(Movie.uuid == identifier), Image.imageType == imageType, Image.width == width).one()
            except NoResultFound:
                return None, None
            else:
                if image is not None:
                    return image.modified, image.isScaled
                else:
                    return None, None


    def getImageBlobByUuid(self, identifier, imageType, width):
        with self._session() as session:
            try:
                image = session.query(Image).filter(Image.movie.has(Movie.uuid == identifier), Image.imageType == imageType, Image.width == width).one()
            except NoResultFound:
                return None
            else:
                if image is not None:
                    return image.blob
                else:
                    return None


    def saveImageData(self, identifier, width, blob, isScaled=False, imageType='Poster', imageFormat='JPEG', urlOriginal=None):
        with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.uuid == identifier).one()
            except NoResultFound:
                return None
            else:
                try:
                    image = session.query(Image).join(Movie).filter(Movie.uuid == identifier, Movie.id == Image.movieId, Image.imageType == imageType, Image.width == width).one()
                except MultipleResultsFound:
                    # logger.error('Multiple poster images of the same size and type found for movie "%s".', self.getMovieTitleByUuid(identifier))
                    image = session.query(Image).join(Movie).filter(Movie.uuid == identifier, Movie.id == Image.movieId, Image.imageType == imageType, Image.width == width).first()
                except NoResultFound:
                    image = Image(
                        imageType = imageType,
                        imageFormat = imageFormat,
                        movie = movie,
                        width = width,
                        isScaled = isScaled,
                        blob = blob,
                        urlOriginal = urlOriginal,
                    )
                else:
                    image.blob = blob
                    image.isScaled = isScaled
                    image.imageFormat = imageFormat

                session.add(image)
                session.commit()

                return image.modified


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
                    try:
                        primaryPosterColor = list(session.query(Image).filter(Image.movieId == movie.id).values(Image.primaryColor))[0][0]
                    except (NoResultFound, IndexError):
                        primaryPosterColor = None

                    movieList.append({
                        'uuid': movie.uuid,
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
                        'primaryPosterColor': primaryPosterColor,
                        'keyBackdrop': movie.keyBackdrop,
                        'isBackdropCached': movie.isBackdropCached,

                        # 'idBackdrop': movie.urlBackdrop.replace('/', '').replace('.jpg', ''),
                        # 'idPoster': movie.urlPoster.replace('/', '').replace('.jpg', ''),
                        'streamless': movie.streamless,

                        'compilation': compilationNameById.get(movie.compilationId),
                        'isCompiled': compilationMovieCountById.get(movie.compilationId, 0),
                    })
            return json.dumps(movieList, separators=(',',':'))


    def getMovieAsJson(self, identifier):
        with self._session() as session:
            try:
                movie = list(session.query(Movie, Localization).filter(Movie.uuid == identifier, Movie.id == Localization.movieId, Localization.locale == 'en').distinct() \
                    .values(Movie.uuid, Movie.titleOriginal, Localization.title, Movie.releaseYear, Movie.runtime, Localization.storyline, Movie.rating, Movie.genres, Movie.budget, Movie.idYoutubeTrailer, Movie.streamless,  Movie.keyPoster, Movie.keyBackdrop))[0]
            except NoResultFound:
                return None
            else:
                record = {
                    'uuid': movie[0],
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
                }
                try:
                    poster = session.query(Image).join(Movie).filter(Image.imageType == 'Poster', Image.movie.has(Movie.uuid == identifier)).first()
                except NoResultFound:
                    pass
                else:
                    if poster is not None and poster.primaryColor:
                        record['primaryPosterColor'] = poster.primaryColor

                return json.dumps(record, separators=(',',':'))


    def getStreamLocationByMovie(self, identifier):
        with self._session() as session:
            try:
                movie = session.query(Movie).filter(Movie.uuid == identifier).one()
            except NoResultFound:
                return None
            else:
                return movie.streams[0].location


    def updatePosterColorByMovieUuid(self, identifier, color):
        with self._session() as session:
            session.query(Image).join(Movie).filter(Image.imageType == 'Poster', Image.movie.has(Movie.uuid == identifier)).update({'primaryColor': color}, synchronize_session=False)


    # def getUnidentifiedTracksMovie(self):
    #     with self._session() as session:
    #         try:
    #             movie = session.query(Movie).join(Track).group_by(Movie.id).having(~Movie.tracks.any()).first()
    #         except NoResultFound:
    #             return None
    #         else:
    #             if movie is not None:
    #                 return movie.uuid



    """


    TODO: migrate schema by dumping all data to JSON, then drop_all, then read JSON back in
          which might not work for images !!!

    Base.metadata.drop_all(self.engine, checkfirst=True)

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
    """
