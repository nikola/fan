# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@generic.company)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

import sys
import platform
from utils.collector import *
from utils.identifier import *

from presenter.control import startPresenter #, stopPresenter
from utils.agent import getUserAgent
from utils.system import isCompatiblePlatform
from server.control import start as startServer, stop as stopServer
from watcher.control import start as startWatcher, stop as stopWatcher


if __name__ == "__main__":
    if not isCompatiblePlatform(): #  or platform.architecture()[0] != "32bit" or platform.win32_ver()[-1].endswith(" Checked"):
        sys.exit()


    # TODO: implement SIGINT handler
    # http://stackoverflow.com/a/1112350

    try:
        startWatcher()

        userAgent = getUserAgent()
        port = startServer(userAgent)

        # from utils.fs import getFileStreams
        # print getFileStreams(os.path.join(PROJECT_PATH, 'backend', 'run.py'))

        # sys.excepthook = handleException

        """
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
        """

        startPresenter(userAgent, r"https://127.0.0.1:%d/" % port, (stopServer, stopWatcher))

    except (KeyboardInterrupt, SystemError):
        # streamManager.shutdown()
        # stopServer()
        # sys.exit(1)
        raise
    except Exception, e:
        # streamManager.shutdown()
        # stopServer()
        # sys.exit(1)
        raise
    # else:
    #     streamManager.shutdown()
    #     stopServer()
