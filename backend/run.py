# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

import os
import platform
from utils.collector import *
from utils.identifier import *
from utils.db import *
from chromium.launcher import *
from utils.agent import getUserAgent
from utils.agent import isCompatiblePlatform
from server.control import start as startServer, stop as stopServer
from config import DB_PERSISTENCE_PATH


def _shutdown():
    """
    """
    stopServer()


if __name__ == "__main__":
    # Must be Windows 7 or higher, non-debug revision, and 32-bit Python interpreter due to CEF dependency.
    if not isCompatiblePlatform() or platform.architecture()[0] != "32bit" or platform.win32_ver()[-1].endswith(" Checked"):
        sys.exit()

    try:
        userAgent = getUserAgent()
        port = startServer(userAgent)

        # sys.excepthook = handleException

        streamManager = StreamManager(DB_PERSISTENCE_PATH)

        for (path, container, files) in getMoviePathnames(r"M:\\"):
            basedata = getBasedataFromPathname(container)

            for filename in files:
                streamLocation = os.path.join(path, filename)
                print streamLocation
                continue

                print "processing %s" % streamLocation
                movieRecord = getMovieFromRawData("de", "de", basedata["title"], basedata["year"])
                if movieRecord is None: continue

                print "adding %s from %s" % (movieRecord["titleOriginal"], streamLocation)
                streamManager.addMovieStream(movieRecord, streamLocation)

                time.sleep(0.5)

        launchChrome(userAgent, r"https://127.0.0.1:%d/" % port, (stopServer, streamManager.shutdown))
    except (KeyboardInterrupt, SystemError):
        streamManager.shutdown()
        stopServer()
        sys.exit(1)
    except Exception, e:
        streamManager.shutdown()
        stopServer()
        sys.exit(1)
