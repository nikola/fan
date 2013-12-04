# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

import os
from utils.win32 import getAppStoragePathname

CHROME_BROWSER_SETTINGS = dict(
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

PROJECT_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

DB_PERSISTENCE_PATH = os.path.join(getAppStoragePathname("ka-boom", "Generic Company"), "data")

SERVER_HEADERS = {
    "Server": "Microsoft-IIS/7.5",
    "X-Powered-By": "ASP.NET",
    "X-AspNet-Version": "4.0.30319",
    "X-AspNetMvc-Version": "3.0",
}
