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
__copyright__ = 'Copyright (C) 2013-2014 Nikola Klaric'

import sys
import os
import time
import re
import argparse
from multiprocessing import JoinableQueue as InterProcessQueue, freeze_support
from Queue import Empty
from ctypes import windll

import win32file

from settings import SERVER_PORT
from models import initialize as initStreamManager
from utils.system import isCompatiblePlatform, getScreenResolution, isDesktopCompositionEnabled, setPriority
from utils.fs import createAppStorageStructure
from utils.system import getCurrentInstanceIdentifier
from utils.config import processCurrentUserConfig
from utils.logs import getLogger
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
            logger.warning('Some processes forcefully terminated after grace period.')
        else:
            interProcessQueue.join()
            interProcessQueue.close()

            orchestrator.join()
            player.join()
            downloader.join()
            logger.info('All processes stopped.')

        logger.info('Closing application.')

        os._exit(1)

    logger = None

    try:
        if getattr(sys, 'frozen', None):
            win32file.SetFileAttributesW(unicode(sys._MEIPASS), 8198)

            os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(sys._MEIPASS, 'requests', 'cacert.pem')

        parser = argparse.ArgumentParser(
            prog='fan',
            description='A movie compilation and playback app for Windows. Fast. Lean. No weather widget.',
        )
        parser.add_argument('--profile', dest='profileIdentifier', action='store',
            help='Use the selected profile identifier for persistence of user data.')
        options = vars(parser.parse_args())

        profileIdentifier = options.get('profileIdentifier')
        if profileIdentifier:
             profileIdentifier = re.sub(r'[^a-zA-Z0-9\-_]', '', profileIdentifier)
        if not profileIdentifier:
            profileIdentifier = getCurrentInstanceIdentifier()

        createAppStorageStructure(profileIdentifier)

        logger = getLogger(profileIdentifier, 'application')

        logger.info('Starting application.')

        if not isCompatiblePlatform():
            windll.user32.MessageBoxA(0, 'This application is only compatible with Windows Vista or newer.', 'Error', 0)
            logger.critical('Aborting because system is not Windows Vista or newer.')
            sys.exit()

        if getScreenResolution() not in ((1920, 1080), (2560,1440)):
            windll.user32.MessageBoxA(0, 'This application must be run at 1920x1080 or 2560x1440 screen resolution.', 'Error', 0)
            logger.critical('Aborting because screen resolution is not 1920x1080 or 2560x1440.')
            sys.exit()

        if not isDesktopCompositionEnabled():
            windll.user32.MessageBoxA(0, 'This application requires that the Desktop Window Manager (DWM) is enabled.', 'Error', 0)
            logger.critical('Aborting because DWM is disabled.')
            sys.exit()

        initStreamManager(profileIdentifier)

        userConfig = processCurrentUserConfig(profileIdentifier)
        screen = 'configure' if not len(userConfig.get('sources', [])) and not userConfig.get('isDemoMode', False) else 'load'
        page = 'http://127.0.0.1:%d/%s.html' % (SERVER_PORT, screen)

        interProcessQueue = InterProcessQueue()

        arguments = (profileIdentifier, interProcessQueue)

        setPriority('idle')
        downloader = startDownloader(*arguments)
        player = startPlayer(*arguments)
        orchestrator = startOrchestrator(*arguments)

        setPriority('normal')
        present(_shutdown, page, *arguments)
    except Exception, e:
        if logger is not None:
            logger.exception(e)
