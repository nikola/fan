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

from presenter.control import startPresenter
from utils.agent import getUserAgent
from utils.system import isCompatiblePlatform
from utils.net import getVacantPort, getCertificateLocation
from server.control import start as startServer, stop as stopServer
from collector.control import start as startCollector, stop as stopCollector


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



    # sys.excepthook = handleException

    try:
        bridgeToken = uuid4().hex

        certificateLocation = getCertificateLocation()
        userAgent = getUserAgent()

        # Omni-directional message queue between boot process,
        # collector process and server process.
        interProcessQueue = InterProcessQueue()

        # Start process, but spawn file watcher and stream manager only after
        # receiving a kick off event from the presenter.
        websocketPort = getVacantPort()
        collector = startCollector(interProcessQueue, websocketPort, certificateLocation, userAgent, bridgeToken)

        httpPort = getVacantPort()
        server = startServer(interProcessQueue, httpPort, certificateLocation, userAgent)

        # Start blocking presenter process.
        # startPresenter(userAgent, 'https://127.0.0.1:%d/' % httpPort)
        startPresenter(userAgent, httpPort, websocketPort, _shutdown, bridgeToken)
        # Calling cefpython.shutdown() will also close all open Websockets,
        # i.e. at this point there are none open.

        _shutdown()

        # # Presenter has been closed, now kick off clean-up tasks.
        # stopServer()
        # stopCollector()
        #
        # # Block until all queue items have been processed.
        # interProcessQueue.join()
        # interProcessQueue.close()
        #
        # # Gracefully stop processes.
        # server.join()
        # collector.join()
        #
        # os.remove(certificateLocation)
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
