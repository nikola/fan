# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import sys
import os
from uuid import uuid4
from multiprocessing import JoinableQueue as InterProcessQueue, freeze_support
from ctypes import windll

from settings import DEBUG
from models import StreamManager
from utils.system import isCompatiblePlatform, isNtfsFilesystem, getScreenResolution, isDesktopCompositionEnabled
from utils.agent import getUserAgent
from utils.net import getVacantPort, getCertificateLocation
from orchestrator.control import start as startOrchestrator, stop as stopOrchestrator
from downloader.control import start as startDownloader, stop as stopDownloader
from player.control import start as startPlayer, stop as stopPlayer
from analyzer.control import start as startAnalyzer, stop as stopAnalyzer
from presenter.control import start as present


if __name__ == '__main__':
    freeze_support()

    if not isCompatiblePlatform():
        windll.user32.MessageBoxA(0, 'This application is only compatible with Windows Vista or newer.', 'Error', 0)
        sys.exit()

    if not isNtfsFilesystem():
        windll.user32.MessageBoxA(0, 'This application must be run from an NTFS partition.', 'Error', 0)
        sys.exit()

    if getScreenResolution() != (1920, 1080):
        windll.user32.MessageBoxA(0, 'This application must be run at 1920x1080 screen resolution.', 'Error', 0)
        sys.exit()

    if not isDesktopCompositionEnabled():
        windll.user32.MessageBoxA(0, 'This application requires that the Desktop Window Manager (DWM) is enabled.', 'Error', 0)
        sys.exit()

    def _shutdown():
        # Presenter has been closed, now kick off clean-up tasks.
        stopOrchestrator()
        stopPlayer()
        stopAnalyzer()
        stopDownloader()

        # Block until all queue items have been processed.
        interProcessQueue.join()
        interProcessQueue.close()

        # Gracefully stop processes.
        orchestrator.join()
        player.join()
        analyzer.join()
        downloader.join()

        os.remove(certificateLocation)

        # Circumvent SystemExit exception handler.
        os._exit(1)

    # sys.excepthook = handleException

    # Create DB connection here to initialize models.
    streamManager = StreamManager()
    streamManager.shutdown()
    del streamManager

    try:
        if DEBUG:
            serverPort = 50000
        else:
            serverPort = getVacantPort()
        # END DEBUG

        certificateLocation = getCertificateLocation()

        # Omni-directional message queue between boot process, collector process and server process.
        interProcessQueue = InterProcessQueue()

        downloader = startDownloader(interProcessQueue)
        analyzer = startAnalyzer(interProcessQueue)
        player = startPlayer(interProcessQueue)

        arguments = (getUserAgent(), serverPort, uuid4().hex, uuid4().hex)

        # Start process, but spawn file scanner and watcher only after receiving a kick-off event from the presenter.
        orchestrator = startOrchestrator(interProcessQueue, certificateLocation, *arguments)

        # Start the blocking presenter process.
        present(_shutdown, *arguments)

        # TODO: implement SIGINT handler
        # http://stackoverflow.com/a/1112350
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
