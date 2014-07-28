# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import re
import datetime
import logging
from simplejson import JSONDecodeError

from settings import LOG_CONFIG
from utils.net import makeThrottledGetRequest, makeUnthrottledGetRequest
from utils.fs import getLogFileHandler
from identifier.fixture import TRAILERS_HD


THEMOVIEDB_API_KEY = 'ef89c0a371440a7226e1be2ddfe84318'

STREAM_SIZE_THRESHOLD = 1024 * 1024 * 10 # 10 MiB

# Compiled regular expressions.
RE_CUT_INDICATOR_1 = re.compile(r"(([ \.\(](extended|final|theatrical|international|unrated|director[ \.']?s?))+([ \.]cut|[ \.]edition|[ \.]version|$))", re.I)
RE_SEARCH_YEAR = re.compile(r"(?<!^)((19|20)\d{2})[a-z0-9\.\-\) '\[\]]*$", re.I)
RE_SEARCH_HEIGHT = re.compile(r"(?<!^)((72|108)0p?)[a-z0-9\.\-\) '\[\]]*$", re.I)
RE_SAMPLE_DIR = re.compile(r'\\!?sample$', re.I)
RE_SAMPLE_FILE = re.compile(r'sample', re.I)
RE_SEP_CHARS = re.compile(r'[\(\[,\-]')
RE_ROMAN_LEADS = re.compile(r'^X?(IX|IV|V?I{0,3}) ')
RE_UNDERSCORE_LEAD = re.compile(r'^_ +')
RE_DOT_SEPARATOR = re.compile(r'\.(?!0)')
RE_UNDERSCORE_SEPARATOR = re.compile(r'_')
RE_MULTI_ANGLE = re.compile(r'\d[\- ]*in[\- ]*\d')
RE_EDITION_IND = re.compile(r'(?<= )(special edition|remastered|european version|hybrid|(2|3)d source|3d half sbs|half sbs|3d|open matte|tv aspect ratio)(?= |$)', re.I)
RE_SOURCE_IND = re.compile(r'(?<= )(blu ?ray|hd dvd|mkv)(?= |$)', re.I)
RE_MULTI_SPACE = re.compile('  +')
RE_DIR_DRIVE = re.compile('"[a-z]\:\\\\', re.I)
RE_DIR_TAIL = re.compile(r'(?<=\\)[^\\]*$', re.I)


logging.basicConfig(**LOG_CONFIG)
logger = logging.getLogger('tmdb')
logger.addHandler(getLogFileHandler('tmdb'))


def getImageConfiguration():
    response = makeThrottledGetRequest('https://api.themoviedb.org/3/configuration', params={'api_key': THEMOVIEDB_API_KEY})
    configuration = response.json()

    sizes = configuration.get('images').get('poster_sizes')
    if 'original' in sizes: sizes.remove('original')
    closestWidth = min(sizes, key=lambda x: abs(int(x[1:]) - 300))
    if int(closestWidth[1:]) < 300:
        closestWidth = sizes[sizes.index(closestWidth) + 1]

    return configuration.get('images').get('secure_base_url'), closestWidth


def getMoviePathnames(sources):
    for source in sources:
        for root, dirs, files in os.walk(unicode(source.get('pathname'))):
            dirname = RE_DIR_DRIVE.sub('', root)

            # Skip directories which contain no movie files.
            if any([True for name in files if name.endswith(('.mkv', '.MKV'))]) and RE_SAMPLE_DIR.search(dirname) is None:
                # Ignore parent directory for the time being.
                if dirname.find('\\') != -1:
                    dirname = RE_DIR_TAIL.search(dirname).group()

                # Remove leading underscore.
                dirname = RE_UNDERSCORE_LEAD.sub('', dirname).strip()

                # Only files with actual movie content.
                if dirname.lower() != 'extras':
                    streams = getOnlyStreams(root, files)

                    if len(streams):
                        if re.compile(r'^\\\\\?\\UNC\\\w+\\\w+$').search(root) is None:
                            basedataFromDir = getBaseDataFromPathname(dirname)
                        else:
                            basedataFromDir = {'title': None, 'year': None}

                        for filename in streams:
                            basedataFromStream = getBaseDataFromPathname(filename)

                            streamLocation = os.path.join(root, filename)

                            yield (streamLocation, basedataFromStream, basedataFromDir)


def getOnlyStreams(root, files):
    streams = []
    for filename in files:
        if not filename.lower().endswith('.mkv'):
            continue
        elif RE_SAMPLE_FILE.search(filename) is not None:
            continue
        elif os.stat(os.path.join(root, filename)).st_size < STREAM_SIZE_THRESHOLD:
            continue
        else:
            streams.append(filename)
    return streams


def getBaseDataFromPathname(pathname):
    releaseYear = None # 2014

    rawTitle = pathname

    # Remove separation characters.
    rawTitle = RE_SEP_CHARS.sub(' ', rawTitle)

    searchReleaseYear = RE_SEARCH_YEAR.search(rawTitle)
    if searchReleaseYear is not None:
        releaseYear = int(searchReleaseYear.groups()[0])
        extractedTitle = re.search('^(.*)(?=%s)' % releaseYear, rawTitle).groups()[0]
    else:
        searchVideoHeight = RE_SEARCH_HEIGHT.search(rawTitle)
        if searchVideoHeight is not None:
            extractedTitle = re.search('^(.*)(?=%s)' % searchVideoHeight.groups()[0], rawTitle).groups()[0]
        else:
            extractedTitle = rawTitle

    # Convert dots to spaces (except when followed by a zero).
    extractedTitle = RE_DOT_SEPARATOR.sub(' ', extractedTitle).strip()

    # Convert underscores to spaces.
    extractedTitle = RE_UNDERSCORE_SEPARATOR.sub(' ', extractedTitle).strip()

    # Collapse multiple spaces.
    extractedTitle = RE_MULTI_SPACE.sub(' ', extractedTitle).strip()

    # Remove superfluous multi-angle indicators.
    extractedTitle = RE_MULTI_ANGLE.sub('', extractedTitle).strip()

    # Remove superfluous source indicators.
    extractedTitle = RE_SOURCE_IND.sub('', extractedTitle).strip()

    # Remove superfluous edition indicators.
    extractedTitle = RE_EDITION_IND.sub(' ', extractedTitle).strip()

    # Collapse multiple spaces.
    extractedTitle = RE_MULTI_SPACE.sub(' ', extractedTitle).strip()

    # Remove cut indicator.
    extractedTitle = RE_CUT_INDICATOR_1.sub('', extractedTitle).strip()
    extractedTitle = re.sub(r'(?<=%s[ \.])(extended|unrated)(?=[ \.])' % releaseYear, '', extractedTitle, 0, re.I).strip()

    # Remove leading Roman numerals.
    extractedTitle = RE_ROMAN_LEADS.sub('', extractedTitle).strip()

    # Remove extraneous whitespace.
    extractedTitle = RE_MULTI_SPACE.sub(' ', extractedTitle).strip()

    # Special cases.
    if extractedTitle.startswith('Aeon Flux'):
        extractedTitle = u'Æon Flux'

    return {'title': extractedTitle, 'year': releaseYear}


def getEditVersionFromFilename(filename, year):
    editVersion = 'Theatrical Cut'

    # Extract cut indicator.
    searchCutIndicator = RE_CUT_INDICATOR_1.search(filename)

    # Alternate case where cut indicator appears after production year.
    if searchCutIndicator is None:
        searchCutIndicator = re.search(r'(?<=%s[ \.])(extended|unrated|dc)(?=[ \.])' % year, filename, re.I)

    if searchCutIndicator is not None:
        editVersion = searchCutIndicator.groups()[0]

        # Normalize edit version.
        editVersion = editVersion.replace('.', ' ').replace('(', '').strip()
        editVersion = editVersion.lower().replace('dc', "Director's Cut").replace(' version', '')
        editVersion = editVersion.replace('directors ', "Director's ")
        editVersion = editVersion.title().replace("'S", "'s")
        editVersion = editVersion.replace(' Edition', ' Cut')
        if not editVersion.endswith(' Cut'): editVersion += ' Cut'
        editVersion = str(editVersion).strip()

    return editVersion


def identifyMovieByTitleYear(language, titlePrimary, yearPrimary, titleSecondary, yearSecondary):
    if yearPrimary is not None and yearSecondary is None:
        searchTitlePrimary, searchTitleSecondary = titlePrimary, titleSecondary
        searchYearPrimary, searchYearSecondary = yearPrimary, yearSecondary
    elif yearPrimary is None and yearSecondary is not None:
        searchTitlePrimary, searchTitleSecondary = titleSecondary, titlePrimary
        searchYearPrimary, searchYearSecondary = yearSecondary, yearPrimary
    elif yearSecondary is not None:
        searchTitlePrimary, searchTitleSecondary = titleSecondary, titlePrimary
        searchYearPrimary, searchYearSecondary = yearSecondary, yearPrimary
    elif yearPrimary is not None:
        searchTitlePrimary, searchTitleSecondary = titlePrimary, titleSecondary
        searchYearPrimary, searchYearSecondary = yearPrimary, yearSecondary
    elif len(titlePrimary) > len(titleSecondary):
        searchTitlePrimary, searchTitleSecondary = titlePrimary, titleSecondary
        searchYearPrimary, searchYearSecondary = yearPrimary, yearSecondary
    else:
        searchTitlePrimary, searchTitleSecondary = titleSecondary, titlePrimary
        searchYearPrimary, searchYearSecondary = yearSecondary, yearPrimary

    # searchTitlePrimary = searchTitlePrimary.encode('utf-8')
    # searchTitleSecondary = searchTitleSecondary.encode('utf-8')

    record = None
    identified = False

    try:
        logger.info('Trying to identify "%s" at themoviedb.org ...' % searchTitlePrimary)

        url = 'https://api.themoviedb.org/3/search/movie'
        params = {
            'api_key': THEMOVIEDB_API_KEY,
            'query': searchTitlePrimary.encode('utf-8'),
            'page': 1,
            'language': language,
            'include_adult': False,
        }
        if searchYearPrimary is not None:
            params['year'] = searchYearPrimary

        response = makeThrottledGetRequest(url, params).json()

        if response['total_results'] == 0 and searchTitleSecondary is not None:
            logger.info('Movie with title "%s" not found at themoviedb.org, retrying with title "%s" ...' % (searchTitlePrimary, searchTitleSecondary))
            params['query'] = searchTitleSecondary.encode('utf-8')
            if searchYearSecondary is not None:
                params['year'] = searchYearSecondary
            response = makeThrottledGetRequest(url, params).json()
        elif not identified:
            logger.info('Movie successfully identified using query: %s' % params['query'])
            identified = True

        if response['total_results'] == 0:
            logger.info('Movie with title "%s" still not found at themoviedb.org, retrying with title "%s" and search type "ngram" ...' % (searchTitleSecondary, searchTitlePrimary))
            params['query'] = searchTitlePrimary.encode('utf-8')
            params['search_type'] = 'ngram'
            if searchYearPrimary is not None:
                params['year'] = searchYearPrimary
            response = makeThrottledGetRequest(url, params).json()
        elif not identified:
            logger.info('Movie successfully identified using query: %s' % params['query'])
            identified = True

        if response['total_results'] == 0 and searchTitleSecondary is not None:
            logger.info('Movie with title "%s" still not found at themoviedb.org, retrying with title "%s" and search type "ngram" ...' % (searchTitlePrimary, searchTitleSecondary))
            params['query'] = searchTitleSecondary.encode('utf-8')
            if searchYearSecondary is not None:
                params['year'] = searchYearSecondary
            response = makeThrottledGetRequest(url, params).json()
        elif not identified:
            logger.info('Movie successfully identified using query: %s' % params['query'])
            identified = True

        if response['total_results'] == 0:
            logger.info('Movie with title "%s" still not found at themoviedb.org, retrying with title "%s", omitting year ...' % (searchTitleSecondary, searchTitlePrimary))
            params['query'] = searchTitlePrimary.encode('utf-8')
            if params.has_key('year'):
                del params['year']
            del params['search_type']
            response = makeThrottledGetRequest(url, params).json()
        elif not identified:
            logger.info('Movie successfully identified using query: %s' % params['query'])
            identified = True

        if response['total_results'] == 0 and searchTitleSecondary is not None:
            logger.info('Movie with title "%s" still not found at themoviedb.org, retrying with title "%s", omitting year ...' % (searchTitlePrimary, searchTitleSecondary))
            params['query'] = searchTitleSecondary.encode('utf-8')
            response = makeThrottledGetRequest(url, params).json()
        elif not identified:
            logger.info('Movie successfully identified using query: %s' % params['query'])
            identified = True

        if response['total_results'] == 0:
            logger.warning('Movie with title "%s" not found at themoviedb.org, giving up for now.' % searchTitlePrimary)
        else:
            movieId = response['results'][0]['id']

            url = 'https://api.themoviedb.org/3/movie/%d' % movieId
            params = {
                'api_key': THEMOVIEDB_API_KEY,
                'language': language,
                'append_to_response': 'trailers',
            }
            response = makeThrottledGetRequest(url, params).json()

            logger.info('Movie identified at themoviedb.org as "%s" with ID: %d.' % (response['original_title'], movieId))

            overview = response.get('overview', None)
            if overview is None:
                logger.info('Movie has no overview in locale "%s", falling back to English ...' % language)
                params['language'] = 'en'
                response = makeThrottledGetRequest(url, params).json()

            # Fetch rating from IMDB instead of TheMovieDB.
            rating = None
            idImdb = response['imdb_id']
            if idImdb is not None:
                url = 'http://www.imdb.com/title/%s/' % idImdb
                html = makeUnthrottledGetRequest(url).text
                ratingSearch = re.search('<span itemprop="ratingValue">\s*([^<]+)', html)
                if ratingSearch is not None:
                    rating = float(ratingSearch.group(1)) * 10

            if TRAILERS_HD.has_key(movieId):
                idYoutubeTrailer = TRAILERS_HD[movieId]
            elif response['trailers'].has_key('youtube') and len(response['trailers']['youtube']):
                idYoutubeTrailer = response['trailers']['youtube'][0].get('source')
            else:
                idYoutubeTrailer = None

            record = dict(
                idTheMovieDb  = movieId,
                idImdb        = idImdb,
                idYoutubeTrailer = idYoutubeTrailer,

                titleOriginal = response['original_title'],
                releaseYear   = datetime.datetime.strptime(response['release_date'], '%Y-%m-%d').year,
                runtime       = response['runtime'] or None,

                urlBackdrop   = response['backdrop_path'],
                urlPoster     = response['poster_path'],

                homepage      = response['homepage'],
                budget        = response['budget'] or None,
                revenue       = response['revenue'] or None,

                rating        = rating,

                locale        = language,
                title         = response['title'] or response['original_title'],
                storyline     = overview,
            )
    except JSONDecodeError:
        logger.error('Error while querying themoviedb.org for "%s" or "%s".' % (titlePrimary, titleSecondary))

    return record
