# coding: utf-8
"""
fan - A movie compilation and playback app for Windows. Fast. Lean. No weather widget.
Copyright (C) 2013-2015 Nikola Klaric.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
__author__ = 'Nikola Klaric (nikola@klaric.org)'
__copyright__ = 'Copyright (C) 2013-2015 Nikola Klaric'

from subprocess import Popen

import win32api

from settings import APP_STORAGE_PATH
from settings.player import MPCHC_INI, MT_PATCH
from utils.logs import getLogger
from updater.lib import *


PLAYER_AMALGAM_PATH = os.path.join(APP_STORAGE_PATH, 'amalgam')


def _updateComponents(profile):
    def _log(text, *args):
        if text.strip():
            logger.info(text.strip())

    logger = getLogger(profile, 'updater')
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
            manifestXml = manifestXml.replace('</assembly>', (MT_PATCH + '</assembly>')).replace('\n', '')
            manifestXml = re.sub(' {2,}', '', manifestXml)

            handle = win32api.BeginUpdateResource(location, 0)
            win32api.UpdateResource(handle, 24, 1, manifestXml)
            win32api.EndUpdateResource(handle, 0)

            with open(location, 'a'):
                os.utime(location, None)


def _writeConfig():
    with open(os.path.join(PLAYER_AMALGAM_PATH, 'mpc-hc.ini'), 'wb') as fp:
        fp.write(MPCHC_INI)


def update(profile):
    if _updateComponents(profile):
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

    # kernel32 = ctypes.windll.kernel32
    # handle = kernel32.OpenProcess(1, 0, pid)
    # return (0 != kernel32.TerminateProcess(handle, 0))
