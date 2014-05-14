# coding: utf-8
""" TODO: implement SIGINT handler
        http://stackoverflow.com/a/1112350
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import sys
from multiprocessing import JoinableQueue as InterProcessQueue, freeze_support

from presenter.control import startPresenter
from utils.agent import getUserAgent
from utils.system import isCompatiblePlatform
from server.control import start as startServer, stop as stopServer
from collector.control import start as startCollector, stop as stopCollector


if __name__ == '__main__':
    freeze_support()

    if not isCompatiblePlatform():
        sys.exit()

    # sys.excepthook = handleException

    try:
        # Omni-directional message queue between boot process,
        # collector process and server process.
        interProcessQueue = InterProcessQueue()

        # Start process, but spawn file watcher and stream manager only after
        # receiving a kick off event from the presenter.
        collector = startCollector(interProcessQueue)

        userAgent = getUserAgent()
        server, port = startServer(interProcessQueue, userAgent)

        # Start blocking presenter process.
        startPresenter(userAgent, 'https://127.0.0.1:%d/' % port)

        # Presenter has been closed, now kick off clean-up tasks.
        stopServer()
        stopCollector()

        # Block until all queue items have been processed.
        interProcessQueue.join()
        interProcessQueue.close()

        # Gracefully stop processes.
        server.join()
        collector.join()
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
