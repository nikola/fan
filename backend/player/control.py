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

from models import StreamManager

from . import playFile, update as updatePlayer


def _startPlayer(queue):
    playerStreamManager = StreamManager()

    isPlayerUpToDate = False

    while True:
        try:
            command = queue.get_nowait()

            if command == 'player:up-to-date':
                isPlayerUpToDate = True

                queue.task_done()
            elif command == 'player:stop':
                playerStreamManager.shutdown()

                queue.task_done()
                break
            elif command.startswith('player:play:'):
                if not isPlayerUpToDate:
                    updatePlayer()
                    isPlayerUpToDate = True
                queue.put('orchestrator:player:updated')

                streamLocation = playerStreamManager.getStreamLocationById(command[12:])
                if streamLocation is not None:
                    playFile(streamLocation)

                queue.task_done()

                queue.put('orchestrator:resume:detail')
            else:
                queue.task_done()
                queue.put(command)

                time.sleep(0.015)
        except Empty:
            time.sleep(0.5)


def start(*args):
    global globalInterProcessQueue
    globalInterProcessQueue = args[0]

    process = Process(target=_startPlayer, args=args)
    process.start()

    return process


def stop():
    global globalInterProcessQueue
    globalInterProcessQueue.put('player:stop')
