# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import time
from utils.system import Process
from Queue import Empty

from downloader.images import downloadBackdrop, downscalePoster
from models import StreamManager

from . import logger


def _startDownloader(queue):
    downloaderStreamManager = StreamManager()
    doDownloadAssets = False
    imageBaseUrl = None
    isIdle = False

    while True:
        try:
            command = queue.get_nowait()
            if command == 'downloader:start':
                # TODO: only launch this when all poster images have been downloaded in frontend

                doDownloadAssets = True
                logger.debug('Downloader main loop started.')

                queue.task_done()
            elif command.startswith('configuration:image-base-url:'):
                imageBaseUrl = command.replace('configuration:image-base-url:', '')
                logger.info('Base URL for images received: %s.' % imageBaseUrl)

                queue.task_done()

                queue.put('orchestrator:start:scan')
            elif command == 'downloader:stop':
                # logger.info('Downloader received STOP command.')

                downloaderStreamManager.shutdown()

                queue.task_done()
                break
            elif command == 'downloader:resume':
                logger.debug('Resuming from idle mode ...')
                isIdle = False

                queue.task_done()
                queue.put('orchestrator:active:downloader')
            else:
                queue.task_done()
                queue.put(command)

                time.sleep(0.015)
        except Empty:
            if doDownloadAssets and not isIdle:
                time.sleep(0.015)

                movieUuid = downloaderStreamManager.getMissingBackdropMovieUuid()
                if movieUuid is not None:
                    time.sleep(0.015)
                    if imageBaseUrl is not None:
                        downloadBackdrop(downloaderStreamManager, imageBaseUrl, movieUuid, True)
                else:
                    time.sleep(0.015)

                    movieUuid, urlOriginal = downloaderStreamManager.getUnscaledPosterImage()
                    if movieUuid is not None:
                        time.sleep(0.015)

                        success = downscalePoster(downloaderStreamManager, movieUuid, urlOriginal)
                        time.sleep(0.015)

                        if success:
                            try:
                                command = queue.get_nowait()
                            except Empty:
                                queue.put('orchestrator:poster-refresh:%s' % movieUuid)
                            else:
                                if command == 'downloader:stop':
                                    downloaderStreamManager.shutdown()

                                    queue.task_done()
                                    break
                                else:
                                    queue.put(command)
                                    queue.task_done()
                    else:
                        logger.debug('Going into idle mode ...')
                        isIdle = True
                        queue.put('orchestrator:wake-up:downloader')
                        time.sleep(0.015)
            else:
                if isIdle:
                    time.sleep(2)
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
