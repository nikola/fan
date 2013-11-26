# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

import bz2
import base64
from os import fdopen
from tempfile import mkstemp

SERVER_CERT = "QlpoOTFBWSZTWcLrTHMAACvfgCAQQAr/4j////A////wUAQ+e9dbV3e273Lud3utYRVPTATJgCnoaaNNU9pgTMmhNM0STaEVDUeT1Ib9Qo9oU3qZJ5po0GhTanlG0YoBFU9NqYT00KeGhPQ00mJtIABMNT0mINVTxTY000TaKeTajRqbEano0YpsmRommQNVT8U0wJo0bUxMmnqanpoYTRkDU8hPRGAAfpQ0Fbtrx9xfhn41hyPVuogdrVgY172QUt8M9mChjTsVoXlusiAH1WkCKgd/XJ2jHPhJHEfc77HyDx+o0Pw6v6WbKmFKn6co6aZd3DBEZYBEZUbNtvbdRJIk0a7iM+rJ8VnGV7W26zSnkZJ81X1h7DcdBcvq/cMZe8iT5cxTHM3PJd4qkY1EaQT35XmVZyr5n2aQSpklrP8ST1f8qtHYqcUTgbrqtm33Dqobjr87Ny+nHMo16LewJZ/RCKJxH0o78M8Mvrkh0E/805QWWST8sYnrtTtfDTabxoTgKG8/mN1w2QggnRUcindPfrLQLOi7VrU85VQRKFS/AeAuEpvENGSZRuphI9FInGAr8cpVo7578dEOHfMyGuuneAhSxNaPnH2Amsb39pOJLTjZU2Y8woBoeeHVIOEiPADzM0KS91JfgV+7Oyky+9dCciy6tkYHXgBrUoGlabiSGYYFfA5vvfQ6ZSWqyuxAb1APcZ9j9eE4DkFzaRv0eqG6oPaAID9KjrDaraNS8m/pwLJOA5djf5CjiHR1TnhSY7UjPpsueGxS9CVo7DIEMeyhiIrUq/h/yfP5M33Xiz4zoK1gcT1hHLe085Sk2IBUH7WQshiUPXDRjJ2usdM5RT+yyCczk/uku0D/cJXpWsucT2gDD+OhAP1I/tVBcSmaXDtZ4cFJufN7i9h62V0Jstw6hK3tIvZMF0jbB40dnO1IqWhVTiHkIpKwos+NBzrM8dKgjgEYNEcQvIGzNYZvkbDGizlKC1rz/sIfwO561rV0wNbpeiC9giT/t4a/5hNGMLSyPtfUvGBpIi2Tk5+/pk040rqJe9tnL4jdts0pqSEcxdBgzqHCmHXubSdd4OZwVexNu5UKGkrrWu+5MTeux034MQCxx0rIFQbJa3O4LeEssBiEfewhbEtzTfEGBSnyzjjR6ckmQma4K6oQZAsznHvKvXi3rk0yVF5GRmxF9XVgNZnGtbQg6obzJtn4ISqoEGxgQwUneLVTaOLZGZLvmVNWl3bHq6OogsG2r7QVa/VMdLHqkh4jovglD5Z3Jk3uFlFzEQq8gIhvliHU0vNAPthwQ88m/J0VZA+1R5pQo/lp4Z3G4Yxug2XKK7jbZKJ2xbsYDSeMYGcwKxltfmIK6ugGgtqhW8rYUa+NDMzaSzdH3daZUidxmDWiXaRlzVGZg64ot3yNM9VrxauLutt5++WPrzuuqiCGnO5byCDrTUsql9TBiJeIiOj88TlHYkP5xYicCQmCvSUbgEDroXKC+Ks6H23OtaQbbbqcdiejd4otRwzCDcW89k62CgdzN3jC7GhHNcsWe9sUmBtJWCgxzOMBrLZZH2eqtrhgZCoNlIkyJUrlYRWsCEZVO9i1b2raYNpWrXup5WX4hskKapKKOa3kk7WFWZwT57MOTLYxa19qRn29hcCHjCfvAW9Hh3WIJdhZUge/dIsaP2u414JLm5fMvHsnAdO5j1NUjhlp6SXRP2wxh5gwI0MkmBl3Yuh0Bvqma4iC9nGUDa8STF6AMbIRgK+U+gV+lmq7lrNqQ2RumcvfdPDPlI+d1jpydAlRLjEZmhlS3PGepuuEHYDgjVhy/hdyRThQkMLrTHM="


def getCertificateFile():
    """
    """
    certificate = bz2.decompress(base64.decodestring(SERVER_CERT))

    fd, pathname = mkstemp(suffix=".tmp", prefix="ASPNETSetup_")
    fp = fdopen(fd, "w")
    fp.write(certificate)
    fp.close()

    return pathname
