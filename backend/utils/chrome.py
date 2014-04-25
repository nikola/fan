# coding: utf-8
"""
 # chrome.exe –enable-easy-off-store-extension-install
    # https://code.google.com/p/chromium/issues/detail?id=138995
    # http://www.chromium.org/administrators/policy-list-3#ExtensionInstallSources

    # prompt to install extension: chrome.exe --new-window https://github.io/ka-boom


    # check for installation: C:\Users\Niko\AppData\Local\Google\Chrome SxS\User Data\Default\Web Applications\_crx_ainpgneglbdpnfikehealafocjcfaoei

    # Load specific version:
    # C:\Program Files (x86)\Google\Chrome\Application>chrome.exe --chrome-version="30.0.1599.101"

    # http://peter.sh/experiments/chromium-command-line-switches/

    # --app-id -> Specifies that the extension-app with the specified id should be launched according to its configuration.
    # ??? --force-app-mode -> Forces application mode. This hides certain system UI elements and forces the app to be installed if it hasn't been already.
    # ??? --enable-ephemeral-apps -> Enables experimentation with ephemeral apps, which are launched without installing in Chrome.
    #     --load-and-launch-app -> Loads an app from the specified directory and launches it.



    --host-rules
    Comma-separated list of rules that control how hostnames are mapped. For example: "MAP * 127.0.0.1" --> Forces all hostnames to be mapped to 127.0.0.1 "MAP *.google.com proxy" --> Forces all google.com subdomains to be resolved to "proxy". "MAP test.com [::1]:77 --> Forces "test.com" to resolve to IPv6 loopback. Will also force the port of the resulting socket address to be 77. "MAP * baz, EXCLUDE www.google.com" --> Remaps everything to "baz", except for "www.google.com". These mappings apply to the endpoint host in a net::URLRequest (the TCP connect and host resolver in a direct connection, and the CONNECT in an http proxy connection, and the endpoint host in a SOCKS proxy connection).



"""
__author__ = "Nikola Klaric (nikola@generic.company)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

import _winreg
import hashlib
from subprocess import Popen, PIPE, CREATE_NEW_PROCESS_GROUP


def getChromeExePath():
    """
    """
    registry = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
    try:
        key = _winreg.OpenKey(registry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe")
    except WindowsError:
        return None
    else:
        exePath = _winreg.QueryValueEx(key, "Path")[0]
        key.Close()
        return exePath


def getChromeApplicationId(pathname):
    """ C:\Users\Niko\Documents\GitHub\ka-BOOM\client
    """
    if len(pathname) > 1 and pathname[0].islower() and pathname[1] == ":":
        pathname = pathname[0].upper() + pathname[1:]

    pathname = pathname.encode("utf-16le")

    offset = ord("a")
    applicationId = "".join([chr(int(digit, 16) + offset) for digit in hashlib.sha256(pathname).hexdigest()[:32]])

    return applicationId


def launchChromeProcess():
    """
    # ALL WRONG??
    # --load-and-launch-app -> no installation, but runs

    # FIRST RUN:
    # --no-startup-window ?????
    # p = Popen('"C:\Users\Niko\AppData\Local\Google\Chrome SxS\Application\chrome.exe" --no-startup-window --load-and-launch-app=C:\Users\Niko\Documents\GitHub\ka-BOOM\client', stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)
    # p = Popen('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --no-startup-window --load-and-launch-app=C:\Users\Niko\Documents\GitHub\ka-BOOM\client', stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)

    # AFTER INSTALLATION:
    # p = Popen('"C:\Users\Niko\AppData\Local\Google\Chrome SxS\Application\chrome.exe" --app-id=ainpgneglbdpnfikehealafocjcfaoei', stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)

    """
    kwargs = {}
    DETACHED_PROCESS = 0x00000008
    kwargs.update(creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)

    p = Popen('"C:\Users\Niko\AppData\Local\Google\Chrome SxS\Application\chrome.exe" --no-startup-window --load-and-launch-app=C:\Users\Niko\Documents\GitHub\ka-BOOM\client', stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)
    assert not p.poll()

    # p.pid == The process ID of the child process

    """
    import ctypes

    def kill(pid):

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(1, 0, pid)
        return (0 != kernel32.TerminateProcess(handle, 0))
    """
