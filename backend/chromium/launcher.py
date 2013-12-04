# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

import time
import traceback
import codecs
import uuid
import imp
import win32con
import win32gui
import win32api
from config import *
from utils.win32 import getNormalizedPathname
from chromium.hooks import ClientHandler

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


def launchChrome(agent, url, callbacks):
    """
    """
    global cefpython

    cefpython = imp.load_dynamic("cefpython_py27", os.path.join(PROJECT_PATH, "backend", "chromium", "cef", "framework.pyd"))

    # Memorize callback functions that must be executed before shutting down the CEF container.
    global onCloseCallbacks
    onCloseCallbacks = callbacks

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

    print getNormalizedPathname("cef/icon.ico"),

    windowId = createChromeWindow(
        title = "ka-BOOM",
        className = "kaboom_%s" % uuid.uuid4().hex,
        iconPathname = getNormalizedPathname("../chromium/cef/icon.ico"),
    )

    windowInfo = cefpython.WindowInfo()
    windowInfo.SetAsChild(windowId)

    browser = cefpython.CreateBrowserSync(
        windowInfo,
        CHROME_BROWSER_SETTINGS,
        navigateUrl=url,
    )
    browser.ToggleFullscreen()

    clientHandler = ClientHandler()
    browser.SetClientHandler(clientHandler)

    cefpython.MessageLoop()
    cefpython.Shutdown()


def stopChromeContainer():
    """
    """
    global cefpython, onCloseCallbacks

    for callback in onCloseCallbacks: callback()

    cefpython.QuitMessageLoop()
    cefpython.Shutdown()


def createChromeWindow(title, className, iconPathname, width=1920, height=1080, xpos=0, ypos=0):
    """
    """
    global cefpython

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
