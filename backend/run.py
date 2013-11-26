# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

import platform
# from multiprocessing import Value, Lock
from ctypes import c_char_p
# from config import CHROME_USER_AGENT
from utils.collector import *
from utils.identifier import *
from utils.db import *
from utils.chrome import *
from utils.agent import getUserAgent
from utils.agent import isCompatiblePlatform
from server.control import start as startServer
from server.control import stop as stopServer


if __name__ == "__main__":
    # Must be Windows 7 or higher, non-debug revision, and 32-bit Python interpreter due to CEF dependency.
    if not isCompatiblePlatform() or platform.architecture()[0] != "32bit" or platform.win32_ver()[-1].endswith(" Checked"):
        sys.exit()

    userAgent = getUserAgent()
    port = startServer(userAgent)

    sys.excepthook = handleException

    # execChromeContainer(r"https://127.0.0.1:8080/static/test.html", stopServer)
    # execChromeContainer(r"https://127.0.0.1:8080/app/index-async.html", stopServer)
    execChromeContainer(userAgent, r"https://127.0.0.1:%d/" % port, stopServer)

    # execChromeContainer(r"C:/Users/Niko/Documents/GitHub/ka-BOOM/backend/vendor/cef/example.html", stopServer)
    # execChromeContainer(r"C:/Users/Niko/Documents/GitHub/ka-BOOM/frontend/app/index.html", stopServer)

    # while 1: pass

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
