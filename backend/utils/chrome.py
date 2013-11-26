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
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

import sys
import os
import re
import time
import traceback
import codecs
import struct
import _winreg
import hashlib
import uuid
from subprocess import Popen, PIPE, CREATE_NEW_PROCESS_GROUP
from vendor.cef import cefpython_py27 as cefpython
import win32con
import win32gui
import win32api
from urllib import pathname2url as urllib_pathname2url
from config import *
from utils.win32 import getNormalizedPathname

DEBUG = True


def handleException(excType, excValue, traceObject):
    """
    """
    errorMsg = "\n".join(traceback.format_exception(excType, excValue, traceObject))

    if type(errorMsg) == bytes:
        errorMsg = errorMsg.decode(encoding="utf-8", errors="replace")

    try:
        with codecs.open(getNormalizedPathname("error.log"), mode="a", encoding="utf-8") as fp:
            fp.write("\n[%s] %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), errorMsg))
    except:
        pass

    errorMsg = errorMsg.encode("ascii", errors="replace").decode("ascii", errors="replace")
    print("\n%s\n" % errorMsg)

    stopChromeContainer()
    os._exit(1)


def execChromeContainer(agent, url, callback):
    """
    """
    # Memorize callback function that must be executed before shutting down the CEF container.
    global onCloseCallback
    onCloseCallback = callback

    cefpython.g_debug = DEBUG
    cefpython.g_debugFile = getNormalizedPathname("debug.log")

    cefpython.Initialize(dict(
        log_file                  = getNormalizedPathname("debug.log"),
        log_severity              = cefpython.LOGSEVERITY_INFO,
        release_dcheck_enabled    = DEBUG, # Disable in production
        browser_subprocess_path   = "%s/%s" % (cefpython.GetModuleDirectory(), "subprocess"),
        user_agent                = agent,
        ignore_certificate_errors = True,
        remote_debugging_port     = 8090,
    ))

    windowId = createChromeWindow(
        title = "ka-BOOM",
        className = "kaboom_%s" % uuid.uuid4().hex,
        iconPathname = getNormalizedPathname("../vendor/cef/icon.ico"),
    )

    windowInfo = cefpython.WindowInfo()
    windowInfo.SetAsChild(windowId)

    browser = cefpython.CreateBrowserSync(
        windowInfo,
        CHROME_BROWSER_SETTINGS,
        navigateUrl=url, # r"C:/Users/Niko/Documents/GitHub/ka-BOOM/backend/vendor/cef/example.html",
    )
    browser.ToggleFullscreen()

    cefpython.MessageLoop()
    cefpython.Shutdown()


def stopChromeContainer():
    """
    """
    cefpython.QuitMessageLoop()
    cefpython.Shutdown()


def createChromeWindow(title, className, iconPathname, width=1920, height=1080, xpos=0, ypos=0):
    """
    """
    wndclass = win32gui.WNDCLASS()
    wndclass.hInstance = win32api.GetModuleHandle(None)
    wndclass.lpszClassName = className
    wndclass.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
    wndclass.hbrBackground = win32con.COLOR_WINDOW
    wndclass.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wndclass.lpfnWndProc = {
        win32con.WM_CLOSE: CloseWindow,
        win32con.WM_DESTROY: QuitApplication,
        win32con.WM_SIZE: cefpython.WindowUtils.OnSize,
        win32con.WM_SETFOCUS: cefpython.WindowUtils.OnSetFocus,
        win32con.WM_ERASEBKGND: cefpython.WindowUtils.OnEraseBackground
    }
    win32gui.RegisterClass(wndclass)

    windowID = win32gui.CreateWindow(
        className,
        title,
        win32con.WS_OVERLAPPEDWINDOW | win32con.WS_CLIPCHILDREN | win32con.WS_VISIBLE,
        xpos, ypos, width, height,
        0, # parent
        0, # menu
        wndclass.hInstance,
        None, # reserved
    )

    bigX = win32api.GetSystemMetrics(win32con.SM_CXICON)
    bigY = win32api.GetSystemMetrics(win32con.SM_CYICON)
    bigIcon = win32gui.LoadImage(0, iconPathname, win32con.IMAGE_ICON, bigX, bigY, win32con.LR_LOADFROMFILE)
    win32api.SendMessage(windowID, win32con.WM_SETICON, win32con.ICON_BIG, bigIcon)

    smallX = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
    smallY = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
    smallIcon = win32gui.LoadImage(0, iconPathname, win32con.IMAGE_ICON, smallX, smallY, win32con.LR_LOADFROMFILE)
    win32api.SendMessage(windowID, win32con.WM_SETICON, win32con.ICON_SMALL, smallIcon)

    return windowID


def CloseWindow(windowHandle, message, wparam, lparam):
    browser = cefpython.GetBrowserByWindowHandle(windowHandle)
    browser.CloseBrowser()

    global onCloseCallback
    onCloseCallback()

    return win32gui.DefWindowProc(windowHandle, message, wparam, lparam)


def QuitApplication(windowHandle, message, wparam, lparam):
    win32gui.PostQuitMessage(0)
    return 0


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
    if (len(pathname) > 1 and pathname[0].islower() and pathname[1] == ":"):
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
