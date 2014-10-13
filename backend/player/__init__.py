# coding: utf-8
""" The secret sauce here is that if you change the EXE’s modification date time stamp,
    the loader will look again for a manifest.  This seems to work reliably every time.

    http://www.emailarchitect.net/easendmail/sdk/html/object_reg_a.htm
    http://www.s-code.com/kayako/index.php?_m=knowledgebase&_a=viewarticle&kbarticleid=64

    DSVidRen=12 -> madVR
"""
__author__ = 'Nikola Klaric (nikola@klaric.org)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import logging
from subprocess import Popen # , PIPE, CREATE_NEW_PROCESS_GROUP

import win32api
from utils.fs import readProcessedStream

from settings import DEBUG
from settings import LOG_CONFIG, APP_STORAGE_PATH
from utils.fs import getLogFileHandler
from updater.lib import *


PLAYER_AMALGAM_PATH = os.path.join(APP_STORAGE_PATH, 'amalgam')


logging.basicConfig(**LOG_CONFIG)
logger = logging.getLogger('updater')
logger.propagate = DEBUG
logger.addHandler(getLogFileHandler('updater'))


def _updateComponents():
    def _log(text, color=BLACK):
        if text.strip():
            logger.info(text.strip())

    setLogger(_log)

    components = [
        ('MPC-HC', 'mpc-hc.exe',
            Component(r'MPC-HC\MPC-HC',
                getLatestReleaseVersion = mpcHc_getLatestReleaseVersion,
                getInstalledVersion = mpcHc_getInstalledVersion,
                installLatestReleaseVersion = mpcHc_installLatestReleaseVersion,
            )
        ),
        ('LAV Filters', 'LAVSplitter.ax',
            Component(LAVFILTERS_CLSID,
                getLatestReleaseVersion = lavFilters_getLatestReleaseVersion,
                getInstalledVersion = lavFilters_getInstalledVersion,
                installLatestReleaseVersion = lavFilters_installLatestReleaseVersion,
            )
        ),
        ('madVR', 'madVR.ax',
            Component(MADVR_CLSID,
                getLatestReleaseVersion = madVr_getLatestReleaseVersion,
                getInstalledVersion = madVr_getInstalledVersion,
                installLatestReleaseVersion = madVr_installLatestReleaseVersion,
            )
        ),
    ]

    mpcHcVersionSnapshot = components[0][2].getInstalledVersion(os.path.join(PLAYER_AMALGAM_PATH, 'mpc-hc.exe'))[0]

    for name, filename, instance in components:
        pathname = os.path.join(PLAYER_AMALGAM_PATH, filename)

        try:
            latestVersion = getattr(instance, 'getLatestReleaseVersion')()
        except:
            _log('ERROR: Could not retrieve version info of the latest %s release.' % name, RED)
        else:
            _log('Latest release version of %s: %s' % (name, latestVersion))

            mustInstall = False
            installedVersion, detectedInstallationPath = instance.getInstalledVersion(pathname)
            if installedVersion is not None:
                _log('Installed version: %s' % installedVersion)

                if not installedVersion or getVersionTuple(installedVersion) < getVersionTuple(latestVersion):
                    mustInstall = True
                else:
                    _log('%s does not need to be updated.' % name, GREEN)
            else:
                _log('%s does not seem to be installed on the local machine.' % name)
                mustInstall = True

            if mustInstall:
                getattr(instance, 'installLatestReleaseVersion')(latestVersion, PLAYER_AMALGAM_PATH, silent=False, archive=True, compact=True, compatText=True)

                currentInstalledVersion, currentInstallationPath = instance.getPostInstallVersion(pathname)
                if currentInstallationPath is None or getVersionTuple(currentInstalledVersion) != getVersionTuple(latestVersion):
                    _log('\nFailed to %s %s %s.'
                        % ('update to' if installedVersion is not None else 'install', name, latestVersion), RED)
                else:
                    _log(' done.\n')
                    if detectedInstallationPath != currentInstallationPath:
                        _log('%s %s is now installed.'
                            % (name, latestVersion))
                        if installedVersion is not None:
                            pass
                    _log('Successfully %s %s. No errors.'
                        % ('updated' if installedVersion is not None else 'installed', name), GREEN)

    mpcHcVersionCurrent = components[0][2].getInstalledVersion(os.path.join(PLAYER_AMALGAM_PATH, 'mpc-hc.exe'))[0]
    return mpcHcVersionSnapshot is None or mpcHcVersionSnapshot != mpcHcVersionCurrent


def _patchManifest():
    location = os.path.join(PLAYER_AMALGAM_PATH, 'mpc-hc.exe')

    handle = win32api.LoadLibraryEx(location, None, 0x20)
    try:
        manifestXml = win32api.LoadResource(handle, 24, 1)
    except:
        manifestXml = None
    finally:
        win32api.FreeLibrary(handle)

    if manifestXml is not None:
        if manifestXml.find('<file name="madVR.ax">') == -1:
            manifestXml = manifestXml.replace('</assembly>', readProcessedStream('d2062963ddf644299341f12439990aa8') + '</assembly>').replace('\n', '')
            manifestXml = re.sub(' {2,}', '', manifestXml)

            handle = win32api.BeginUpdateResource(location, 0)
            win32api.UpdateResource(handle, 24, 1, manifestXml)
            win32api.EndUpdateResource(handle, 0)

            # Touch file.
            with open(location, 'a'):
                os.utime(location, None)


def _writeConfig():
    with open(os.path.join(PLAYER_AMALGAM_PATH, 'mpc-hc.ini'), 'wb') as fp:
        fp.write(readProcessedStream('4ebc0ca1e8324ba6a134ca78b1ca3088'))


def update():
    if _updateComponents():
        _patchManifest()
        _writeConfig()


def playFile(location):
    # kwargs = {}
    # DETACHED_PROCESS = 0x00000008
    # kwargs.update(creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)

    process = Popen([
        os.path.join(PLAYER_AMALGAM_PATH, 'mpc-hc.exe'),
        location,
        '/play', '/close', '/fullscreen',
    ]) # , stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)
    process.wait()
