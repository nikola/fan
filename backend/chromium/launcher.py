# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

import os
import time
import traceback
import codecs
import uuid
import imp

import win32gui
import win32api
import win32con

from config import *
from utils.win32 import getNormalizedPathname

# from chromium.hooks import ClientHandler


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


def launchChrome(agent, url, callbacks):
    """
    """
    global cefpython

    cefpython = imp.load_dynamic("cefpython_py27", os.path.join(PROJECT_PATH, "backend", "chromium", "cef", "libgfx.dll"))

    # Memorize callback functions that must be executed before shutting down the CEF container.
    global onCloseCallbacks
    onCloseCallbacks = callbacks

    cefpython.g_debug = DEBUG
    cefpython.g_debugFile = getNormalizedPathname("debug.log")

    cefpython.Initialize(
        dict(   # applicationSettings
            debug                     = DEBUG,
            cache_path                = '',
            log_file                  = getNormalizedPathname("debug.log"),
            log_severity              = cefpython.LOGSEVERITY_INFO,
            release_dcheck_enabled    = DEBUG, # Disable in production
            browser_subprocess_path   = "%s\\%s" % (cefpython.GetModuleDirectory(), "iexplore"),
            user_agent                = agent,
            ignore_certificate_errors = True,
            remote_debugging_port     = 8090,
        ),
        {
            # https://code.google.com/p/chromiumembedded/source/browse/trunk/cef3/libcef/common/cef_switches.cc
            'disable-javascript-open-windows':      '',
            'disable-javascript-close-windows':     '',
            'disable-javascript-access-clipboard':  '',
            'disable-javascript-dom-paste':         '',
            'disable-text-area-resize':             '',
            'disable-tab-to-links':                 '',
            # http://peter.sh/experiments/chromium-command-line-switches/
            'disable-breakpad':                     '',
            'disable-extensions':                   '',
            'disable-google-now-integration':       '',
            'disable-improved-download-protection': '',
            'disable-infobars':                     '',
            'disable-ipv6':                         '',
            'disable-java':                         '',
            'disable-logging':                      '',
            'disable-preconnect':                   '',
            'disable-prerender-local-predictor':    '',
            'disable-sync':                         '',
            'disable-volume-adjust-sound':          '',
            'disable-webaudio':                     '',
            'dns-prefetch-disable':                 '',
            'disk-cache-dir':                       'nul',
            'media-cache-dir':                      'nul',
            'disk-cache-size':                      '1',
            'enable-benchmarking':                  '',
            'no-displaying-insecure-content':       '',
            'no-pings':                             '',
            'no-referrers':                         '',
            'noerrdialogs':                         '',

            # locale_pak Load the locale resources from the given path. When running on Mac/Unix the path should point to a locale.pak file.
        },
    )

    windowId = createChromeWindow(
        title = "ka-BOOM",
        className = "kaboom_%s" % uuid.uuid4().hex,
        iconPathname = getNormalizedPathname("../chromium/cef/icon.ico"),
    )

    windowInfo = cefpython.WindowInfo()
    windowInfo.SetAsChild(windowId)

    # browser = cefpython.CreateBrowserSync(
    cefpython.CreateBrowserSync(
        windowInfo,
        CHROME_BROWSER_SETTINGS,
        navigateUrl=url,
    )
    # browser.ToggleFullscreen()

    # clientHandler = ClientHandler()
    # browser.SetClientHandler(clientHandler)

    cefpython.MessageLoop()
    cefpython.Shutdown()


def stopChromeContainer():
    """
    """
    global cefpython, onCloseCallbacks

    for callback in onCloseCallbacks: callback()

    cefpython.QuitMessageLoop()
    cefpython.Shutdown()


def createChromeWindow(title, className, iconPathname):
    """
    """
    global cefpython

    wndclass = win32gui.WNDCLASS()
    wndclass.hInstance = win32api.GetModuleHandle(None)
    wndclass.lpszClassName = className
    wndclass.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
    wndclass.hbrBackground = win32con.BLACK_BRUSH
    wndclass.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wndclass.lpfnWndProc = {
        win32con.WM_CLOSE: CloseWindow,
        win32con.WM_DESTROY: QuitApplication,
        win32con.WM_SIZE: cefpython.WindowUtils.OnSize,
        win32con.WM_SETFOCUS: cefpython.WindowUtils.OnSetFocus,
        win32con.WM_ERASEBKGND: cefpython.WindowUtils.OnEraseBackground
    }
    win32gui.RegisterClass(wndclass)

    # int = CreateWindow(className, windowTitle , style , x , y , width , height , parent , menu , hinstance , reserved )
    # int = CreateWindowEx(dwExStyle, className , windowTitle , style , x , y , width , height , parent , menu , hinstance , reserved )

    # windowID = win32gui.CreateWindow(
    windowID = win32gui.CreateWindowEx(
        win32con.WS_EX_APPWINDOW, # | win32con.WS_EX_TOPMOST,
        className,
        title,
        # win32con.WS_OVERLAPPEDWINDOW | win32con.WS_CLIPCHILDREN | win32con.WS_VISIBLE,
        win32con.WS_POPUP | win32con.WS_VISIBLE | win32con.WS_SYSMENU,
        win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
        win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1),
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
    """
    """
    global cefpython, onCloseCallbacks

    browser = cefpython.GetBrowserByWindowHandle(windowHandle)
    browser.CloseBrowser()

    for callback in onCloseCallbacks: callback()

    return win32gui.DefWindowProc(windowHandle, message, wparam, lparam)


def QuitApplication(*args, **kwargs):
    win32gui.PostQuitMessage(0)
    return 0
