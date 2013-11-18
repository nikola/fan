# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

from server import app
from multiprocessing import Process
from pants.http import HTTPServer
from pants import Engine

def _startHttpServer(port):
    """
    """
    HTTPServer(app).listen(port)
    Engine.instance().start()

def start(port):
    """
    """
    global process
    process = Process(target=_startHttpServer, args=(port,))
    process.start()

def stop():
    """
    """
    global process
    process.terminate()
