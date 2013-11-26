# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

import os
# from utils.agent import getUserAgent

CHROME_BROWSER_SETTINGS = dict(
    universal_access_from_file_urls_allowed = True,
    file_access_from_file_urls_allowed = True,

    # author_and_user_styles_disabled = True,
    # default_encoding = "",
    javascript_open_windows_disallowed = True,
    javascript_close_windows_disallowed = True,
    javascript_access_clipboard_disallowed = True,
    java_disabled = True,
    plugins_disabled = True,
    text_area_resize_disabled = True,
)

# CHROME_USER_AGENT = getUserAgent()

PROJECT_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

SERVER_HEADERS = {
    "Server": "Microsoft-IIS/7.5",
    "X-Powered-By": "ASP.NET",
    "X-AspNet-Version": "4.0.30319",
    "X-AspNetMvc-Version": "3.0",
}
