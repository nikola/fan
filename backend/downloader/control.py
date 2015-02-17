# coding: utf-8
"""
fan - A movie compilation and playback app for Windows. Fast. Lean. No weather widget.
Copyright (C) 2013-2015 Nikola Klaric.

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
__copyright__ = 'Copyright (C) 2013-2015 Nikola Klaric'

import os
import time
from utils.system import Process
from Queue import Empty

from settings import APP_STORAGE_PATH
from downloader.images import getBacklogEntry, processBacklogEntry
from utils.logs import getLogger


def _startDownloader(profile, queue):
    isIdle = True
    processMissingArtwork = False
    logger = getLogger(profile, 'downloader')

    while True:
        try:
            command = queue.get_nowait()
            if command == 'downloader:process:missing:artwork':
                processMissingArtwork = True
                isIdle = False

                countUnprocessedPosters = sum(1 for _ in os.listdir(os.path.join(APP_STORAGE_PATH, 'backlog', 'posters')))
                time.sleep(0)

                queue.task_done()
                queue.put('orchestrator:push:pending:poster-count:%d' % countUnprocessedPosters)
            elif command == 'downloader:pause':
                processMissingArtwork = False
                isIdle = True

                queue.task_done()
            elif command == 'downloader:stop':
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

            time.sleep(0)
        except Empty:
            if isIdle:
                time.sleep(5)
            elif not processMissingArtwork:
                time.sleep(1)
            else:
                missingBackdrop = getBacklogEntry('backdrop')
                time.sleep(0)
                if missingBackdrop is not None:
                    processBacklogEntry(profile, 'backdrop', missingBackdrop) # TODO: handle network errors
                    time.sleep(0)
                else:
                    unscaledPoster = getBacklogEntry('poster')
                    time.sleep(0)
                    if unscaledPoster is not None:
                        processBacklogEntry(profile, 'poster', unscaledPoster)  # TODO: handle network errors
                        time.sleep(0)

                        queue.put('orchestrator:push:poster-decrement')
                        time.sleep(0)
                    else:
                        queue.put('orchestrator:push:posters-done')
                        time.sleep(0)

                        logger.debug('Assuming idle mode ...')
                        time.sleep(0)
                        isIdle = True
                        queue.put('orchestrator:wake-up:downloader')
                        time.sleep(0)


def start(*args):
    global globalInterProcessQueue
    globalInterProcessQueue = args[1]

    process = Process(target=_startDownloader, args=args)
    process.start()

    return process


def stop():
    global globalInterProcessQueue
    globalInterProcessQueue.put('downloader:stop')
