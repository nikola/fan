# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@generic.company)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

from multiprocessing import Process


def _startWatcher():
    pass


def start(*args):
    global globalWatcherProcess

    globalWatcherProcess = Process(target=_startWatcher, args=args)
    globalWatcherProcess.start()


def stop():
    global globalWatcherProcess

    globalWatcherProcess.terminate()
