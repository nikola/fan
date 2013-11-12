# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

import sys
import time
import platform
from utils.collector import *
from utils.identifier import *
from utils.db import *


if __name__ == "__main__":
    if platform.system() != "Windows":
        sys.exit()

    streamManager = StreamManager()

    for (path, container, files) in getMoviePathnames(r"M:\\"):
        basedata = getBasedataFromPathname(container)

        for filename in files:
            streamLocation = os.path.join(path, filename)

            print "processing %s" % streamLocation
            movieRecord = getMovieFromRawData("de", "de", basedata["title"], basedata["year"])
            if movieRecord is None: continue

            print "adding %s from %s" % (movieRecord["titleOriginal"], streamLocation)
            streamManager.addMovieStream(movieRecord, streamLocation)

            time.sleep(0.5)
