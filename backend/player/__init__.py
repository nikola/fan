# coding: utf-8
""" The secret sauce here is that if you change the EXE’s modification date time stamp,
    the loader will look again for a manifest.  This seems to work reliably every time.

    http://www.emailarchitect.net/easendmail/sdk/html/object_reg_a.htm
    http://www.s-code.com/kayako/index.php?_m=knowledgebase&_a=viewarticle&kbarticleid=64


"""
__author__ = "Nikola Klaric (nikola@generic.company)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

import sys
# import os
# import re
import win32api

from utils.win32 import getAppStoragePathname
# from updater.const import *
from updater.lib import *

PLAYER_AMALGAM_PATH = os.path.join(getAppStoragePathname(), 'amalgam')

MT_PATCH = """
    <file name="madVR.ax">
        <comClass clsid="{E1A8B82A-32CE-4B0D-BE0D-AA68C772E423}" threadingModel="Both" description="madVR"></comClass>
        <comClass clsid="{F352C9C1-D39D-4622-A279-978A60927CDE}" threadingModel="Both" description="madVR Property Page"></comClass>
    </file>
"""


def updateComponents():
    def log(text, color=BLACK):
        #  windll.Kernel32.SetConsoleTextAttribute(CONSOLE_HANDLER, color)
        sys.stdout.write(text)

    setLogger(log)

    components = [
        ('MPC-HC',
            Component(r'MPC-HC\MPC-HC',
                getLatestReleaseVersion = mpcHc_getLatestReleaseVersion,
                getInstalledVersion = mpcHc_getInstalledVersion,
                installLatestReleaseVersion = mpcHc_installLatestReleaseVersion,
            )
        ),
        ('LAV Filters',
            Component(LAVFILTERS_CLSID,
                getLatestReleaseVersion = lavFilters_getLatestReleaseVersion,
                getInstalledVersion = lavFilters_getInstalledVersion,
                installLatestReleaseVersion = lavFilters_installLatestReleaseVersion,
            )
        ),
        ('madVR',
            Component(MADVR_CLSID,
                getLatestReleaseVersion = madVr_getLatestReleaseVersion,
                getInstalledVersion = madVr_getInstalledVersion,
                installLatestReleaseVersion = madVr_installLatestReleaseVersion,
            )
        ),
    ]

    for name, instance in components:
        log('\n')

        latestVersion = getattr(instance, 'getLatestReleaseVersion')()
        if latestVersion is None:
            log('ERROR: Could not retrieve version info of the latest %s release.\n' % name, RED)
        else:
            log('Latest release version of %s: %s\n' % (name, latestVersion))

            installedVersion, detectedInstallationPath = instance.getInstalledVersion(PLAYER_AMALGAM_PATH)
            mustInstall = False
            if installedVersion is not None:
                log('Installed version: %s\n\t%s\n' % (installedVersion, detectedInstallationPath))

                if not installedVersion or getVersionTuple(installedVersion) < getVersionTuple(latestVersion):
                    mustInstall = True
                else:
                    log('%s does not need to be updated.\n' % name, GREEN)
            else:
                log('%s does not seem to be installed on the local machine.\n' % name)
                mustInstall = True

            if mustInstall:
                try:
                    getattr(instance, 'installLatestReleaseVersion')(latestVersion, PLAYER_AMALGAM_PATH, False, True, True)
                except Exception, e:
                    log(' ERROR: %s\n' % e.message, RED)
                else:
                    currentInstalledVersion, currentInstallationPath = instance.getInstalledVersion(PLAYER_AMALGAM_PATH)
                    if currentInstallationPath is None or getVersionTuple(currentInstalledVersion) != getVersionTuple(latestVersion):
                        log('\nFailed to %s %s %s.\n'
                            % ('update to' if installedVersion is not None else 'install', name, latestVersion), RED)
                    else:
                        log(' done.\n')
                        if detectedInstallationPath != currentInstallationPath:
                            log('%s %s is now installed in:\n\t%s\n'
                                % (name, latestVersion, currentInstallationPath))
                            if installedVersion is not None:
                                log('Your previous installation of %s %s remains in:\n\t%s\n'
                                    % (name, installedVersion, detectedInstallationPath))
                        log('Successfully %s %s. No errors.\n'
                            % ('updated' if installedVersion is not None else 'installed', name), GREEN)


def patchMpcHcManifest():
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
            manifestXml = manifestXml.replace('</assembly>', MT_PATCH.strip() + '</assembly>').replace('\n', '')
            manifestXml = re.sub(' {2,}', '', manifestXml)

            handle = win32api.BeginUpdateResource(location, 0)
            win32api.UpdateResource(handle, 24, 1, manifestXml)
            win32api.EndUpdateResource(handle, 0)

            # Touch file.
            with open(location, 'a'):
                os.utime(location, None)
