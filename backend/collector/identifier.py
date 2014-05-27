# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import time
import httplib
import socket

import tmdb3 as themoviedb
from babel import Locale as BabelLocale

from settings.collector import THEMOVIEDB_API_KEY
from utils.win32 import getAppStoragePathname



def identifyMovieByTitleYear(language, territory, title, year):
    socket.setdefaulttimeout(5)

    themoviedb.set_key(THEMOVIEDB_API_KEY)
    themoviedb.set_cache('null') # filename=os.path.join(getAppStoragePathname(), 'tmdb3.cache'))


    """


    https://github.com/ahmetabdi/themoviedb



    id = Datapoint('id', initarg=1)
    title = Datapoint('title')
    originaltitle = Datapoint('original_title')
    tagline = Datapoint('tagline')
    overview = Datapoint('overview')
    runtime = Datapoint('runtime')
    budget = Datapoint('budget')
    revenue = Datapoint('revenue')
    releasedate = Datapoint('release_date', handler=process_date)
    homepage = Datapoint('homepage')
    imdb = Datapoint('imdb_id')

    backdrop = Datapoint('backdrop_path', handler=Backdrop,
                         raw=False, default=None)
    poster = Datapoint('poster_path', handler=Poster,
                       raw=False, default=None)

    popularity = Datapoint('popularity')
    userrating = Datapoint('vote_average')
    votes = Datapoint('vote_count')

    adult = Datapoint('adult')
    collection = Datapoint('belongs_to_collection', handler=lambda x: \
                                                        Collection(raw=x))
    genres = Datalist('genres', handler=Genre)
    studios = Datalist('production_companies', handler=Studio)
    countries = Datalist('production_countries', handler=Country)
    languages = Datalist('spoken_languages', handler=Language)
    """
    record = None

    try:
        # Search movie by title and year. Omit year in retry.
        locale = themoviedb.locales.Locale(language, territory, encoding='iso-8859-1')
        results = themoviedb.searchMovie(query=title.encode('utf-8'), locale=locale, year=year)
        if not len(results):
            time.sleep(0.35)
            results = themoviedb.searchMovie(query=title.encode('utf-8'), locale=locale)

        if len(results):
            result = results[0]
            record = dict(
                titleOriginal = result.originaltitle,
                titleLocal    = result.title,
                releaseYear   = result.releasedate.year,
                urlBackdrop   = result.backdrop.geturl(),
                urlPoster     = result.poster.geturl(),
                idImdb        = result.imdb,
                idTheMovieDb  = result.id,
                taglineLocal  = result.tagline,
                overviewLocal = result.overview,
                runtime       = result.runtime or None,
                budget        = result.budget or None,
                revenue       = result.revenue or None,
                homepage      = result.homepage,
                locale        = BabelLocale(language, territory),
            )
    except (themoviedb.TMDBHTTPError, httplib.BadStatusLine, socket.timeout):
        print "error"

    return record
