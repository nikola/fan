# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import json
from contextlib import contextmanager
from sqlite3 import dbapi2 as sqlite

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.orm.exc import NoResultFound

from settings import EXE_PATH
from models.common import Base, GUID, createNamedTuple, createUuid # , DictSerializable
from models.streams import Stream
# from models.genres import Genre
from models.movies import Movie
from models.images import Image
from models.localizations import Localization
# from models.tracks import Track


# TODO: use named tuples ?
#   https://docs.python.org/2/library/collections.html#collections.namedtuple


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

        # if not DEBUG and os.path.exists(os.path.join(getAppStoragePathname(), 'data.accdb')):
        #     self._restore()
        #     # TODO: migrate schema by dumping all data to JSON, then drop_all, then read JSON back in
        #       which might not work for images !!!
        # else:
        # Base.metadata.drop_all(self.engine, checkfirst=True)
        Base.metadata.create_all(self.engine, checkfirst=True)

        if cleanUp:
            with self._session() as session:
                session.query(Movie).filter(Movie.isPosterDownloading == True).update({'isPosterDownloading': False})
                session.query(Movie).filter(Movie.isBackdropDownloading == True).update({'isBackdropDownloading': False})


    def shutdown(self):
        self.engine.dispose()


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
                    localization = Localization(
                        locale = movieRecord['locale'],
                        title = movieRecord['title'],
                        storyline = movieRecord['storyline'],
                    )
                    movie = Movie(**movieRecord)
                    localization.movie = movie
                    session.add_all([movie, localization])

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


    def getUnscaledPosterImage(self):
        with self._session() as session:
            try:
                image = session.query(Image).filter(Image.isScaled == False, Image.imageType == 'Poster').first()
            except NoResultFound:
                return None
            else:
                if image is not None:
                    return image


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


    def getImageByUuid(self, identifier, imageType='Poster', width=1920):
        with self._session() as session:
            try:
                image = session.query(Image).filter(Image.movie.has(Movie.uuid == identifier), Image.imageType == imageType, Image.width == width).one()
            except NoResultFound:
                return None
            else:
                if image is not None:
                    return image
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

                return image # TODO: correct return type ?


    def getAllMoviesAsJson(self):
        with self._session() as session:
            movieList = []
            for movie in session.query(Movie, Localization).filter(Movie.id == Localization.movieId).values(Movie.uuid, Movie.titleOriginal, Localization.title, Movie.releaseYear, Movie.runtime, Localization.storyline, Movie.rating):
                movieList.append({
                    'uuid': movie[0],
                    'titleOriginal': movie[1],
                    'titleLocalized': movie[2],
                    'releaseYear': movie[3],
                    'runtime': movie[4],
                    'storyline': movie[5],
                    'rating': movie[6],
                })
            return json.dumps(movieList, separators=(',',':'))


    def getMovieAsJson(self, identifier):
        with self._session() as session:
            try:
                movie = list(session.query(Movie, Localization).filter(Movie.uuid == identifier, Movie.id == Localization.movieId).values(Movie.uuid, Movie.titleOriginal, Localization.title, Movie.releaseYear, Movie.runtime, Localization.storyline, Movie.rating))[0]
            except NoResultFound:
                return None
            else:
                return json.dumps({
                    'uuid': movie[0],
                    'titleOriginal': movie[1],
                    'titleLocalized': movie[2],
                    'releaseYear': movie[3],
                    'runtime': movie[4],
                    'storyline': movie[5],
                    'rating': movie[6],
                }, separators=(',',':'))


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
