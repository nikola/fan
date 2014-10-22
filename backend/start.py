# coding: utf-8
"""
fan - A movie compilation and playback app for Windows. Fast. Lean. No weather widget.
Copyright (C) 2013-2014 Nikola Klaric.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
__author__ = 'Nikola Klaric (nikola@klaric.org)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import sys
import os
import time
import logging
import argparse
from multiprocessing import JoinableQueue as InterProcessQueue, freeze_support
from Queue import Empty
from ctypes import windll

import win32file

from settings import DEBUG
from settings import LOG_CONFIG
from models import initialize as initStreamManager
from utils.system import isCompatiblePlatform, getScreenResolution, isDesktopCompositionEnabled, setPriority
from utils.fs import getLogFileHandler
from utils.config import getCurrentUserConfig, getOverlayConfig, exportUserConfig
from orchestrator.control import start as startOrchestrator, stop as stopOrchestrator
from downloader.control import start as startDownloader, stop as stopDownloader
from player.control import start as startPlayer, stop as stopPlayer
from presenter.control import start as present


if __name__ == '__main__':
    freeze_support()

    def _shutdown():
        stopOrchestrator()
        stopPlayer()
        stopDownloader()

        counter = 0
        unsafe = False
        while True:
            try:
                command = interProcessQueue.get_nowait()
            except Empty:
                break
            else:
                interProcessQueue.task_done()
                if command.find(':stop') != -1:
                    interProcessQueue.put(command)
                counter += 1
                if counter > 600:
                    orchestrator.terminate()
                    player.terminate()
                    downloader.terminate()
                    unsafe = True
                else:
                    time.sleep(0.1)

        if unsafe:
            interProcessQueue.cancel_join_thread()
            interProcessQueue.close()
            logger.warning('All processes forcefully terminated after grace period.')
        else:
            interProcessQueue.join()
            interProcessQueue.close()

            orchestrator.join()
            player.join()
            downloader.join()
            logger.info('All processes stopped.')

        logger.info('Closing application.')

        os._exit(1)

    logging.basicConfig(**LOG_CONFIG)
    logger = logging.getLogger('core')
    logger.propagate = DEBUG
    logger.addHandler(getLogFileHandler('core')) # Implicitly create app storage folder structure.

    try:
        if not isCompatiblePlatform():
            windll.user32.MessageBoxA(0, 'This application is only compatible with Windows Vista or newer.', 'Error', 0)
            logger.critical('Aborting because system is not Windows Vista or newer.')
            sys.exit()

        if getScreenResolution() != (1920, 1080):
            windll.user32.MessageBoxA(0, 'This application must be run at 1920x1080 screen resolution.', 'Error', 0)
            logger.critical('Aborting because screen resolution is not 1920x1080.')
            sys.exit()

        if not isDesktopCompositionEnabled():
            windll.user32.MessageBoxA(0, 'This application requires that the Desktop Window Manager (DWM) is enabled.', 'Error', 0)
            logger.critical('Aborting because DWM is disabled.')
            sys.exit()

        if getattr(sys, 'frozen', None):
            win32file.SetFileAttributesW(unicode(sys._MEIPASS), 8198)

            os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(sys._MEIPASS, 'requests', 'cacert.pem')

        logger.info('Starting application.')

        useExternalConfig = None

        parser = argparse.ArgumentParser(
            prog='fan',
            description='A movie compilation and playback app for Windows. Fast. Lean. No weather widget.',
        )

        # TODO: add arguments --profile and --purge-artifacts (for removing intermediate poster images)

        parser.add_argument('--export-config', dest='exportConfigPath', action='store',
            help='Write the current configuration to the given path.')
        parser.add_argument('--load-config', dest='loadConfigPath', action='store',
            help='Use the configuration from the given path.')

        options = vars(parser.parse_args())

        loadConfigPathname = options.get('loadConfigPath')
        if loadConfigPathname is not None:
            if os.path.exists(loadConfigPathname) and os.path.isfile(loadConfigPathname):
                userConfig = getOverlayConfig(loadConfigPathname)
                useExternalConfig = loadConfigPathname
            else:
                logger.error('Configuration not found: %s' % loadConfigPathname)
                sys.exit(1)
        else:
            userConfig = getCurrentUserConfig()

        if options.get('exportConfigPath') is not None:
            exportConfigPathname = options.get('exportConfigPath')
            exportUserConfig(userConfig, exportConfigPathname)
            logger.info('Current configuration saved in: %s' % exportConfigPathname)
            sys.exit()

        initStreamManager()

        serverPort = 59741

        arguments = (serverPort, userConfig, useExternalConfig)

        interProcessQueue = InterProcessQueue()

        setPriority('idle')
        downloader = startDownloader(interProcessQueue)
        player = startPlayer(interProcessQueue)

        orchestrator = startOrchestrator(interProcessQueue, *arguments)

        setPriority('normal')
        present(_shutdown, *arguments)
    except Exception, e:
        logger.exception(e)
