# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

CEF_CMD_LINE_SETTINGS = {
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
}

CEF_APP_SETTINGS = {
    'cache_path':                  '',
    'multi_threaded_message_loop': False,
    'ignore_certificate_errors':   True,
    'log_file':                    '',
    'locale':                      'he',
}

CEF_BROWSER_SETTINGS = dict(
    # default_encoding = "",
    universal_access_from_file_urls_allowed = True,
    file_access_from_file_urls_allowed = True,
    javascript_open_windows_disallowed = True,
    javascript_close_windows_disallowed = True,
    javascript_access_clipboard_disallowed = True,
    java_disabled = True,
    plugins_disabled = True,
    text_area_resize_disabled = True,
    application_cache_disabled = True,
    # pack_loading_disabled = True,
)

CEF_REAL_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.80 Safari/537.36'
