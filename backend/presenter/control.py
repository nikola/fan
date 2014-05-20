# coding: utf-8
""" Implant CEF library into .EXE:
        http://www.pyinstaller.org/export/v2.0/project/doc/Manual.html#collect

    Extended Window Styles:
        http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx

    SetWindowPos function:
        http://msdn.microsoft.com/en-us/library/windows/desktop/ms633545(v=vs.85).aspx

    Inspect Kivy logic:
        https://github.com/kivy-garden/garden.cefpython/blob/master/__init__.py
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import time
import traceback
import codecs
import uuid
import imp

import win32gui
import win32api
import win32con

from presenter.hooks import ClientHandler
from config import *
from settings.presenter import *
from utils.win32 import getNormalizedPathname


shutdownAll = None


class JavascriptBridge(object):
    # mainBrowser = None
    # stringVisitor = None

    def __init__(self, mainBrowser): # , shutdownCallback):
        self.mainBrowser = mainBrowser
        # self.shutdownCallback = shutdownCallback

    def log(self, message):
        print(message)

    def shutdown(self):
        stop()
        # self.shutdownCallback()


    def Print(self, message):
        print(message)

    def TestAllTypes(self, *args):
        print(args)

    def ExecuteFunction(self, *args):
        self.mainBrowser.GetMainFrame().ExecuteFunction(*args)

    def TestJSCallback(self, jsCallback):
        print("jsCallback.GetFunctionName() = %s" % jsCallback.GetFunctionName())
        print("jsCallback.GetFrame().GetIdentifier() = %s" % \
                jsCallback.GetFrame().GetIdentifier())
        jsCallback.Call("This message was sent from python using js callback")

    def TestJSCallbackComplexArguments(self, jsObject):
        jsCallback = jsObject["myCallback"];
        jsCallback.Call(1, None, 2.14, "string", ["list", ["nested list", \
                {"nested object":None}]], \
                {"nested list next":[{"deeply nested object":1}]})

    def TestPythonCallback(self, jsCallback):
        jsCallback.Call(self.PyCallback)

    def PyCallback(self, *args):
        message = "PyCallback() was executed successfully! Arguments: %s" \
                % str(args)
        print(message)
        self.mainBrowser.GetMainFrame().ExecuteJavascript(
                "window.alert(\"%s\")" % message)

    # def GetSource(self):
    #     # Must keep a strong reference to the StringVisitor object
    #     # during the visit.
    #     self.stringVisitor = StringVisitor()
    #     self.mainBrowser.GetMainFrame().GetSource(self.stringVisitor)
    #
    # def GetText(self):
    #     # Must keep a strong reference to the StringVisitor object
    #     # during the visit.
    #     self.stringVisitor = StringVisitor()
    #     self.mainBrowser.GetMainFrame().GetText(self.stringVisitor)


def handleException(excType, excValue, traceObject):
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

    stop()
    os._exit(1)



def start(userAgent, httpPort, websocketPort, callback, bridgeToken): # , callbacks):
    global shutdownAll
    shutdownAll = callback

    # Import CEF Python library.
    global cefpython
    cefpython = imp.load_dynamic('cefpython_py27', os.path.join(PROJECT_PATH, 'backend', 'presenter', 'cef', 'libgfx.dll'))

    # Memorize callback functions that must be executed before shutting down the CEF container.
    # global onCloseCallbacks
    # onCloseCallbacks = callbacks

    appSettings = CEF_APP_SETTINGS
    appSettings.update({
        'log_severity':            cefpython.LOGSEVERITY_DISABLE,
        'browser_subprocess_path': os.path.join(cefpython.GetModuleDirectory(), 'iexplore'),
        'user_agent':              userAgent,
        'locales_dir_path':        os.path.join(cefpython.GetModuleDirectory()), # TODO: replace this with known directory
    })
    if DEBUG:
        appSettings.update({
            'debug':                  True,
            'release_dcheck_enabled': True,
            'remote_debugging_port':  8090,
            'log_file':               getNormalizedPathname('debug.log'), # TODO: replace this
            'log_severity':           cefpython.LOGSEVERITY_INFO,
        })
    # {END DEBUG}

    cefpython.Initialize(appSettings, CEF_CMD_LINE_SETTINGS)

    windowName = 'ka-BOOM' # TODO: use random name
    className = 'kaboom_%s' % uuid.uuid4().hex  # TODO: use random class
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

    # BUG: only works when /HKEY_CURRENT_USER/Software/Microsoft/Windows/DWM/Composition = 0
    dwExStyle = win32con.WS_EX_APPWINDOW | win32con.WS_EX_TOPMOST | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
    style = win32con.WS_VISIBLE | win32con.WS_POPUP | win32con.WS_CLIPCHILDREN | win32con.WS_CLIPSIBLINGS

    if DEBUG:
        dwExStyle = win32con.WS_EX_APPWINDOW
        style = win32con.WS_VISIBLE | win32con.WS_OVERLAPPEDWINDOW | win32con.WS_CLIPCHILDREN | win32con.WS_CLIPSIBLINGS | win32con.WS_MAXIMIZE
    # {END DEBUG}

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

    if not DEBUG:
        win32gui.SetLayeredWindowAttributes(windowId, win32api.RGB(255, 255, 255), 0, win32con.LWA_COLORKEY)
    # {END NOT DEBUG}

    # To turn off:
    # win32gui.SetWindowLong(windowID, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(windowID, win32con.GWL_EXSTYLE) & ~win32con.WS_EX_LAYERED)
    # win32gui.RedrawWindow(windowID, None, None, win32con.RDW_ERASE | win32con.RDW_INVALIDATE | win32con.RDW_FRAME | win32con.RDW_ALLCHILDREN)
    # win32gui.ShowWindow(windowID, win32con.SW_SHOWNORMAL)

    bigX = win32api.GetSystemMetrics(win32con.SM_CXICON)
    bigY = win32api.GetSystemMetrics(win32con.SM_CYICON)
    bigIcon = win32gui.LoadImage(0, iconPathname, win32con.IMAGE_ICON, bigX, bigY, win32con.LR_LOADFROMFILE)
    win32api.SendMessage(windowId, win32con.WM_SETICON, win32con.ICON_BIG, bigIcon)

    smallX = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
    smallY = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
    smallIcon = win32gui.LoadImage(0, iconPathname, win32con.IMAGE_ICON, smallX, smallY, win32con.LR_LOADFROMFILE)
    win32api.SendMessage(windowId, win32con.WM_SETICON, win32con.ICON_SMALL, smallIcon)

    windowInfo = cefpython.WindowInfo()
    windowInfo.SetAsChild(windowId)

    browser = cefpython.CreateBrowserSync(
        windowInfo,
        CHROME_BROWSER_SETTINGS,
        navigateUrl='https://127.0.0.1:%d/' % httpPort,
    )

    clientHandler = ClientHandler()
    browser.SetClientHandler(clientHandler)

    bridge = JavascriptBridge(browser) # , shutdownCallback)

    jsBindings = cefpython.JavascriptBindings(bindToFrames=False, bindToPopups=True) # TODO: set to False
    jsBindings.SetProperty('WEBSOCKET_PORT', websocketPort)
    jsBindings.SetObject(bridgeToken, bridge)
    jsBindings.SetObject('console', bridge)
    # TODO: put this into settings
    jsBindings.SetProperty('navigator', {'userAgent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.80 Safari/537.36'})
    browser.SetJavascriptBindings(jsBindings)

    cefpython.MessageLoop()
    cefpython.Shutdown()

    shutdownAll()


def stop():
    global cefpython
    cefpython.QuitMessageLoop()
    cefpython.Shutdown()

    global shutdownAll
    shutdownAll()


def CloseWindow(windowHandle, message, wparam, lparam):
    global cefpython
    browser = cefpython.GetBrowserByWindowHandle(windowHandle)
    browser.CloseBrowser()

    print 'CloseWindow'

    return win32gui.DefWindowProc(windowHandle, message, wparam, lparam)


def QuitApplication(*args, **kwargs):
    print 'QuitApplication'
    win32gui.PostQuitMessage(0)
    return 0