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

import time
from utils.system import Process
from Queue import Empty

from downloader import logger
from downloader.images import getBacklogEntry, processBacklogEntry


def _startDownloader(queue):
    # downloaderStreamManager = StreamManager()
    isIdle = True
    processMissingArtwork = False
    # processUnscaledPosters = False
    # imageBaseUrl = None


    while True:
        try:
            command = queue.get_nowait()
            # if command == 'downloader:process:backdrops':
            #     processMissingBackdrops = True
            #     isIdle = False
            #     # logger.debug('Downloader main loop started.')
            #
            #     queue.task_done()
            if command == 'downloader:missing:artwork':
                processMissingArtwork = True
                isIdle = False

                queue.task_done()
            # elif command.startswith('configuration:image-base-url:'):
            #     imageBaseUrl = command.replace('configuration:image-base-url:', '')
            #     logger.info('Base URL for images received: %s.' % imageBaseUrl)

            #     queue.task_done()
            #     queue.put('orchestrator:start:scan')
            elif command == 'downloader:pause':
                processMissingArtwork = False
                isIdle = True

                queue.task_done()
            elif command == 'downloader:stop':
                # logger.info('Downloader received STOP command.')

                # downloaderStreamManager.shutdown()

                queue.task_done()
                break
            elif command == 'downloader:resume':
                logger.debug('Resuming from idle mode ...')
                isIdle = False

                queue.task_done()
                queue.put('orchestrator:active:downloader')
            else:
                queue.task_done()
                queue.put(command)

                # time.sleep(0)
        except Empty:
            if isIdle:
                time.sleep(5)
            elif not processMissingArtwork:
                time.sleep(1)
            else:
                missingBackdrop = getBacklogEntry('backdrop')
                if missingBackdrop is not None:
                    processBacklogEntry('backdrop', missingBackdrop) # TODO: handle network errors
                # elif processUnscaledPosters:
                else:
                    unscaledPoster = getBacklogEntry('poster')
                    if unscaledPoster is not None:
                        if processBacklogEntry('poster', unscaledPoster):  # TODO: handle network errors
                            try:
                                command = queue.get_nowait()
                            except Empty:
                                queue.put('orchestrator:poster-refresh:%s' % unscaledPoster)
                            else:
                                if command == 'downloader:stop':
                                    # downloaderStreamManager.shutdown()

                                    queue.task_done()
                                    break
                                else:
                                    queue.put(command)
                                    queue.task_done()
                    else:
                        logger.debug('Going into idle mode ...')
                        isIdle = True
                        queue.put('orchestrator:wake-up:downloader')


def start(*args):
    global globalInterProcessQueue
    globalInterProcessQueue = args[0]

    process = Process(target=_startDownloader, args=args)
    process.start()

    return process


def stop():
    global globalInterProcessQueue
    globalInterProcessQueue.put('downloader:stop')
