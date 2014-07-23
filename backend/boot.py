# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import sys
import os
import logging
from uuid import uuid4
from multiprocessing import JoinableQueue as InterProcessQueue, freeze_support
from ctypes import windll

import win32file

from settings import DEBUG
from settings import LOG_CONFIG
from models import initialize as initStreamManager
from utils.system import isCompatiblePlatform, isNtfsFilesystem, getScreenResolution, isDesktopCompositionEnabled
from utils.agent import getUserAgent
from utils.net import getVacantPort, getCertificateLocation
from utils.fs import getLogFileHandler, createAppStorageStructure
from utils.config import getCurrentUserConfig
from orchestrator.control import start as startOrchestrator, stop as stopOrchestrator
from downloader.control import start as startDownloader, stop as stopDownloader
from player.control import start as startPlayer, stop as stopPlayer
from analyzer.control import start as startAnalyzer, stop as stopAnalyzer
from presenter.control import start as present


if __name__ == '__main__':
    freeze_support()

    logging.basicConfig(**LOG_CONFIG)
    logger = logging.getLogger('application')
    logger.addHandler(getLogFileHandler('application'))

    if not isCompatiblePlatform():
        windll.user32.MessageBoxA(0, 'This application is only compatible with Windows Vista or newer.', 'Error', 0)
        logger.critical('Aborting because system is not Windows Vista or newer.')
        sys.exit()

    if not isNtfsFilesystem():
        windll.user32.MessageBoxA(0, 'This application must be run from an NTFS partition.', 'Error', 0)
        logger.critical('Aborting because system is not on NTFS partition.')
        sys.exit()

    if getScreenResolution() != (1920, 1080):
        windll.user32.MessageBoxA(0, 'This application must be run at 1920x1080 screen resolution.', 'Error', 0)
        logger.critical('Aborting because screen resolution is not 1920x1080.')
        sys.exit()

    if not isDesktopCompositionEnabled():
        windll.user32.MessageBoxA(0, 'This application requires that the Desktop Window Manager (DWM) is enabled.', 'Error', 0)
        logger.critical('Aborting because DWM is disabled.')
        sys.exit()

    # Hide unpacked directory.
    if getattr(sys, 'frozen', None):
        # FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM | FILE_ATTRIBUTE_NOT_CONTENT_INDEXED
        win32file.SetFileAttributesW(unicode(sys._MEIPASS), 2 | 4 | 8192)

    def _shutdown():
        # Presenter has been closed, now kick off clean-up tasks.
        stopOrchestrator()
        stopPlayer()
        stopAnalyzer()
        stopDownloader()

        # Block until all queue items have been processed.
        interProcessQueue.join()
        interProcessQueue.close()
        logger.info('Pending IPC items successfully processed.')

        # Gracefully stop processes.
        orchestrator.join()
        player.join()
        analyzer.join()
        downloader.join()
        logger.info('All processes gracefully terminated.')

        os.remove(certificateLocation)

        logger.info('Closing application.')
        logger.info('<' * 80)
        logger.info('')

        # Circumvent SystemExit exception handler.
        os._exit(1)

    # sys.excepthook = handleException

    if DEBUG:
        from scripts.packBlobs import run as runPackBlobs
        runPackBlobs()
    # END if DEBUG

    logger.info('>' * 80)
    logger.info('Starting application.')

    # Create AppData sub-folders.
    createAppStorageStructure()

    # Create DB connection here to initialize models.
    initStreamManager()

    userConfig = getCurrentUserConfig()

    try:
        serverPort = getVacantPort()
        if DEBUG:
            serverPort = 50000
        # END if DEBUG

        certificateLocation = getCertificateLocation()

        # Omni-directional message queue between boot process, collector process and server process.
        interProcessQueue = InterProcessQueue()

        downloader = startDownloader(interProcessQueue)
        analyzer = startAnalyzer(interProcessQueue)
        player = startPlayer(interProcessQueue)

        arguments = (getUserAgent(), serverPort, uuid4().hex, uuid4().hex, False, userConfig)

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
