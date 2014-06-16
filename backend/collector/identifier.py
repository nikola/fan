# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import datetime

from settings.collector import THEMOVIEDB_API_KEY
from utils.net import makeThrottledGetRequest


def identifyMovieByTitleYear(language, territory, title, year):
    record = None

    url = 'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': THEMOVIEDB_API_KEY,
        'query': title.encode('utf-8'),
        'page': 1,
        'language': 'en',
        'include_adult': False,
        'primary_release_year': year, # TODO: change to use year instead so that Planet Earth is identified correctly ???
    }
    response = makeThrottledGetRequest(url, params).json()

    if response['total_results'] == 0:
        print 'movie %s not found at tmdb, retrying' % title
        del params['primary_release_year']
        response = makeThrottledGetRequest(url, params).json()

    # TODO: retry with different query mode parameter, e.g. for Aeon Flux

    if response['total_results'] > 0:
        movieId = response['results'][0]['id']
        print 'movie %s found at tmdb, id = %d' % (title, movieId)

        url = 'https://api.themoviedb.org/3/movie/%d' % movieId
        params = {
            'api_key': THEMOVIEDB_API_KEY,
            'language': 'en',
        }
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
