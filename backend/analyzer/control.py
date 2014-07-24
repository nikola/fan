# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import time
from utils.system import Process
from Queue import Empty

from models import StreamManager


def _startAnalyzer(queue):
    streamManager = StreamManager()
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
    globalInterProcessQueue = args[0]

    process = Process(target=_startAnalyzer, args=args)
    process.start()

    return process


def stop():
    global globalInterProcessQueue
    globalInterProcessQueue.put('analyzer:stop')
