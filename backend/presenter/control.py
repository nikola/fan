# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@generic.company)"
__copyright__ = "Copyright (c) 2013-2014 Nikola Klaric"

import time
import traceback
import codecs
import uuid
import imp
from multiprocessing import Process, Queue

import win32gui
import win32api
import win32con

"""
from ctypes import *
class COLORREF(Structure):
    _fields_ = [
    ("byRed", c_byte),
    ("byGreen", c_byte),
    ("byBlue", c_byte)
    ]
print windll.gdi32.CreateSolidBrush(COLORREF(255, 0, 0))
"""

from config import *
from utils.win32 import getNormalizedPathname

# from chromium.hooks import ClientHandler
# if globals().has_key('cefpython'):
#     print "before", cefpython

# print "after", cefpython

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

    _destroyChromeContainer()
    os._exit(1)


def startPresenter(agent, url, callbacks):
    global globalPresenterProcess
    # global cefpython
    global onCloseCallbacks

    global className, windowName

    onCloseCallbacks = callbacks

    className = 'kaboom_%s' % uuid.uuid4().hex
    windowName = 'ka-BOOM'

    cefpython = imp.load_dynamic("cefpython_py27", os.path.join(PROJECT_PATH, "backend", "presenter", "cef", "libgfx.dll"))

    # cefpython = imp.load_dynamic("cefpython_py27", os.path.join(PROJECT_PATH, "backend", "presenter", "cef", "libgfx.dll"))

    print '0className', className
    print '0windowName', windowName

    globalPresenterProcess = Process(target=_createChromeContainer, args=(agent, url, className, windowName)) # , callbacks))
    globalPresenterProcess.start()


def stopPresenter():
    global globalPresenterProcess
    # cefpython,
    global onCloseCallbacks

    for callback in onCloseCallbacks: callback()

    global className, windowName

    print '1className', className
    print '1windowName', windowName
    windowHandle = win32gui.FindWindow(className, windowName)

    print 'windowHandle', windowHandle

    print 'GetBrowserByWindowHandle', cefpython.GetBrowserByWindowHandle(windowHandle)

    browser = cefpython.GetBrowserByWindowHandle(windowHandle)
    browser.CloseBrowser()


    cefpython.QuitMessageLoop()
    cefpython.Shutdown()

    # cefpython.browser.CloseBrowser()

    # QuitApplication()

    print 2

    globalPresenterProcess.terminate()


def _createChromeContainer(agent, url, className, windowName): # , callbacks):
    # global cefpython

    # TODO: Refactor:
    #   https://github.com/kivy-garden/garden.cefpython/blob/master/__init__.py

    # Implant into .EXE:
    #   http://www.pyinstaller.org/export/v2.0/project/doc/Manual.html#collect

    # cefpython = imp.load_dynamic("cefpython_py27", os.path.join(PROJECT_PATH, "backend", "presenter", "cef", "libgfx.dll"))

    # Memorize callback functions that must be executed before shutting down the CEF container.
    # global onCloseCallbacks
    # onCloseCallbacks = callbacks

    cefpython.g_debug = DEBUG
    cefpython.g_debugFile = getNormalizedPathname("debug.log")

    cefpython.Initialize(
        dict(   # applicationSettings
            debug                       = DEBUG,
            cache_path                  = '',
            log_file                    = getNormalizedPathname("debug.log"),
            log_severity                = cefpython.LOGSEVERITY_INFO,
            release_dcheck_enabled      = DEBUG, # Disable in production
            browser_subprocess_path     = "%s\\%s" % (cefpython.GetModuleDirectory(), "iexplore"),
            user_agent                  = agent,
            ignore_certificate_errors   = True,
            remote_debugging_port       = 8090,
            multi_threaded_message_loop = False,
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

    """
    windowId = createChromeWindow(
        className = className, # 'kaboom_%s' % uuid.uuid4().hex,
        windowName = windowName, # 'ka-BOOM',
        iconPathname = getNormalizedPathname("../presenter/cef/icon.ico"),
    )
    """


    iconPathname = getNormalizedPathname("../presenter/cef/icon.ico")


    wndclass = win32gui.WNDCLASS()
    wndclass.hInstance = win32api.GetModuleHandle(None)
    wndclass.lpszClassName = className
    wndclass.style = 0 # win32con.CS_NOCLOSE # win32con.CS_VREDRAW | win32con.CS_HREDRAW
    wndclass.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
    wndclass.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wndclass.lpfnWndProc = {
        win32con.WM_CLOSE: CloseWindow,
        win32con.WM_DESTROY: QuitApplication,
        win32con.WM_SIZE: cefpython.WindowUtils.OnSize,
        win32con.WM_SETFOCUS: cefpython.WindowUtils.OnSetFocus,
        win32con.WM_ERASEBKGND: cefpython.WindowUtils.OnEraseBackground
    }
    win32gui.RegisterClass(wndclass)

    # Extended Window Styles:
    #   http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx

    # SetWindowPos function:
    #   http://msdn.microsoft.com/en-us/library/windows/desktop/ms633545(v=vs.85).aspx

    # if DEBUG:
    #     dwExStyle = win32con.WS_EX_APPWINDOW
    #     style = win32con.WS_OVERLAPPEDWINDOW | win32con.WS_CLIPCHILDREN | win32con.WS_VISIBLE
    # else:

    # BUG: only works when /HKEY_CURRENT_USER/Software/Microsoft/Windows/DWM/Composition = 0





    dwExStyle = win32con.WS_EX_APPWINDOW | win32con.WS_EX_TOPMOST | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
    # dwExStyle = win32con.WS_EX_LAYERED
    style = win32con.WS_VISIBLE | win32con.WS_POPUP | win32con.WS_CLIPCHILDREN | win32con.WS_CLIPSIBLINGS

    windowId = win32gui.CreateWindowEx(
        dwExStyle,
        className,
        windowName,
        style,
        win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
        win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1),
        0, # parent
        0, # menu
        wndclass.hInstance,
        None, # reserved
    )

    #  if not DEBUG:
    win32gui.SetLayeredWindowAttributes(windowId, win32api.RGB(255, 255, 255), 0, win32con.LWA_COLORKEY)
    # win32gui.SetLayeredWindowAttributes(windowID, win32api.RGB(0, 0, 0), 255, win32con.LWA_COLORKEY)

    # win32gui.ShowWindow(windowID, win32con.SW_SHOWNORMAL)

    # win32gui.SetWindowPos(windowID, None, 0, 0, 1920, 1080, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
    # SetWindowPos(window_->GetNativeWindow(), NULL, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED);

    # To turn off:
    # win32gui.SetWindowLong(windowID, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(windowID, win32con.GWL_EXSTYLE) & ~win32con.WS_EX_LAYERED)
    # win32gui.RedrawWindow(windowID, None, None, win32con.RDW_ERASE | win32con.RDW_INVALIDATE | win32con.RDW_FRAME | win32con.RDW_ALLCHILDREN)

    # 100% Opaque:
    # win32gui.SetLayeredWindowAttributes(windowID, 0, (20 * 100) / 100, win32con.LWA_ALPHA)

    bigX = win32api.GetSystemMetrics(win32con.SM_CXICON)
    bigY = win32api.GetSystemMetrics(win32con.SM_CYICON)
    bigIcon = win32gui.LoadImage(0, iconPathname, win32con.IMAGE_ICON, bigX, bigY, win32con.LR_LOADFROMFILE)
    win32api.SendMessage(windowId, win32con.WM_SETICON, win32con.ICON_BIG, bigIcon)

    smallX = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
    smallY = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
    smallIcon = win32gui.LoadImage(0, iconPathname, win32con.IMAGE_ICON, smallX, smallY, win32con.LR_LOADFROMFILE)
    win32api.SendMessage(windowId, win32con.WM_SETICON, win32con.ICON_SMALL, smallIcon)

    # return windowID



















    print 'windowId', windowId

    windowInfo = cefpython.WindowInfo()
    windowInfo.SetAsChild(windowId)

    browser = cefpython.CreateBrowserSync(
        windowInfo,
        CHROME_BROWSER_SETTINGS,
        navigateUrl=url,
    )

    # print 0
    # print browser

    # clientHandler = ClientHandler()
    # browser.SetClientHandler(clientHandler)

    cefpython.MessageLoop()
    # cefpython.Shutdown()


def _destroyChromeContainer():
    # global cefpython, \
    global onCloseCallbacks

    for callback in onCloseCallbacks: callback()

    cefpython.QuitMessageLoop()
    cefpython.Shutdown()


"""
def createChromeWindow(className, windowName, iconPathname):
    # global cefpython

    print '2className', className
    print '2windowName', windowName

    wndclass = win32gui.WNDCLASS()
    wndclass.hInstance = win32api.GetModuleHandle(None)
    wndclass.lpszClassName = className
    wndclass.style = 0 # win32con.CS_NOCLOSE # win32con.CS_VREDRAW | win32con.CS_HREDRAW
    wndclass.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
    wndclass.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wndclass.lpfnWndProc = {
        win32con.WM_CLOSE: CloseWindow,
        win32con.WM_DESTROY: QuitApplication,
        win32con.WM_SIZE: cefpython.WindowUtils.OnSize,
        win32con.WM_SETFOCUS: cefpython.WindowUtils.OnSetFocus,
        win32con.WM_ERASEBKGND: cefpython.WindowUtils.OnEraseBackground
    }
    win32gui.RegisterClass(wndclass)

    # Extended Window Styles:
    #   http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx

    # SetWindowPos function:
    #   http://msdn.microsoft.com/en-us/library/windows/desktop/ms633545(v=vs.85).aspx

    # if DEBUG:
    #     dwExStyle = win32con.WS_EX_APPWINDOW
    #     style = win32con.WS_OVERLAPPEDWINDOW | win32con.WS_CLIPCHILDREN | win32con.WS_VISIBLE
    # else:

    # BUG: only works when /HKEY_CURRENT_USER/Software/Microsoft/Windows/DWM/Composition = 0





    dwExStyle = win32con.WS_EX_APPWINDOW | win32con.WS_EX_TOPMOST | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
    # dwExStyle = win32con.WS_EX_LAYERED
    style = win32con.WS_VISIBLE | win32con.WS_POPUP | win32con.WS_CLIPCHILDREN | win32con.WS_CLIPSIBLINGS

    windowID = win32gui.CreateWindowEx(
        dwExStyle,
        className,
        windowName,
        style,
        win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
        win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1),
        0, # parent
        0, # menu
        wndclass.hInstance,
        None, # reserved
    )

    #  if not DEBUG:
    win32gui.SetLayeredWindowAttributes(windowID, win32api.RGB(255, 255, 255), 0, win32con.LWA_COLORKEY)
    # win32gui.SetLayeredWindowAttributes(windowID, win32api.RGB(0, 0, 0), 255, win32con.LWA_COLORKEY)

    # win32gui.ShowWindow(windowID, win32con.SW_SHOWNORMAL)

    # win32gui.SetWindowPos(windowID, None, 0, 0, 1920, 1080, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
    # SetWindowPos(window_->GetNativeWindow(), NULL, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED);

    # To turn off:
    # win32gui.SetWindowLong(windowID, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(windowID, win32con.GWL_EXSTYLE) & ~win32con.WS_EX_LAYERED)
    # win32gui.RedrawWindow(windowID, None, None, win32con.RDW_ERASE | win32con.RDW_INVALIDATE | win32con.RDW_FRAME | win32con.RDW_ALLCHILDREN)

    # 100% Opaque:
    # win32gui.SetLayeredWindowAttributes(windowID, 0, (20 * 100) / 100, win32con.LWA_ALPHA)

    bigX = win32api.GetSystemMetrics(win32con.SM_CXICON)
    bigY = win32api.GetSystemMetrics(win32con.SM_CYICON)
    bigIcon = win32gui.LoadImage(0, iconPathname, win32con.IMAGE_ICON, bigX, bigY, win32con.LR_LOADFROMFILE)
    win32api.SendMessage(windowID, win32con.WM_SETICON, win32con.ICON_BIG, bigIcon)

    smallX = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
    smallY = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
    smallIcon = win32gui.LoadImage(0, iconPathname, win32con.IMAGE_ICON, smallX, smallY, win32con.LR_LOADFROMFILE)
    win32api.SendMessage(windowID, win32con.WM_SETICON, win32con.ICON_SMALL, smallIcon)

    return windowID
"""

def CloseWindow(windowHandle, message, wparam, lparam):
    # global cefpython, \
    global onCloseCallbacks

    print 'close'
    print windowHandle
    print 'end'

    browser = cefpython.GetBrowserByWindowHandle(windowHandle)
    browser.CloseBrowser()


    # for callback in onCloseCallbacks: callback()

    return win32gui.DefWindowProc(windowHandle, message, wparam, lparam)


def QuitApplication(windowHandle, *args, **kwargs): # windowHandle, message, wparam, lparam):
    # win32gui.UnregisterClass(parent.className, None)

    """
	browser = cefpython.GetBrowserByWindowID(windowHandle)
	browser.CloseBrowser()


	cefwindow.DestroyWindow(windowHandle)

        ---->

            win32gui.DestroyWindow(windowHandle)
            #className = GetWindowClassName(windowHandle)
            #win32gui.UnregisterClass(className, None)
            #del g_windows[windowID] # Let window with this className be created again.


	win32gui.PostQuitMessage(0)
    """

    win32gui.PostQuitMessage(0)
    return 0


if __name__ == '__main__':
    print '--------- MAIN ------------'
#
#     print cefpython
#     # cefpython.t = 1
