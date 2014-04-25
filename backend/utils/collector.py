# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@generic.company)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

import os
import re

STREAM_SIZE_THRESHOLD = 1024 * 1024 * 10 # 10 MiB


def getMoviePathnames(top):
    """
    """
    # If the root is a mapped network share, check first if it's mounted.
    if any([True for drive in os.popen("wmic logicaldisk get Name, DriveType").readlines() if
            re.compile(r"^4\s+%s:" % top[0]).search(drive) is not None]) and not os.access(top, os.R_OK):
        return

    # Pass root as a Unicode string.
    for root, dirs, files in os.walk(unicode(top)):
        dirname = re.compile(r"[a-z]\:\\\\", re.I).sub("", root)

        # Skip directories which contain no movie files.
        if not any([True for name in files if name.endswith((".mkv", ".MKV"))]) or re.compile(r"\\!?sample$", re.I).search(dirname) is not None: continue

        # Ignore parent directory for the time being.
        if dirname.find("\\") != -1:
            dirname = re.compile(r"(?<=\\).*$").search(dirname).group()

        # Remove leading underscore.
        dirname = re.compile(r"^_ +").sub("", dirname).strip()

        # Only files with actual movie content.
        streams = []
        for filename in files:
            if not filename.lower().endswith(".mkv"):
                continue
            elif re.compile(r"sample", re.I).search(filename) is not None:
                continue
            elif os.stat(os.path.join(root, filename)).st_size < STREAM_SIZE_THRESHOLD:
                continue
            else:
                streams.append(filename)
        if not len(streams): continue

        yield (root, dirname, streams)


def getBasedataFromPathname(pathname):
    """
    """
    releaseYear = 2013
    editVersion = "Theatrical Cut"

    searchReleaseYear = re.compile(r"(?<!^)((19|20)\d{2})[a-zA-Z0-9\.\-\) '\[\]]*$").search(pathname)
    if searchReleaseYear is not None:
        releaseYear = int(searchReleaseYear.groups()[0])
        rawTitle = re.search("^(.*)(?=%s)" % releaseYear, pathname).groups()[0]
    else:
        rawTitle = pathname

    extractedTitle = rawTitle

    # Remove special characters.
    extractedTitle = re.compile(r"[\(\[,\-]").sub(" ", extractedTitle)

    # Convert dots to spaces (except when followed by a zero).
    extractedTitle = re.compile(r"\.(?!0)").sub(" ", extractedTitle)

    # Remove superfluous multi-angle indicators.
    extractedTitle = re.compile(r"\d[\- ]*in[\- ]*\d").sub("", extractedTitle).strip()

    # Remove superfluous edition indicators.
    extractedTitle = re.compile(r"(?<= )(special edition|hybrid|(2|3)d source|open matte|tv aspect ratio)(?= |$)", re.I).sub(" ", extractedTitle).strip()

    # Collapse multiple spaces.
    extractedTitle = re.compile("  +").sub(" ", extractedTitle)

    # Extract cut indicator.
    searchCutIndicator = re.compile(r"((extended|final|theatrical|international|director[ ']s?)( unrated)?( cut|$))", re.I).search(extractedTitle)
    if searchCutIndicator is not None:
        editVersion = searchCutIndicator.groups()[0]
        extractedTitle = extractedTitle.replace(editVersion, "")

    # Remove leading Roman numerals.
    extractedTitle = re.compile(r"^X?(IX|IV|V?I{0,3}) ").sub("", extractedTitle)

    # Remove surrounding whitespace.
    extractedTitle = extractedTitle.strip()

    return {
        "title":        extractedTitle,
        "year":         releaseYear,
        "editVersion":  editVersion,
    }
