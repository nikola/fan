# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import time
from multiprocessing import Process
from Queue import Empty

from models import StreamManager

from . import playFile


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
                if isPlayerUpToDate:
                    playFile(playerStreamManager.getStreamLocationByMovie(command[-32:]))

                    queue.put('orchestrator:resume:detail')
                else:
                    queue.put(command)

                queue.task_done()
            else:
                queue.put(command)
                queue.task_done()
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
