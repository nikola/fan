# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import re

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
RE_MULTI_ANGLE = re.compile(r'\d[\- ]*in[\- ]*\d')
RE_EDITION_IND = re.compile(r'(?<= )(special edition|hybrid|(2|3)d source|open matte|tv aspect ratio)(?= |$)', re.I)
RE_MULTI_SPACE = re.compile('  +')
RE_DIR_DRIVE = re.compile('"[a-z]\:\\\\', re.I)
RE_DIR_TAIL = re.compile(r'(?<=\\)[^\\]*$', re.I)


def getMoviePathnames(top):
    # If the root is a mapped network share, check first if it's mounted.
    # if any([True for drive in os.popen("wmic logicaldisk get Name, DriveType").readlines() if
    #         re.compile(r"^4\s+%s:" % top[0]).search(drive) is not None]) and not os.access(top, os.R_OK):
    #     raise StopIteration

    # Pass root as a Unicode string.
    for root, dirs, files in os.walk(unicode(top)):
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
                    yield (root, dirname, streams)


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


def getBaseDataFromDirName(pathname):
    releaseYear = 2014

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
    extractedTitle = RE_DOT_SEPARATOR.sub(' ', extractedTitle)

    # Remove superfluous multi-angle indicators.
    extractedTitle = RE_MULTI_ANGLE.sub('', extractedTitle).strip()

    # Remove superfluous edition indicators.
    extractedTitle = RE_EDITION_IND.sub(' ', extractedTitle).strip()

    # Collapse multiple spaces.
    extractedTitle = RE_MULTI_SPACE.sub(' ', extractedTitle)

    # Remove cut indicator.
    extractedTitle = RE_CUT_INDICATOR_1.sub('', extractedTitle)
    extractedTitle = re.sub(r'(?<=%s[ \.])(extended|unrated)(?=[ \.])' % releaseYear, '', extractedTitle, 0, re.I)

    # Remove leading Roman numerals.
    extractedTitle = RE_ROMAN_LEADS.sub('', extractedTitle)

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
