# coding: utf-8
""" TODO: implement SIGINT handler
        http://stackoverflow.com/a/1112350
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import sys
import os
from uuid import uuid4
from multiprocessing import JoinableQueue as InterProcessQueue, freeze_support

from utils.system import isCompatiblePlatform
from utils.agent import getUserAgent
from utils.net import getVacantPort, getCertificateLocation
from collector.control import start as startCollector, stop as stopCollector
from server.control import start as startServer, stop as stopServer
from presenter.control import start as present


if __name__ == '__main__':
    freeze_support()

    if not isCompatiblePlatform():
        sys.exit()

    def _shutdown():
        print '_shutdown called'

        # Presenter has been closed, now kick off clean-up tasks.
        stopServer()
        stopCollector()

        # Block until all queue items have been processed.
        interProcessQueue.join()
        interProcessQueue.close()

        # Gracefully stop processes.
        server.join()
        collector.join()

        os.remove(certificateLocation)

        # Circumvent SystemExit exception handler.
        os._exit(1)

    # sys.excepthook = handleException

    try:
        bridgeToken = uuid4().hex

        certificateLocation = getCertificateLocation()
        userAgent = getUserAgent()

        # Omni-directional message queue between boot process, collector process and server process.
        interProcessQueue = InterProcessQueue()

        # Start process, but spawn file watcher and stream manager only after receiving a kick off event from the presenter.
        websocketPort = getVacantPort()
        collector = startCollector(interProcessQueue, websocketPort, certificateLocation, userAgent, bridgeToken) # TODO: not token here

        httpPort = getVacantPort()
        server = startServer(interProcessQueue, httpPort, certificateLocation, userAgent)                       # TODO: token here!

        # Start blocking presenter process.
        present(userAgent, httpPort, websocketPort, _shutdown, bridgeToken)
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

    # os._exit(1)
    # else:
    #     streamManager.shutdown()
    #     stopServer()
