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
__copyright__ = 'Copyright (c) 2013-2015 Nikola Klaric'


class ClientHandler(object):

    def __init__(self):
        pass


    # def OnKeyEvent(self, browser, event, eventHandle):
    #     """ Called after the renderer and JavaScript in the page has had a chance to handle the event.
    #         |event| contains information about the keyboard event. |os_event| is the operating system event message, if any.
    #         Return true if the keyboard event was handled or false otherwise. Description of the KeyEvent type is in the OnPreKeyEvent() callback.
    #     """
    #     if event['windows_key_code'] == 116:
    #         browser.ReloadIgnoreCache()
    #         return True


    # DisplayHandler -----------------------------------------------------------

    # void OnLoadingStateChange(Browser browser, bool isLoading, bool canGoBack, bool canGoForward)
    # def OnLoadingStateChange(self, browser, isLoading, canGoBack, canGoForward):
        """ Called when the loading state has changed. This callback will be executed twice.
            Once when loading is initiated either programmatically or by user action,
            and once when loading is terminated due to completion, cancellation of failure.
        """

    # void OnAddressChange(Browser browser, Frame frame, string url)
    # def OnAddressChange(self, browser, frame, url):
        """ Called when a frame's address has changed.
        """

    # void OnTitleChange(Browser browser, string title)
    # def OnTitleChange(self, browser, title):
        """ Called when the page title changes.
        """

    # bool OnTooltip(Browser browser, list& textOut)
    # def OnTooltip(self, browser, textOut):
        """ Called when the browser is about to display a tooltip.
            textOut[0] contains the text that will be displayed in the tooltip.
            To handle the display of the tooltip yourself return true.
            Otherwise, you can optionally modify textOut[0] and then return false to allow the browser to display the tooltip.
            When window rendering is disabled the application is responsible for drawing tooltips and the return value is ignored.
        """

    # void OnStatusMessage(Browser browser, string value)
    # def OnStatusMessage(self, browser, value):
        """ Called when the browser receives a status message.
        """

    # bool OnConsoleMessage(Browser browser, string message, string source, int line)
    # def OnConsoleMessage(self, browser, message, source, line):
        """ Called to display a console message. Return true to stop the message from being output to the console.
        """


    # KeyboardHandler -----------------------------------------------------------

    # bool OnPreKeyEvent(Browser browser, KeyEvent event, MSG*|GdkEvent*|NSEvent* eventHandle, list& isKeyboardShortcutOut)
    # def OnPreKeyEvent(self, browser, event, eventHandle, isKeyboardShortcutOut):
        """ Called before a keyboard event is sent to the renderer. |event| contains information about the keyboard event.
            |eventHandle| is the operating system event message, if any. Return true if the event was handled or false otherwise.
            If the event will be handled in OnKeyEvent() as a keyboard shortcut set isKeyboardShortcutOut[0] to true and return false.

            KeyEvent is a dictionary with the following keys:

                "type" (KeyEventType) -     The type of keyboard event
                "modifiers" (uint32) -      Bit flags describing any pressed modifier keys. See KeyEventFlags for values.
                "windows_key_code" (int) -  The Windows key code for the key event. This value is used by the DOM specification.
                                            Sometimes it comes directly from the event (i.e. on Windows)
                                            and sometimes it's determined using a mapping function.
                                            See "WebCore/platform/chromium/KeyboardCodes.h" for the list of values.
                "native_key_code" (int) -   The actual key code genenerated by the platform.
                "is_system_key" (int) -     Indicates whether the event is considered a "system key" event
                                            (see http://msdn.microsoft.com/en-us/library/ms646286(VS.85).aspx for details).
                                            This value will always be false on non-Windows platforms.
                "character" (wchar_t or
                    unsigned short) -       The character generated by the keystroke.
                "unmodified_character"
                    (wchar_t or
                    unsigned short) -       Same as |character| but unmodified by any concurrently-held modifiers (except shift).
                                            This is useful for working out shortcut keys.
                "focus_on_editable_field"
                    (bool) -                True if the focus is currently on an editable field on the page. This is useful for determining
                                            if standard key events should be intercepted.

            KeyEventType is one of:

                cefpython.KEYEVENT_RAWKEYDOWN
                cefpython.KEYEVENT_KEYDOWN
                cefpython.KEYEVENT_KEYUP
                cefpython.KEYEVENT_CHAR

            KeyEventFlags constants ("modifiers" key):

                cefpython.EVENTFLAG_NONE
                cefpython.EVENTFLAG_CAPS_LOCK_ON
                cefpython.EVENTFLAG_SHIFT_DOWN
                cefpython.EVENTFLAG_CONTROL_DOWN
                cefpython.EVENTFLAG_ALT_DOWN
                cefpython.EVENTFLAG_LEFT_MOUSE_BUTTON
                cefpython.EVENTFLAG_MIDDLE_MOUSE_BUTTON
                cefpython.EVENTFLAG_RIGHT_MOUSE_BUTTON
                cefpython.EVENTFLAG_NUM_LOCK_ON
                cefpython.EVENTFLAG_IS_KEY_PAD
                cefpython.EVENTFLAG_IS_LEFT
                cefpython.EVENTFLAG_IS_RIGHT
        """

    # bool OnKeyEvent(Browser browser, KeyEvent event, MSG*|GdkEvent*|NSEvent* eventHandle)
    # def OnKeyEvent(self, browser, event, eventHandle):



    # LoadHandler -------------------------------------------------------------

    # def OnLoadStart(self, browser, frame):
        """ Called when the browser begins loading a frame. The |frame| value will never be empty -- call the IsMain() method to check
            if this frame is the main frame. Multiple frames may be loading at the same time.
            Sub-frames may start or continue loading after the main frame load has ended. This method may not be called for a particular frame
            if the load request for that frame fails. For notification of overall browser load status use DisplayHandler.OnLoadingStateChange instead.
        """

    # void OnLoadEnd(Browser browser, Frame frame, int httpStatusCode)
    # def OnLoadEnd(self, browser, frame, httpStatusCode):
        """ Called when the browser is done loading a frame. The |frame| value will never be empty -- call the IsMain() method to check
            if this frame is the main frame. Multiple frames may be loading at the same time.
            Sub-frames may start or continue loading after the main frame load has ended.
            This method will always be called for all frames irrespective of whether the request completes successfully.
            This event behaves like window.onload, it waits for all the content to load (e.g. images),
            there is currently no callback for a DOMContentLoaded event, see Issue 32.
            There are some cases when this callback won't get called, see this topic: http://www.magpcss.org/ceforum/viewtopic.php?f=6&t=10906
        """

    # void OnLoadError(Browser browser, Frame frame, NetworkError errorCode, list& errorText, string failedUrl)
    # def OnLoadError(self, browser, frame, errorCode, errorText, failedUrl):
        """ Called when the resource load for a navigation fails or is canceled. |errorCode| is the error code number,
            |errorText[0]| is the error text and |failedUrl| is the URL that failed to load.
            See net\base\net_error_list.h for complete descriptions of the error codes.
        """

    # void OnRendererProcessTerminated(Browser browser, TerminationStatus status)
    # def OnRendererProcessTerminated(self, browser, status):
        """ Called when the render process terminates unexpectedly. |status| indicates how the process terminated.
            TerminationStatus constants:
            cefpython.TS_ABNORMAL_TERMINATION - Non-zero exit status.
            cefpython.TS_PROCESS_WAS_KILLED - SIGKILL or task manager kill.
            cefpython.TS_PROCESS_CRASHED - Segmentation fault.
        """

    # void OnPluginCrashed(Browser browser, string pluginPath)
    # def OnPluginCrashed(self, browser, pluginPath):
        """ Called when a plugin has crashed. |pluginPath| is the path of the plugin that crashed.
        """


    # RenderHandler -----------------------------------------------------------

    # bool GetRootScreenRect(Browser browser, list out rect)
    # def GetRootScreenRect(self, browser, rect):
        """ Called to retrieve the root window rectangle in screen coordinates.
            Return true if the rectangle was provided.
        """

    # bool GetViewRect(Browser browser, list out rect)
    # def GetViewRect(self, browser, rect):
        """ Called to retrieve the view rectangle which is relative to screen coordinates.
            Return true if the rectangle was provided.
            The rect list should contain 4 elements: [x, y, width, height].
        """

    # bool GetScreenPoint(Browser browser, int viewX, int viewY, list out screenCoordinates)
    # def GetScreenPoint(self, browser, viewX, viewY, screenCoordinates):
        """ Called to retrieve the translation from view coordinates to actual screen coordinates.
            Return true if the screen coordinates were provided.
            The screenCoordinates list should contain 2 elements: [x, y].
        """

    # void OnPopupShow(Browser browser, bool show)
    # def OnPopupShow(self, browser, show):
        """ Called when the browser wants to show or hide the popup widget.
            The popup should be shown if |show| is true and hidden if |show| is false.
        """

    # void OnPopupSize(Browser browser, list rect)
    # def OnPopupSize(self, browser, rect):
        """ Called when the browser wants to move or resize the popup widget. |rect| contains the new location and size.
            The rect list should contain 4 elements: [x, y, width, height].
        """

    # void OnPaint(Browser browser, int paintElementType, list out dirtyRects, PaintBuffer buffer, int width, int height)
    # def OnPaint(self, browser, paintElementType, dirtyRects, buffer, width, height):
        """ Called when an element should be painted. |paintElementType| indicates whether the element is the view or the popup widget.
            |buffer| contains the pixel data for the whole image. |dirtyRects| contains the set of rectangles that need to be repainted.
            On Windows |buffer| will be width*height*4 bytes in size and represents a BGRA image with an upper-left origin.
            The BrowserSettings.animation_frame_rate value controls the rate at which this method is called.
            paintElementType is one of:
            cefpython.PET_VIEW
            cefpython.PET_POPUP
            dirtyRects is a list of rects: [[x, y, width, height], [..]]
        """

    # void OnCursorChange(Browser browser, CursorHandle cursor)
    # def OnCursorChange(self, browser, cursor):
        """ Called when the browser window's cursor has changed. CursorHandle is an int pointer.
        """

    # void OnScrollOffsetChanged(Browser browser)
    # def OnScrollOffsetChanged(self, browser):
        """ Called when the scroll offset has changed.
        """


    # RequestHandler -----------------------------------------------------------

    # bool OnBeforeResourceLoad(Browser browser, Frame frame, Request request)
    # def OnBeforeResourceLoad(self, browser, frame, request):
        """ Called on the IO thread before a resource request is loaded. The |request| object may be modified.
            To cancel the request return true otherwise return false.
        """

    # ResourceHandler GetResourceHandler(Browser browser, Frame frame, Request request)
    # def GetResourceHandler(self, browser, frame, request):
        """ Called on the IO thread before a resource is loaded. To allow the resource to load normally return None.
            To specify a handler for the resource return a ResourceHandler object. The |request| object should not be modified in this callback.
            The ResourceHandler object is a python class that implements the ResourceHandler callbacks.
            Remember to keep a strong reference to this object while resource is being loaded.
            The GetResourceHandler example can be found in the wxpython-response.py script on Linux.
        """
    #     return None

    # void OnResourceRedirect(Browser browser, Frame frame, string oldUrl, list& newUrlOut)
    # def OnResourceRedirect(self, browser, frame, oldUrl, newUrlOut):
        """ Called on the IO thread when a resource load is redirected. The |oldUrl| parameter will contain the old URL.
        The newUrlOut[0] parameter will contain the new URL and can be changed if desired.
        """

    # bool GetAuthCredentials(Browser browser, Frame frame, bool isProxy, string host, int port, string realm, string scheme, AuthCallback callback) {
    # def GetAuthCredentials(self, browser, frame, isProxy, host, port, realm, scheme, callback):
        """ Called on the IO thread when the browser needs credentials from the user. |isProxy| indicates whether the host is a proxy server.
            |host| contains the hostname and |port| contains the port number. Return true to continue the request and call AuthCallback::Continue()
            when the authentication information is available. Return false to cancel the request.
            The AuthCallback object methods:
                void Continue(string username, string password)
                void Cancel()
        """

    # bool OnQuotaRequest(Browser browser, string originUrl, long newSize, QuotaCallback callback)
    # def OnQuotaRequest(self, browser, originUrl, newSize, callback):
        """ Called on the IO thread when javascript requests a specific storage quota size via the webkitStorageInfo.requestQuota function.
            |originUrl| is the origin of the page making the request. |newSize| is the requested quota size in bytes.
            Return true and call QuotaCallback::Continue() either in this method or at a later time to grant or deny the request.
            Return False to cancel the request.
            The QuotaCallback object methods:
            void Continue(bool allow)
            void Cancel()
        """

    # void OnProtocolExecution(Browser browser, string url, list& allowExecutionOut)
    # def OnProtocolExecution(self, browser, url, allowExecutionOut):
        """ Called on the UI thread to handle requests for URLs with an unknown protocol component.
            Set allowExecutionOut[0] to True to attempt execution via the registered OS protocol handler, if any.
            SECURITY WARNING: YOU SHOULD USE THIS METHOD TO ENFORCE RESTRICTIONS BASED ON SCHEME, HOST OR OTHER URL ANALYSIS BEFORE ALLOWING OS EXECUTION.
            There's no default implementation for OnProtocolExecution on Linux, you have to make OS system call on your own.
            You probably also need to use LoadHandler::OnLoadError() when implementing this on Linux.
        """
