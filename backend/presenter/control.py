# coding: utf-8
""" Extended Window Styles:
        http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx

    SetWindowPos function:
        http://msdn.microsoft.com/en-us/library/windows/desktop/ms633545(v=vs.85).aspx

    Inspect Kivy logic:
        https://github.com/kivy-garden/garden.cefpython/blob/master/__init__.py
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os
# import time
import traceback
# import codecs
import uuid
import imp
import logging

import win32gui
import win32api
import win32con

from settings import DEBUG
from settings import LOG_CONFIG
from settings import ENTROPY_SEED, ASSETS_PATH, APP_STORAGE_PATH
from settings.presenter import *
# from presenter.hooks import ClientHandler
# from utils.win32 import getColorBrush # getNormalizedPathname,
from utils.fs import getLogFileHandler
from utils.system import getCurrentInstanceIdentifier


logging.basicConfig(**LOG_CONFIG)
logger = logging.getLogger('gui')
logger.propagate = DEBUG
logger.addHandler(getLogFileHandler('gui'))


shutdownAll = None

# TODO: REFACTOR AND CLEAN UP !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class JavascriptBridge(object):
    # mainBrowser = None
    # stringVisitor = None

    def __init__(self, mainBrowser): # , shutdownCallback):
        self.mainBrowser = mainBrowser
        # self.shutdownCallback = shutdownCallback

    def log(self, message):
        logger.info(message)

    def debug(self, message):
        logger.debug(message)

    def warn(self, message):
        logger.warning(message)

    def error(self, message):
        logger.error(message)

    def shutdown(self):
        stop()

    # def Print(self, message):
    #     print(message)

    # def TestAllTypes(self, *args):
    #     print(args)

    # def ExecuteFunction(self, *args):
    #     self.mainBrowser.GetMainFrame().ExecuteFunction(*args)

    # def TestJSCallback(self, jsCallback):
    #     print("jsCallback.GetFunctionName() = %s" % jsCallback.GetFunctionName())
    #     print("jsCallback.GetFrame().GetIdentifier() = %s" % \
    #             jsCallback.GetFrame().GetIdentifier())
    #     jsCallback.Call("This message was sent from python using js callback")

    # def TestJSCallbackComplexArguments(self, jsObject):
    #     jsCallback = jsObject["myCallback"];
    #     jsCallback.Call(1, None, 2.14, "string", ["list", ["nested list", \
    #             {"nested object":None}]], \
    #             {"nested list next":[{"deeply nested object":1}]})

    # def TestPythonCallback(self, jsCallback):
    #     jsCallback.Call(self.PyCallback)

    # def PyCallback(self, *args):
    #     message = "PyCallback() was executed successfully! Arguments: %s" \
    #             % str(args)
    #     print(message)
    #     self.mainBrowser.GetMainFrame().ExecuteJavascript(
    #             "window.alert(\"%s\")" % message)

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

    # try:
    #     with codecs.open(getNormalizedPathname("error.log"), mode="a", encoding="utf-8") as fp:
    #         fp.write("\n[%s] %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), errorMsg))
    # except:
    #     pass

    errorMsg = errorMsg.encode("ascii", errors="replace").decode("ascii", errors="replace")
    print("\n%s\n" % errorMsg)

    stop()
    os._exit(1)


def start(callback, userAgent, serverPort, bridgeToken, bootToken, mustSecure, userConfig, *args):
    global shutdownAll
    shutdownAll = callback

    global msie
    msie = imp.load_dynamic('prsclguba_cl'.decode((str(255 - 0xe0) + 'tor')[::-1]) + str(255 - 0xe4), os.path.join(ASSETS_PATH, 'trident', 'libgfx.dll'))

    appSettings = CEF_APP_SETTINGS
    appSettings.update({
        'cache_path':              os.path.join(APP_STORAGE_PATH, getCurrentInstanceIdentifier() + '.cache'),
        'log_severity':            msie.LOGSEVERITY_DISABLE,
        'browser_subprocess_path': os.path.join(ASSETS_PATH, 'trident', 'ka-BOOM-GUI'),
        'user_agent':              userAgent,
        'locales_dir_path':        os.path.join(ASSETS_PATH, 'trident'),
    })
    if False: # DEBUG
        appSettings.update({
            'debug':                  True,
            'release_dcheck_enabled': True,
            'remote_debugging_port':  8090,
            # 'log_file':               getNormalizedPathname('debug.log'),
            'log_severity':           msie.LOGSEVERITY_INFO,
        })
    # END if DEBUG

    msie.Initialize(appSettings, CEF_CMD_LINE_SETTINGS)

    windowName = 'ka-BOOM'
    className = uuid.uuid4().hex
    iconPathname = os.path.join(ASSETS_PATH, 'shaders', '92d2b19706b64732981b00c07f6c4bee.cso')

    wndclass = win32gui.WNDCLASS()
    wndclass.hInstance = win32api.GetModuleHandle(None)
    wndclass.lpszClassName = className
    wndclass.style = win32con.CS_NOCLOSE | win32con.CS_VREDRAW | win32con.CS_HREDRAW
    wndclass.hbrBackground = win32gui.GetStockObject(win32con.BLACK_BRUSH)
    wndclass.hCursor = win32gui.SetCursor(None)
    wndclass.lpfnWndProc = {
        win32con.WM_CLOSE: CloseWindow,
        win32con.WM_DESTROY: QuitApplication,
        win32con.WM_SIZE: msie.WindowUtils.OnSize,
        win32con.WM_SETFOCUS: msie.WindowUtils.OnSetFocus,
        win32con.WM_ERASEBKGND: msie.WindowUtils.OnEraseBackground
    }
    win32gui.RegisterClass(wndclass)

    # BUG: only works when /HKEY_CURRENT_USER/Software/Microsoft/Windows/DWM/Composition = 0
    dwExStyle = win32con.WS_EX_APPWINDOW # | win32con.WS_EX_LAYERED
    style = win32con.WS_VISIBLE | win32con.WS_POPUP | win32con.WS_CLIPCHILDREN | win32con.WS_CLIPSIBLINGS

    # if DEBUG:
    #     dwExStyle = win32con.WS_EX_APPWINDOW | win32con.WS_EX_TOPMOST
    #     style = win32con.WS_VISIBLE | win32con.WS_OVERLAPPEDWINDOW | win32con.WS_CLIPCHILDREN | win32con.WS_CLIPSIBLINGS | win32con.WS_MAXIMIZE
    # {END DEBUG}

    global windowId
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

    # win32gui.SetLayeredWindowAttributes(windowId, win32api.RGB(255, 255, 255), 0, win32con.LWA_COLORKEY)

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

    windowInfo = msie.WindowInfo()
    windowInfo.SetAsChild(windowId)

    protocol = 'https:' if mustSecure else 'http:'
    screen = 'configure' if not len(userConfig['sources']) and not userConfig.get('isDemoMode', False) else 'load'
    browser = msie.CreateBrowserSync(
        windowInfo,
        CEF_BROWSER_SETTINGS,
        navigateUrl='%s//127.0.0.1:%d/%s.asp' % (protocol, serverPort, screen),
    )

    # clientHandler = ClientHandler()
    # browser.SetClientHandler(clientHandler)

    bridge = JavascriptBridge(browser)

    jsBindings = msie.JavascriptBindings(bindToFrames=True, bindToPopups=True)
    jsBindings.SetProperty('ᴠ', bootToken)  # http://www.unicode.org/Public/security/revision-06/confusables.txt
    jsBindings.SetProperty('ka', {'config': userConfig})
    jsBindings.SetObject('__%s__' % bridgeToken, bridge)
    jsBindings.SetObject('console', bridge)
    jsBindings.SetProperty('navigator', {'userAgent': ENTROPY_SEED})
    browser.SetJavascriptBindings(jsBindings)

    win32api.ShowCursor(0)

    msie.MessageLoop()
    msie.Shutdown()

    shutdownAll()


def stop():
    global msie
    msie.QuitMessageLoop()
    msie.Shutdown()

    global windowId
    win32gui.ShowWindow(windowId, win32con.SW_HIDE)

    global shutdownAll
    shutdownAll()


def CloseWindow(windowHandle, message, wparam, lparam):
    global msie
    browser = msie.GetBrowserByWindowHandle(windowHandle)
    browser.CloseBrowser()

    # print 'CloseWindow'

    return win32gui.DefWindowProc(windowHandle, message, wparam, lparam)


def QuitApplication(*args, **kwargs):
    # print 'QuitApplication'
    win32gui.PostQuitMessage(0)
    return 0
