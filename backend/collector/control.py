# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import time
from Queue import Empty
from multiprocessing import Process

from models import StreamManager


def _startWatcher(queue, *args, **kwargs):
    while True:
        try:
            command = queue.get_nowait()
            if command == 'start:collector':
                streamManager = StreamManager()
                queue.task_done()
            elif command == 'stop:StreamManager':
                streamManager.shutdown()
                queue.task_done()
                break
            else:
                queue.put(command)
                queue.task_done()
        except Empty:
            time.sleep(0.015)


def _dummy():
    """
        for (path, container, files) in getMoviePathnames(r"M:\\"):
            basedata = getBasedataFromPathname(container)

            for filename in files:
                streamLocation = os.path.join(path, filename)
                print streamLocation
                continue

                print "processing %s" % streamLocation
                movieRecord = getMovieFromRawData("de", "de", basedata["title"], basedata["year"])
                if movieRecord is None: continue

                print "adding %s from %s" % (movieRecord["titleOriginal"], streamLocation)
                streamManager.addMovieStream(movieRecord, streamLocation)

                time.sleep(0.5)
    """


def start(*args):
    global globalInterProcessQueue
    globalInterProcessQueue = args[0]

    process = Process(target=_startWatcher, args=args)
    process.start()

    return process


def stop():
    global globalInterProcessQueue
    globalInterProcessQueue.put('stop:StreamManager')
