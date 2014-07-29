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
                # logger.info('Downloader main loop started.')

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
                logger.info('Resuming from idle mode ...')
                isIdle = False

                queue.task_done()
            else:
                queue.task_done()
                queue.put(command)
        except Empty:
            if doDownloadAssets and not isIdle:
                # time.sleep(0.5)

                movieUuid = downloaderStreamManager.getMissingBackdropMovieUuid()
                if movieUuid is not None:
                    if imageBaseUrl is not None:
                        logger.info('Must download backdrop for "%s".' % downloaderStreamManager.getMovieTitleByUuid(movieUuid))
                        downloadBackdrop(downloaderStreamManager, imageBaseUrl, movieUuid, True)
                else:
                    image = downloaderStreamManager.getUnscaledPosterImage()
                    if image is not None:
                        logger.info('Must downscale original poster image for "%s".' % downloaderStreamManager.getMovieTitleById(image.movieId))
                        movieUuid = downscalePoster(downloaderStreamManager, image)

                        if movieUuid is not None:
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
                        logger.info('Going into idle mode ...')
                        isIdle = True
                        queue.put('orchestrator:wake-up:downloader')
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
