# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import time
from Queue import Empty
from multiprocessing import Process, Queue

from models import StreamManager


def _startWatcher(q, *args, **kwargs):
    streamManager = StreamManager()

    # command = q.get()
    # if command == 'work':
    #     print 'work'
    if True:
        while True:
            try:
                command = q.get_nowait()
                if command == 'stop':
                    streamManager.shutdown()
                    break
            except Empty:
                time.sleep(0.25)


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
    global globalWatcherQueue
    globalWatcherQueue = Queue()

    args += globalWatcherQueue,

    global globalWatcherProcess
    globalWatcherProcess = Process(target=_startWatcher, args=args)
    globalWatcherProcess.start()


def work():
    # TODO: refactor this into sending of commands between processes
    global globalWatcherQueue
    globalWatcherQueue.put('work')


def stop():
    global globalWatcherQueue
    globalWatcherQueue.put('stop')

    global globalWatcherProcess
    globalWatcherProcess.join()
    globalWatcherProcess.terminate()
