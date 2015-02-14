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

import time
from utils.system import Process
from Queue import Empty

from models import StreamManager


def _startAnalyzer(profile, queue):
    streamManager = StreamManager(profile)
    isStarted = False

    while True:
        try:
            command = queue.get_nowait()
            if command == 'analyzer:start':
                # TODO: only launch this when all poster images have been downloaded in frontend

                isStarted = True

                queue.task_done()
            elif command == 'analyzer:stop':
                streamManager.shutdown()

                queue.task_done()
                break
            else:
                queue.put(command)
                queue.task_done()
        except Empty:
            if isStarted:
                time.sleep(0.5)
            else:
                time.sleep(0.015)


def start(*args):
    global globalInterProcessQueue
    globalInterProcessQueue = args[1]

    process = Process(target=_startAnalyzer, args=args)
    process.start()

    return process


def stop():
    global globalInterProcessQueue
    globalInterProcessQueue.put('analyzer:stop')
