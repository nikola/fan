# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import time
from multiprocessing import Process
from Queue import Empty

from models import StreamManager


def _startDownloader(queue):
    downloaderStreamManager = StreamManager()

    while True:
        try:
            command = queue.get_nowait()
            if command == 'downloader:stop':
                downloaderStreamManager.shutdown()

                queue.task_done()
                break
            else:
                queue.put(command)
                queue.task_done()
        except Empty:
            time.sleep(0.5)


def start(*args):
    global globalInterProcessQueue
    globalInterProcessQueue = args[0]

    process = Process(target=_startDownloader, args=args)
    process.start()

    return process


def stop():
    global globalInterProcessQueue
    globalInterProcessQueue.put('downloader:stop')
