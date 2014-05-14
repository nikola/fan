# coding: utf-8
""" TODO: implement SIGINT handler
        http://stackoverflow.com/a/1112350
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import sys
# import platform
from utils.collector import *
from utils.identifier import *

from presenter.control import startPresenter #, stopPresenter
from utils.agent import getUserAgent
from utils.system import isCompatiblePlatform
from server.control import start as startServer, stop as stopServer
from collector.control import start as startCollector, stop as stopCollector


if __name__ == '__main__':
    if not isCompatiblePlatform():
        sys.exit()

    # sys.excepthook = handleException

    try:
        startCollector()

        userAgent = getUserAgent()
        port = startServer(userAgent)

        startPresenter(userAgent, r"https://127.0.0.1:%d/" % port, (stopServer, stopCollector))
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
