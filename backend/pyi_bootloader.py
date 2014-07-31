# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import sys
import os
import time
import logging
from uuid import uuid4
from multiprocessing import JoinableQueue as InterProcessQueue, freeze_support
from Queue import Empty
from ctypes import windll

import win32file

from settings import DEBUG
from settings import LOG_CONFIG
from models import initialize as initStreamManager
from utils.system import isCompatiblePlatform, isNtfsFilesystem, getScreenResolution, isDesktopCompositionEnabled
from utils.agent import getUserAgent
from utils.net import getCertificateLocation
from utils.fs import getLogFileHandler
from utils.config import getCurrentUserConfig
from orchestrator.control import start as startOrchestrator, stop as stopOrchestrator
from downloader.control import start as startDownloader, stop as stopDownloader
from player.control import start as startPlayer, stop as stopPlayer
# from analyzer.control import start as startAnalyzer, stop as stopAnalyzer
from presenter.control import start as present


if __name__ == '__main__':
    freeze_support()

    def _shutdown():
        # Presenter has been closed, now kick off clean-up tasks.
        stopOrchestrator()
        stopPlayer()
        # stopAnalyzer()
        stopDownloader()

        # Remove pending commands from queue if not essential.
        while True:
            try:
                command = interProcessQueue.get_nowait()
            except Empty:
                break
            else:
                interProcessQueue.task_done()
                if command.find(':stop') != -1:
                    interProcessQueue.put(command)
                time.sleep(0.1)

        # Block until all queue items have been processed.
        interProcessQueue.join()
        interProcessQueue.close()
        # logger.info('Pending IPC items successfully processed.')

        # Gracefully stop processes.
        orchestrator.join()
        player.join()
        # analyzer.join()
        downloader.join()
        logger.info('All processes gracefully terminated.')

        os.remove(certificateLocation)

        logger.info('Closing application.')
        # logger.info('<' * 80)
        # logger.info('')

        # Circumvent SystemExit exception handler.
        os._exit(1)

    logging.basicConfig(**LOG_CONFIG)
    logger = logging.getLogger('core')
    logger.addHandler(getLogFileHandler('core'))

    try:
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

            # Enable SSL support in requests library when running as EXE.
            os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(sys._MEIPASS, 'requests', 'cacert.pem')

        # sys.excepthook = handleException

        if True: # DEBUG
            from scripts.packBlobs import run as runPackBlobs
            runPackBlobs()
        # END if DEBUG

        # logger.info('>' * 80)
        logger.info('Starting application.')

        # Create DB connection here to initialize models.
        initStreamManager()

        userConfig = getCurrentUserConfig()

        serverPort = 0xe95d # 59741
        certificateLocation = getCertificateLocation()

        # Omni-directional message queue between boot process, collector process and server process.
        interProcessQueue = InterProcessQueue()

        downloader = startDownloader(interProcessQueue)
        # analyzer = startAnalyzer(interProcessQueue)
        player = startPlayer(interProcessQueue)

        arguments = (getUserAgent(), serverPort, uuid4().hex, uuid4().hex, False, userConfig)

        # Start process, but spawn file scanner and watcher only after receiving a kick-off event from the presenter.
        orchestrator = startOrchestrator(interProcessQueue, certificateLocation, *arguments)

        # Start the blocking presenter process.
        present(_shutdown, *arguments)

        # TODO: implement SIGINT handler
        # http://stackoverflow.com/a/1112350
    except:
        logger.exception()
