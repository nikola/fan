# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import time
from multiprocessing import Process
from Queue import Empty

from downloader.images import downloadBackdrop, downscalePoster
from models import StreamManager


def _startDownloader(queue):
    downloaderStreamManager = StreamManager()
    isStarted = False

    while True:
        try:
            command = queue.get_nowait()
            if command == 'downloader:start':
                # TODO: only launch this when all poster images have been downloaded in frontend

                isStarted = True

                queue.task_done()
            elif command.startswith('configuration:image-base-url:'):
                imageBaseUrl = command.replace('configuration:image-base-url:', '')

                queue.task_done()
            elif command == 'downloader:stop':
                # print 'attempting to shut down downloader stream manager ...'
                downloaderStreamManager.shutdown()
                # print '... shut down downloader stream manager!'

                queue.task_done()
                break
            else:
                queue.put(command)
                queue.task_done()
        except Empty:
            if isStarted:
                # movieUuid = downloaderStreamManager.getMissingBackdropMovie()
                # if movieUuid is not None:
                #     print '%s needs a backdrop' % movieUuid
                #     downloadBackdrop(downloaderStreamManager, imageBaseUrl, movieUuid, True)
                # else:
                image = downloaderStreamManager.getUnscaledPosterImage()
                if image is not None:
                    downscalePoster(downloaderStreamManager, image)
                    # TODO: send websocket event to client to update poster
                else:
                    # print 'nothing to downscale'
                    pass
                time.sleep(0.5)
            else:
                time.sleep(0.015)


def start(*args):
    global globalInterProcessQueue
    globalInterProcessQueue = args[0]

    process = Process(target=_startDownloader, args=args)
    process.start()

    return process


def stop():
    global globalInterProcessQueue
    globalInterProcessQueue.put('downloader:stop')
