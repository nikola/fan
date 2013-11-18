# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

from server import app

@app.route('/')
def hello(request):
    return "Hello, World!"
