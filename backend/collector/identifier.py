# coding: utf-8
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
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

# import os
import time
# import httplib
# import socket
import datetime
import logging

# import requests
# import tmdb3 as themoviedb
# from babel import Locale as BabelLocale

from settings.collector import THEMOVIEDB_API_KEY
from utils.net import makeThrottledGetRequest
# from utils.win32 import getAppStoragePathname

# IMAGE_BASE_URL = None

# LAST_TMDB_ACCESS = time.clock()

# Don't be too chatty on the console.
# REQUESTS_LOGGER = logging.getLogger('urllib3')
# REQUESTS_LOGGER.setLevel(logging.CRITICAL)
# REQUESTS_LOGGER = logging.getLogger('requests.packages.urllib3')
# REQUESTS_LOGGER.setLevel(logging.CRITICAL)
# REQUESTS_LOGGER.propagate = True


def getImageBaseUrl():
    print 'called getImageBaseUrl()'

    # global IMAGE_BASE_URL
    # if IMAGE_BASE_URL is None:
    url = 'https://api.themoviedb.org/3/configuration'
    # response = requests.get(url, params={'api_key': THEMOVIEDB_API_KEY}, timeout=5)
    response = makeThrottledGetRequest(url, params={'api_key': THEMOVIEDB_API_KEY})
    configuration = response.json()
    return configuration.get('images').get('secure_base_url')
    # return IMAGE_BASE_URL


def identifyMovieByTitleYear(language, territory, title, year):
    record = None

    # try:
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': THEMOVIEDB_API_KEY,
        'query': title.encode('utf-8'),
        'page': 1,
        'language': 'en',
        'include_adult': False,
        'primary_release_year': year,
    }
    # response = requests.get(url, params=params, timeout=5).json()
    response = makeThrottledGetRequest(url, params).json()
    if response['total_results'] == 0:
        print 'movie %s not found at tmdb, retrying' % title
        del params['primary_release_year']
        # time.sleep(0.35)
        # response = requests.get(url, params=params, timeout=5).json()
        response = makeThrottledGetRequest(url, params).json()
    # time.sleep(0.35)

    # global LAST_TMDB_ACCESS
    # print 'last TMDB access:', LAST_TMDB_ACCESS
    # LAST_TMDB_ACCESS = time.clock()

    if response['total_results'] > 0:
        movieId = response['results'][0]['id']
        print 'movie %s found at tmdb, id = %d' % (title, movieId)

        url = 'https://api.themoviedb.org/3/movie/%d' % movieId
        params = {
            'api_key': THEMOVIEDB_API_KEY,
            'language': 'en',
        }
        # response = requests.get(url, params=params, timeout=5).json()
        response = makeThrottledGetRequest(url, params).json()

        record = dict(
                idTheMovieDb  = movieId,
                titleOriginal = response['original_title'],
                titleLocal    = response['title'],
                releaseYear   = datetime.datetime.strptime(response['release_date'], '%Y-%m-%d').year,
                urlBackdrop   = response['backdrop_path'],
                urlPoster     = response['poster_path'],
                idImdb        = response['imdb_id'],
                taglineLocal  = response['tagline'],
                overview      = response['overview'],
                runtime       = response['runtime'] or None,
                budget        = response['budget'] or None,
                revenue       = response['revenue'] or None,
                homepage      = response['homepage'],
                # locale        = BabelLocale(language, territory),
            )

    return record
