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

CEF_CMD_LINE_SETTINGS = {
    # https://code.google.com/p/chromiumembedded/source/browse/trunk/cef3/libcef/common/cef_switches.cc
    'disable-javascript-open-windows':      '',
    'disable-javascript-close-windows':     '',
    'disable-javascript-access-clipboard':  '',
    'disable-javascript-dom-paste':         '',
    'disable-text-area-resize':             '',
    'disable-tab-to-links':                 '',
    # http://peter.sh/experiments/chromium-command-line-switches/
    'no-proxy-server':                      '',
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
    # 'enable-benchmarking':                  '',
    # 'no-displaying-insecure-content':       '',
    'no-pings':                             '',
    'no-referrers':                         '',
    'noerrdialogs':                         '',

    # 'disable-threaded-compositing':         '',
    # 'disable-accelerated-compositing':      '',
    # 'enable-software-compositing':          '',
    # 'disable-gpu-compositing':              '',
    # 'disable-gpu-vsync': '',
}

CEF_APP_SETTINGS = {
    'multi_threaded_message_loop':  False,
    'ignore_certificate_errors':    True,
    'log_file':                     '',
    'locale':                       'en-US',
    'pack_loading_disabled':        1,
    # 'auto_zooming':                 '',
    # 'downloads_enabled':            False,
    # 'remote_debugging_port ':       -1,
}

CEF_BROWSER_SETTINGS = dict(
    # default_encoding = "",
    universal_access_from_file_urls_allowed = False,
    file_access_from_file_urls_allowed = False,
    javascript_open_windows_disallowed = True,
    javascript_close_windows_disallowed = True,
    javascript_access_clipboard_disallowed = True,
    dom_paste_disabled = True,
    java_disabled = True,
    plugins_disabled = True,
    text_area_resize_disabled = True,
    # application_cache_disabled = True,
    databases_disabled = True,
    local_storage_disabled = True,
    tab_to_links_disabled = True,
    # pack_loading_disabled = True,

    # accelerated_compositing_disabled = True,
    # webgl_disabled = True,
)

CEF_REMOTE_DEBUGGING_PORT = 8090
