# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@generic.company)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

import time
from Queue import Empty
from multiprocessing import Process, Queue

from models import StreamManager


def _startWatcher(q, *args, **kwargs):
    streamManager = StreamManager()

    # TODO: wait a few seconds until presenter is ready

    while True:
        try:
            command = q.get(False)
            if command == 'stop':
                streamManager.shutdown()
                break
        except Empty:
            time.sleep(0.25)


def start(*args):
    global globalWatcherQueue
    globalWatcherQueue = Queue()

    args += globalWatcherQueue,

    global globalWatcherProcess
    globalWatcherProcess = Process(target=_startWatcher, args=args)
    globalWatcherProcess.start()


def stop():
    global globalWatcherQueue
    globalWatcherQueue.put('stop')

    global globalWatcherProcess
    globalWatcherProcess.join()
    globalWatcherProcess.terminate()
