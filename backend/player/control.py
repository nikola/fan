# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
import time
from subprocess import Popen
from multiprocessing import Process
from Queue import Empty

from models import StreamManager


def _startPlayer(queue):
    playerStreamManager = StreamManager()

    while True:
        try:
            command = queue.get_nowait()
            if command == 'player:stop':
                print 'attempting to shut down player stream manager ...'
                playerStreamManager.shutdown()
                print '... shut down player stream manager!'

                queue.task_done()
                break
            elif command.startswith('player:play:'):
                identifier = command[-32:]
                location = playerStreamManager.getStreamLocationByMovie(identifier)
                # print location

                process = Popen([
                    # os.path.join(PLAYER_AMALGAM_PATH, 'mpc-hc.exe'),
                    r'C:\Program Files (x86)\MPC-HC\mpc-hc.exe',
                    location,
                    '/play', '/close', '/fullscreen',
                ])
                process.wait()



                queue.task_done()
            else:
                queue.put(command)
                queue.task_done()
        except Empty:
            time.sleep(0.015)


def start(*args):
    global globalInterProcessQueue
    globalInterProcessQueue = args[0]

    process = Process(target=_startPlayer, args=args)
    process.start()

    return process


def stop():
    global globalInterProcessQueue
    globalInterProcessQueue.put('player:stop')
