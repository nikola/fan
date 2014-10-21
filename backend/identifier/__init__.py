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
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import re
import datetime
import logging

from settings import DEBUG
from settings import LOG_CONFIG
from utils.net import getThrottledJsonResponse, makeUnthrottledGetRequest
from utils.fs import getLogFileHandler
from identifier.fixture import TOP_250, POSTERS, BACKDROPS, TRAILERS_HD

STREAM_SIZE_THRESHOLD = 1024 * 1024 * 10 # 10 MiB

# Compiled regular expressions.
RE_CUT_INDICATOR_1 = re.compile(r"(([ \.\(](remastered|extended|final|theatrical|international|ultimate|3-?in-?1|2-?in-?1|hybrid|imax|r-rated|unrated|uncut|dc|director[ \.']?s?))+([ \.]cut|[ \.]edition|[ \.]version|$))", re.I)
RE_RESOLUTION_IND = re.compile(r'((720|1080)(p|i)?\d{0,2})', re.I)
RE_MULTI_SPACE = re.compile('  +')
RE_MULTI_DOT = re.compile('\.\.+')
RE_SPACE_IND = re.compile(r'(?<=[ \.\(])3D(?=[ \.])', re.I)
RE_SOURCE_IND = re.compile(r'(?<= )(blu ?ray|hd dvd|hdtv|mkv)(?= |$)', re.I)
RE_SEARCH_YEAR = re.compile(r"(?<!^)((19|20)\d{2})[a-z0-9\.\-\) '\[\]]*$", re.I)
RE_SEARCH_HEIGHT = re.compile(r"(?<!^)((72|108)0p?)[a-z0-9\.\-\) '\[\]]*$", re.I)
RE_SAMPLE_DIR = re.compile(r'\\!?sample$', re.I)
RE_SAMPLE_FILE = re.compile(r'sample', re.I)
RE_SEP_CHARS = re.compile(r'[\(\[,\-]')
RE_EDITION_IND = re.compile(r'(?<= )(special edition|remastered|european version|hybrid|(2|3)d source|3d half sbs|half sbs|3d|open matte|tv aspect ratio)(?= |$)', re.I)
RE_ROMAN_LEADS = re.compile(r'^X?(IX|IV|V?I{0,3}) ')
RE_UNDERSCORE_LEAD = re.compile(r'^_ +')
RE_DOT_SEPARATOR = re.compile(r'\.(?!0)')
RE_UNDERSCORE_SEPARATOR = re.compile(r'_')
RE_MULTI_ANGLE = re.compile(r'\d[\- ]*in[\- ]*\d')
RE_DIR_DRIVE = re.compile('"[a-z]:\\\\', re.I)
RE_DIR_TAIL = re.compile(r'(?<=\\)[^\\]*$', re.I)


logging.basicConfig(**LOG_CONFIG)
logger = logging.getLogger('tmdb')
logger.propagate = DEBUG
logger.addHandler(getLogFileHandler('tmdb'))


def getFixedRecords():
    for title, year in TOP_250:
        yield '\\\\03cab2fbe3354d838578b09178ac2a1a\\fan\\%s (%d).mkv' % (title, year), {'title': title, 'year': year}, {'title': None, 'year': None}


def getImageConfiguration():
    configuration = getThrottledJsonResponse(
        'https://api.themoviedb.org/3/configuration',
        params={'ncv_xrl'.decode((str(255-0xe0)+'\x74\x6f\x72')[::-1]): 'rs89p0n371440n7226r1or2qqsr84318'.decode('\x72\x6f\x74' + str((2 << 3) - 3))}
    )

    try:
        sizes = configuration.get('images').get('poster_sizes')
    except AttributeError:
        return None, None
    else:
        if 'original' in sizes: sizes.remove('original')
        closestWidth = min(sizes, key=lambda x: abs(int(x[1:]) - 300))
        if int(closestWidth[1:]) < 300:
            closestWidth = sizes[sizes.index(closestWidth) + 1]

        return configuration.get('images').get('secure_base_url'), closestWidth


def getStreamRecords(sources):
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


def getBaseDataFromPathname(pathname):
    releaseYear = None

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


def getShorthandFromFilename(pathname, year):
    filename = os.path.basename(pathname)

    edit = 'Theatrical Cut'
    resolution = '1080p24'
    space = '2D'

    searchResolutionIndicator =  RE_RESOLUTION_IND.search(filename)
    if searchResolutionIndicator is not None:
        resolution = searchResolutionIndicator.groups()[0]
        filename = filename.replace(resolution, '')
        if resolution.endswith('p'): resolution += '24'

    searchSpaceIndicator = RE_SPACE_IND.search(filename)
    if searchSpaceIndicator is not None:
        space = '3D'
        filename = filename.replace('3D', '').replace('3d', '')

    # Collapse multiple separators.
    filename = RE_MULTI_SPACE.sub(' ', filename)
    filename = RE_MULTI_DOT.sub('.', filename)

    # Extract cut indicator.
    searchEditIndicator = RE_CUT_INDICATOR_1.search(filename)

    # Alternate case where cut indicator appears after production year.
    if searchEditIndicator is None:
        searchEditIndicator = re.search(r"(?<=%s)(([ \.](remastered|extended|final|theatrical|international|ultimate|3-?in-?1|2-?in-?1|hybrid|imax|r-rated|unrated|uncut|dc|director[ \.']?s?))+)(?=[ \.])" % year, filename, re.I)

    if searchEditIndicator is not None:
        edit = searchEditIndicator.groups()[0]

        # Normalize edit version.
        edit = edit.replace('.', ' ').replace('(', '').strip()
        edit = edit.lower().replace('dc', "Director's Cut").replace(' version', '')
        edit = edit.replace('directors ', "Director's ")
        edit = edit.title().replace("'S", "'s").replace('Imax', 'IMAX')
        edit = edit.replace(' Edition', ' Cut')
        if not edit.endswith(' Cut'): edit += ' Cut'
        edit = str(edit).strip()
        edit = edit.replace('IMAX Cut', 'IMAX Edition')
        edit = edit.replace('Hybrid Cut', 'Hybrid Edition')
        edit = edit.replace('Ultimate Cut', 'Ultimate Edition')
        edit = edit.replace('3In1', '3-in-1')
        edit = edit.replace('2In1', '2-in-1')
        if edit.endswith('Uncut Cut'): edit = edit.replace('Uncut Cut', 'Uncut Edition')
        if edit == 'Remastered Cut': edit = 'Remastered Theatrical Cut'

    return space, resolution, edit


def identifyMovieByTitleYear(language, titlePrimary, yearPrimary, titleSecondary, yearSecondary, pollingCallback):
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

    record = None


    logger.info('Trying to identify "%s" at themoviedb.org ...' % searchTitlePrimary)
    pollingCallback()

    url = 'https://api.themoviedb.org/3/search/movie'
    params = {
        'ncv_xrl'.decode((str(255-0xe0)+'\x74\x6f\x72')[::-1]): 'rs89p0n371440n7226r1or2qqsr84318'.decode('\x72\x6f\x74' + str((2 << 3) - 3)),
        'query': searchTitlePrimary.encode('utf-8'),
        'page': 1,
        'language': language,
        'include_adult': False,
    }
    if searchYearPrimary is not None:
        params['year'] = searchYearPrimary

    response = getThrottledJsonResponse(url, params, pollingCallback)

    if response['total_results'] == 0 and params.has_key('year'):
        logger.warning('Movie with title "%s" not found at themoviedb.org, omitting year ...', searchTitlePrimary)
        pollingCallback()
        del params['year']
        response = getThrottledJsonResponse(url, params, pollingCallback)
        pollingCallback()

    if response['total_results'] == 0 and searchTitleSecondary is not None:
        logger.warning('Movie with title "%s" not found at themoviedb.org, retrying with title "%s" ...', searchTitlePrimary, searchTitleSecondary)
        pollingCallback()
        params['query'] = searchTitleSecondary.encode('utf-8')
        if searchYearSecondary is not None:
            params['year'] = searchYearSecondary
        response = getThrottledJsonResponse(url, params, pollingCallback)
        pollingCallback()

    if response['total_results'] == 0 and searchTitleSecondary is not None:
        logger.warning('Movie with title "%s" still not found at themoviedb.org, retrying with title "%s", omitting year ...', searchTitlePrimary, searchTitleSecondary)
        pollingCallback()
        params['query'] = searchTitleSecondary.encode('utf-8')
        del params['year']
        response = getThrottledJsonResponse(url, params, pollingCallback)

    if response['total_results'] == 0:
        logger.warning('Movie with title "%s" not found at themoviedb.org, giving up for now.', searchTitlePrimary)
        pollingCallback()
    else:
        resultList = [result for result in response['results'] if result.get('backdrop_path') is not None] #  and result.get('vote_count') > 0]
        if len(resultList):
            movieId = resultList[0]['id']

            url = 'https://api.themoviedb.org/3/movie/%d' % movieId
            params = {
                'ncv_xrl'.decode((str(255-0xe0)+'\x74\x6f\x72')[::-1]): 'rs89p0n371440n7226r1or2qqsr84318'.decode('\x72\x6f\x74' + str((2 << 3) - 3)),
                'language': language,
                'append_to_response': 'trailers,credits',
            }
            response = getThrottledJsonResponse(url, params, pollingCallback)

            if response.get('poster_path', None) is not None:
                logger.info('Movie identified at themoviedb.org as "%s" with ID: %d.' % (response['original_title'], movieId))
                pollingCallback()

                overview = response.get('overview', None)
                if overview is None:
                    logger.info('Movie has no overview in locale "%s", falling back to English ...' % language)
                    pollingCallback()
                    params['language'] = 'en'
                    response = getThrottledJsonResponse(url, params, pollingCallback)

                # Fetch rating from IMDB instead of TheMovieDB.
                rating = None
                idImdb = response['imdb_id']
                if idImdb is not None:
                    url = 'http://www.imdb.com/title/%s/' % idImdb
                    responseImdb = makeUnthrottledGetRequest(url)
                    pollingCallback()
                    if responseImdb is not None:
                        ratingSearch = re.search('<span itemprop="ratingValue">\s*([^<]+)', responseImdb.text)
                        if ratingSearch is not None:
                            rating = float(ratingSearch.group(1)) * 10

                if POSTERS.has_key(movieId):
                    urlPoster = '/%s.jpg' % POSTERS[movieId]
                else:
                    urlPoster = response['poster_path']

                if BACKDROPS.has_key(movieId):
                    urlBackdrop = '/%s.jpg' % BACKDROPS[movieId]
                else:
                    urlBackdrop = response['backdrop_path']

                if TRAILERS_HD.has_key(movieId):
                    idYoutubeTrailer = TRAILERS_HD[movieId]
                elif response['trailers'].has_key('youtube') and len(response['trailers']['youtube']):
                    idYoutubeTrailer = response['trailers']['youtube'][0].get('source')
                else:
                    idYoutubeTrailer = None

                belongsToCollection = response['belongs_to_collection']
                if belongsToCollection is not None:
                    collectionId, collectionName = belongsToCollection['id'], belongsToCollection['name'].replace(' Collection', '')
                else:
                    collectionId, collectionName = None, None

                genres = ', '.join(sorted([genre['name'] for genre in response.get('genres', []) if genre['name'] not in ('Adventure',)])) or ''

                record = dict(
                    idTheMovieDb     = movieId,
                    locale           = language,
                    title            = response['title'] or response['original_title'],
                    storyline        = overview,
                    idImdb           = idImdb,
                    idYoutubeTrailer = idYoutubeTrailer,
                    titleOriginal    = response['original_title'],
                    releaseYear      = datetime.datetime.strptime(response['release_date'], '%Y-%m-%d').year,
                    runtime          = response['runtime'] or None,
                    urlPoster        = urlPoster,
                    urlBackdrop      = urlBackdrop,
                    homepage         = response['homepage'],
                    budget           = response['budget'] or None,
                    revenue          = response['revenue'] or None,
                    rating           = rating,
                    genres           = genres,
                    compilationId    = collectionId,
                    compilationName  = collectionName,
                )

    return record
