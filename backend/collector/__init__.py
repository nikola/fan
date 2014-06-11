# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

from settings.collector import THEMOVIEDB_API_KEY
from utils.net import makeThrottledGetRequest


def getImageConfiguration():
    response = makeThrottledGetRequest('https://api.themoviedb.org/3/configuration', params={'api_key': THEMOVIEDB_API_KEY})
    configuration = response.json()

    # ["w92","w154","w185","w342","w500","w780","original"]
    sizes = configuration.get('images').get('poster_sizes')
    if 'original' in sizes: sizes.remove('original')
    closestWidth = min(sizes, key=lambda x: abs(int(x[1:]) - 300))
    if int(closestWidth[1:]) < 300:
        closestWidth = sizes[sizes.index(closestWidth) + 1]

    print 'closest width: ', closestWidth

    return configuration.get('images').get('secure_base_url'), closestWidth
