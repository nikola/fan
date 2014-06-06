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
from ctypes import windll

from settings import DEBUG
from utils.system import isCompatiblePlatform, isNtfsFilesystem, getScreenResolution
from utils.agent import getUserAgent
from utils.net import getVacantPort, getCertificateLocation
from collector.control import start as startCollector, stop as stopCollector
from downloader.control import start as startDownloader, stop as stopDownloader
from player.control import start as startPlayer, stop as stopPlayer
from server.control import start as startServer, stop as stopServer
from presenter.control import start as present


if __name__ == '__main__':
    freeze_support()

    if not isCompatiblePlatform():
        windll.user32.MessageBoxA(0, 'This application is only compatible with Windows Vista or newer!', 'Error', 0)
        sys.exit()

    if not isNtfsFilesystem():
        windll.user32.MessageBoxA(0, 'This application must be run from an NTFS partition!', 'Error', 0)
        sys.exit()

    if getScreenResolution() != (1920, 1080):
        windll.user32.MessageBoxA(0, 'This application must be run at 1920x1080 screen resolution!', 'Error', 0)
        sys.exit()

    def _shutdown():
        print '_shutdown called'

        # Presenter has been closed, now kick off clean-up tasks.
        stopServer()
        stopCollector()
        stopDownloader()
        stopPlayer()

        # Block until all queue items have been processed.
        interProcessQueue.join()
        interProcessQueue.close()

        # Gracefully stop processes.
        server.join()
        collector.join()
        downloader.join()
        player.join()

        os.remove(certificateLocation)

        # Circumvent SystemExit exception handler.
        os._exit(1)

    # sys.excepthook = handleException

    try:
        bridgeToken = uuid4().hex
        frontendToken = uuid4().hex

        certificateLocation = getCertificateLocation()
        userAgent = getUserAgent()

        # Omni-directional message queue between boot process, collector process and server process.
        interProcessQueue = InterProcessQueue()

        player = startPlayer(interProcessQueue)

        downloader = startDownloader(interProcessQueue)

        # Start process, but spawn file watcher and stream manager only after receiving a kick off event from the presenter.
        websocketPort = getVacantPort()
        collector = startCollector(interProcessQueue, websocketPort, certificateLocation, userAgent, bridgeToken) # TODO: not token here

        if DEBUG:
            httpPort = 50000
        else:
            httpPort = getVacantPort()
        # END DEBUG
        server = startServer(interProcessQueue, httpPort, websocketPort, certificateLocation, userAgent, frontendToken)          # TODO: token here!

        # Start the blocking presenter process.
        present(userAgent, httpPort, websocketPort, _shutdown, bridgeToken, frontendToken)
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
