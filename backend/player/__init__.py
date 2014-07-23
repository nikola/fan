# coding: utf-8
""" The secret sauce here is that if you change the EXE’s modification date time stamp,
    the loader will look again for a manifest.  This seems to work reliably every time.

    http://www.emailarchitect.net/easendmail/sdk/html/object_reg_a.htm
    http://www.s-code.com/kayako/index.php?_m=knowledgebase&_a=viewarticle&kbarticleid=64

    DSVidRen=12 -> madVR
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import logging
from subprocess import Popen

import win32api
from pylzma import decompress as uppercase

from settings import LOG_CONFIG, APP_STORAGE_PATH, BASE_DIR
from utils.fs import getLogFileHandler
from updater.lib import *


PLAYER_AMALGAM_PATH = os.path.join(APP_STORAGE_PATH, 'amalgam')

MT_PATCH = """
    <file name="madVR.ax">
        <comClass clsid="{E1A8B82A-32CE-4B0D-BE0D-AA68C772E423}" threadingModel="Both" description="madVR"></comClass>
        <comClass clsid="{F352C9C1-D39D-4622-A279-978A60927CDE}" threadingModel="Both" description="madVR Property Page"></comClass>
    </file>
    <file name="LAVSplitter.ax">
        <comClass clsid="{171252A0-8820-4AFE-9DF8-5C92B2D66B04}" threadingModel="Both" description="LAV Splitter"></comClass>
        <comClass clsid="{A19DE2F2-2F74-4927-8436-61129D26C141}" threadingModel="Both" description="LAV Splitter Properties"></comClass>
        <comClass clsid="{B98D13E7-55DB-4385-A33D-09FD1BA26338}" threadingModel="Both" description="LAV Splitter Source"></comClass>
        <comClass clsid="{56904B22-091C-4459-A2E6-B1F4F946B55F}" threadingModel="Both" description="LAV Splitter Input Formats"></comClass>
    </file>
    <file name="LAVAudio.ax">
        <comClass clsid="{E8E73B6B-4CB3-44A4-BE99-4F7BCB96E491}" threadingModel="Both" description="LAV Audio Decoder"></comClass>
        <comClass clsid="{2D8F1801-A70D-48F4-B76B-7F5AE022AB54}" threadingModel="Both" description="LAV Audio Properties"></comClass>
        <comClass clsid="{BD72668E-6BFF-4CD1-8480-D465708B336B}" threadingModel="Both" description="LAV Audio Format Settings"></comClass>
        <comClass clsid="{20ED4A03-6AFD-4FD9-980B-2F6143AA0892}" threadingModel="Both" description="LAV Audio Status"></comClass>
        <comClass clsid="{C89FC33C-E60A-4C97-BEF4-ACC5762B6404}" threadingModel="Both" description="LAV Audio Mixer"></comClass>
    </file>
    <file name="LAVVideo.ax">
        <comClass clsid="{EE30215D-164F-4A92-A4EB-9D4C13390F9F}" threadingModel="Both" description="LAV Video Decoder"></comClass>
        <comClass clsid="{278407C2-558C-4BED-83A0-B6FA454200BD}" threadingModel="Both" description="LAV Video Properties"></comClass>
        <comClass clsid="{2D4D6F88-8B41-40A2-B297-3D722816648B}" threadingModel="Both" description="LAV Video Format Settings"></comClass>
    </file>
"""

logging.basicConfig(**LOG_CONFIG)
logger = logging.getLogger('player')
logger.addHandler(getLogFileHandler('player'))


def _updateComponents():
    def _log(text, color=BLACK):
        logger.info(text)

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
        _log('\n')

        pathname = os.path.join(PLAYER_AMALGAM_PATH, filename)

        try:
            latestVersion = getattr(instance, 'getLatestReleaseVersion')()
        except:
            _log('ERROR: Could not retrieve version info of the latest %s release.\n' % name, RED)
        else:
            _log('Latest release version of %s: %s\n' % (name, latestVersion))

            mustInstall = False
            installedVersion, detectedInstallationPath = instance.getInstalledVersion(pathname)
            if installedVersion is not None:
                _log('Installed version: %s\n\t%s\n' % (installedVersion, detectedInstallationPath))

                if not installedVersion or getVersionTuple(installedVersion) < getVersionTuple(latestVersion):
                    mustInstall = True
                else:
                    _log('%s does not need to be updated.\n' % name, GREEN)
            else:
                _log('%s does not seem to be installed on the local machine.\n' % name)
                mustInstall = True

            if mustInstall:
                getattr(instance, 'installLatestReleaseVersion')(latestVersion, PLAYER_AMALGAM_PATH, silent=False, archive=True, compact=True, compatText=True)

                currentInstalledVersion, currentInstallationPath = instance.getPostInstallVersion(pathname)
                if currentInstallationPath is None or getVersionTuple(currentInstalledVersion) != getVersionTuple(latestVersion):
                    _log('\nFailed to %s %s %s.\n'
                        % ('update to' if installedVersion is not None else 'install', name, latestVersion), RED)
                else:
                    _log(' done.\n')
                    if detectedInstallationPath != currentInstallationPath:
                        _log('%s %s is now installed in:\n\t%s\n'
                            % (name, latestVersion, currentInstallationPath))
                        if installedVersion is not None:
                            _log('Your previous installation of %s %s remains in:\n\t%s\n'
                                % (name, installedVersion, detectedInstallationPath))
                    _log('Successfully %s %s. No errors.\n'
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
            manifestXml = manifestXml.replace('</assembly>', MT_PATCH.strip() + '</assembly>').replace('\n', '')
            manifestXml = re.sub(' {2,}', '', manifestXml)

            handle = win32api.BeginUpdateResource(location, 0)
            win32api.UpdateResource(handle, 24, 1, manifestXml)
            win32api.EndUpdateResource(handle, 0)

            # Touch file.
            with open(location, 'a'):
                os.utime(location, None)


def _writeConfig():
    with open(os.path.join(BASE_DIR, 'backend', 'filters', '4ebc0ca1e8324ba6a134ca78b1ca3088'), 'rb') as fp:
        string = fp.read()
    with open(os.path.join(PLAYER_AMALGAM_PATH, 'mpc-hc.ini'), 'wb') as fp:
        fp.write(uppercase(string))


def update():
    if _updateComponents():
        _patchManifest()
        _writeConfig()


def playFile(location):
    process = Popen([
        os.path.join(PLAYER_AMALGAM_PATH, 'mpc-hc.exe'),
        location,
        '/play', '/close', '/fullscreen',
    ])
    process.wait()
