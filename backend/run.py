# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

import platform
from utils.collector import *
from utils.identifier import *
from utils.db import *
from utils.chrome import *
from utils.agent import isCompatiblePlatform
from server.control import start as startServer
from server.control import stop as stopServer


if __name__ == "__main__":
    # Must be Windows 7 or higher, non-debug revision, and 32-bit Python interpreter due to CEF dependency.
    if not isCompatiblePlatform() or platform.architecture()[0] != "32bit" or platform.win32_ver()[-1].endswith(" Checked"):
        sys.exit()

    startServer(8080)

    sys.excepthook = handleException

    execChromeContainer(r"C:/Users/Niko/Documents/GitHub/ka-BOOM/backend/vendor/cef/example.html", stopServer)
    # execChromeContainer(r"C:/Users/Niko/Documents/GitHub/ka-BOOM/frontend/app/index.html")


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
