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

import os
import uuid
import imp

import win32gui
import win32api
import win32con

from settings import DEBUG, ASSETS_PATH, APP_STORAGE_PATH
from settings.presenter import *
from presenter.hooks import ClientHandler
from utils.logs import getLogger
from utils.win32 import getColorBrush


shutdownAll = None


class JavascriptBridge(object):

    def __init__(self, mainBrowser, windowId, logger):
        self.mainBrowser = mainBrowser
        self.windowId = windowId
        self.logger = logger

    def log(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def exitApplication(self):
        win32gui.ShowWindow(self.windowId, win32con.SW_HIDE)

        stop()


def start(callback, initialPage, profile, *args):
    global shutdownAll
    shutdownAll = callback

    global cef
    cef = imp.load_dynamic('cefpython_py27', os.path.join(ASSETS_PATH, 'thirdparty', 'cef', 'cefpython_py27.pyd'))

    appSettings = CEF_APP_SETTINGS
    appSettings.update({
        'cache_path':              os.path.join(APP_STORAGE_PATH, profile + '.cache'),
        'log_severity':            cef.LOGSEVERITY_DISABLE,
        'browser_subprocess_path': os.path.join(ASSETS_PATH, 'thirdparty', 'cef', 'subprocess'),
        'locales_dir_path':        os.path.join(ASSETS_PATH, 'thirdparty', 'cef'),
    })
    if DEBUG:
        appSettings.update({
            'debug':                  True,
            'release_dcheck_enabled': True,
            'remote_debugging_port':  CEF_REMOTE_DEBUGGING_PORT,
            'log_severity':           cef.LOGSEVERITY_INFO,
        })

    cef.Initialize(appSettings, CEF_CMD_LINE_SETTINGS)

    windowName = 'fan'
    className = uuid.uuid4().hex
    iconPathname = os.path.join(ASSETS_PATH, 'assets', 'fan.ico')

    wndclass = win32gui.WNDCLASS()
    wndclass.hInstance = win32api.GetModuleHandle(None)
    wndclass.lpszClassName = className
    wndclass.style = win32con.CS_NOCLOSE | win32con.CS_VREDRAW | win32con.CS_HREDRAW
    wndclass.hbrBackground = getColorBrush(0, 0, 0) # win32gui.GetStockObject(win32con.BLACK_BRUSH)
    wndclass.hCursor = win32gui.SetCursor(None)
    wndclass.lpfnWndProc = {
        win32con.WM_CLOSE: CloseWindow,
        win32con.WM_DESTROY: QuitApplication,
        win32con.WM_SIZE: cef.WindowUtils.OnSize,
        win32con.WM_SETFOCUS: cef.WindowUtils.OnSetFocus,
        win32con.WM_ERASEBKGND: cef.WindowUtils.OnEraseBackground
    }
    win32gui.RegisterClass(wndclass)

    dwExStyle = win32con.WS_EX_APPWINDOW
    style = win32con.WS_VISIBLE | win32con.WS_POPUP | win32con.WS_CLIPCHILDREN | win32con.WS_CLIPSIBLINGS | win32con.WS_MAXIMIZE

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

    bigX = win32api.GetSystemMetrics(win32con.SM_CXICON)
    bigY = win32api.GetSystemMetrics(win32con.SM_CYICON)
    bigIcon = win32gui.LoadImage(0, iconPathname, win32con.IMAGE_ICON, bigX, bigY, win32con.LR_LOADFROMFILE)
    win32api.SendMessage(windowId, win32con.WM_SETICON, win32con.ICON_BIG, bigIcon)

    smallX = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
    smallY = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
    smallIcon = win32gui.LoadImage(0, iconPathname, win32con.IMAGE_ICON, smallX, smallY, win32con.LR_LOADFROMFILE)
    win32api.SendMessage(windowId, win32con.WM_SETICON, win32con.ICON_SMALL, smallIcon)

    windowInfo = cef.WindowInfo()
    windowInfo.SetAsChild(windowId)

    browser = cef.CreateBrowserSync(
        windowInfo,
        CEF_BROWSER_SETTINGS,
        navigateUrl=initialPage,
    )

    clientHandler = ClientHandler()
    browser.SetClientHandler(clientHandler)

    bridge = JavascriptBridge(browser, windowId, getLogger(profile, 'presenter'))

    jsBindings = cef.JavascriptBindings(bindToFrames=True, bindToPopups=True)
    jsBindings.SetObject('console', bridge)
    browser.SetJavascriptBindings(jsBindings)

    win32api.ShowCursor(0)

    cef.MessageLoop()
    cef.Shutdown()

    shutdownAll()


def stop():
    global cef
    cef.QuitMessageLoop()
    cef.Shutdown()

    global shutdownAll
    shutdownAll()


def CloseWindow(windowHandle, message, wparam, lparam):
    global cef
    browser = cef.GetBrowserByWindowHandle(windowHandle)
    browser.CloseBrowser()

    return win32gui.DefWindowProc(windowHandle, message, wparam, lparam)


def QuitApplication(*args, **kwargs):
    win32gui.PostQuitMessage(0)
    return 0
