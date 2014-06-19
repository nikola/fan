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
from orchestrator.control import start as startOrchestrator, stop as stopOrchestrator
from downloader.control import start as startDownloader, stop as stopDownloader
from player.control import start as startPlayer, stop as stopPlayer
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
        # Presenter has been closed, now kick off clean-up tasks.
        stopOrchestrator()
        stopDownloader()
        stopPlayer()

        # Block until all queue items have been processed.
        interProcessQueue.join()
        interProcessQueue.close()

        # Gracefully stop processes.
        orchestrator.join()
        downloader.join()
        player.join()

        os.remove(certificateLocation)

        # Circumvent SystemExit exception handler.
        os._exit(1)

    # sys.excepthook = handleException

    try:
        bridgeToken = uuid4().hex
        bootToken = uuid4().hex

        certificateLocation = getCertificateLocation()

        userAgent = getUserAgent()

        # Omni-directional message queue between boot process, collector process and server process.
        interProcessQueue = InterProcessQueue()

        player = startPlayer(interProcessQueue)

        downloader = startDownloader(interProcessQueue)

        if DEBUG:
            serverPort = 50000
        else:
            serverPort = getVacantPort()
        # END DEBUG

        # Start process, but spawn file scanner and watcher only after receiving a kick off event from the presenter.
        orchestrator = startOrchestrator(interProcessQueue, certificateLocation, userAgent, serverPort, bridgeToken, bootToken)

        # Start the blocking presenter process.
        present(_shutdown, userAgent, serverPort, bridgeToken, bootToken) # TODO: refactor last arguments into reusable tuple
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
