# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os.path
import re
from hashlib import md5 as MD5

from utils.fs import writeProcessedStream

BASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..')
BLOBS_PATH = os.path.join(BASE_DIR, 'backend', 'filters')


RESOURCES_CONFIG_CSS = [
    'frontend/app/css/fonts.css',
    'frontend/app/css/icons.css',

    'frontend/app/css/app.css',

    'frontend/app/css/buttons.css',
    'frontend/app/css/configure.css',
]

RESOURCES_CONFIG_JS = [
    'frontend/app/js/thirdparty/jquery.min.js',

    'frontend/app/js/thirdparty/keypress.min.js',

    'frontend/app/js/thirdparty/velocity.min.js',
    'frontend/app/js/thirdparty/velocity.ui.min.js',

    'frontend/app/js/lib/l10n.js',
    'frontend/app/js/lib/hotkeys.js',
    'frontend/app/js/lib/lang.js',
    'frontend/app/js/lib/sockets.js',

    'frontend/app/js/configure.js',
]

RESOURCES_GUI_CSS = [
    'frontend/app/css/fonts.css',
    'frontend/app/css/icons.css',

    'frontend/app/css/app.css',

    'frontend/app/css/buttons.css',
    'frontend/app/css/grid.css',
    'frontend/app/css/detail.css',
]

RESOURCES_GUI_JS = [
    'frontend/app/js/thirdparty/cortex.min.js',
    'frontend/app/js/thirdparty/jquery.min.js',

    'frontend/app/js/thirdparty/protovis.js',
    'frontend/app/js/thirdparty/mmcq.js',
    'frontend/app/js/thirdparty/keypress.min.js',

    'frontend/app/js/thirdparty/velocity.min.js',
    'frontend/app/js/thirdparty/velocity.ui.min.js',

    'frontend/app/js/lib/sockets.js',
    'frontend/app/js/lib/colors.js',
    'frontend/app/js/lib/l10n.js',
    'frontend/app/js/lib/receiver.js',
    'frontend/app/js/lib/hotkeys.js',
    'frontend/app/js/lib/lang.js',
    'frontend/app/js/lib/menu.js',
    'frontend/app/js/lib/grid.js',
    'frontend/app/js/lib/detail.js',

    'frontend/app/js/gui.js',
]

RESOURCES_FONT = [
    'frontend/fonts/regular.ttf',
    'frontend/fonts/bold.ttf',
    'frontend/fonts/italic.ttf',
    'frontend/fonts/icons.ttf',
]


def _readStrip(filename, delimiters='{}'):
    with open(filename, 'rU') as fp:
        content = fp.read()

    # Remove whitespace between tags.
    content = re.sub(r'>\s*<', '><', content)

    # Remove comments.
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.MULTILINE|re.DOTALL)

    # Remove leading whitespace.
    content = re.sub(r'(?<=\n) +', '', content)

    # Remove trailing whitespace.
    content = re.sub(r' +(?=\n)', '', content)

    # Remove newlines.
    content = re.sub(r'\r\n', '\n', content)
    content = re.sub(r'\n+', '\n', content)
    content = re.sub(r'(?<=[' + delimiters + '])\n', '', content)

    return content


def run():
    # Compress bootloader.
    pathname = os.path.join(BASE_DIR, 'frontend', 'app', 'html', 'load.html')
    html = _readStrip(pathname, '{};')
    writeProcessedStream('b1932b8b02de45bc9ec66ebf1c75bb15', html)

    # Compress configurator.
    pathname = os.path.join(BASE_DIR, 'frontend', 'app', 'html', 'configure.html')
    with open(pathname, 'rb') as fp:
        html = fp.read()
    html = re.sub(r'>\s*<', '><', html)

    stylesheetContent = []
    for pathname in RESOURCES_CONFIG_CSS:
        content = _readStrip(os.path.join(BASE_DIR, pathname), '{};,')
        stylesheetContent.append(content)
    stylesheetsAmalgamated = ''.join(stylesheetContent)

    scriptContent = []
    for pathname in RESOURCES_CONFIG_JS:
        content = _readStrip(os.path.join(BASE_DIR, pathname), '{},')
        scriptContent.append(content)
    scriptsAmalgamated = ''.join(scriptContent)

    html = html.replace('</head>', '<script>%s</script><style>%s</style></head>' % (scriptsAmalgamated, stylesheetsAmalgamated))

    writeProcessedStream('e7edf96693d14aa8a011da221782f4a6', html)

    # Compress GUI.
    pathname = os.path.join(BASE_DIR, 'frontend', 'app', 'html', 'gui.html')
    with open(pathname, 'rb') as fp:
        html = fp.read()
    html = re.sub(r'>\s*<', '><', html)

    stylesheetContent = []
    for pathname in RESOURCES_GUI_CSS:
        content = _readStrip(os.path.join(BASE_DIR, pathname), '{};,')
        stylesheetContent.append(content)
    stylesheetsAmalgamated = ''.join(stylesheetContent)

    scriptContent = []
    for pathname in RESOURCES_GUI_JS:
        content = _readStrip(os.path.join(BASE_DIR, pathname), '{},')
        scriptContent.append(content)
    scriptsAmalgamated = ''.join(scriptContent)

    html = html.replace('</head>', '<script>%s</script><style>%s</style></head>' % (scriptsAmalgamated, stylesheetsAmalgamated))

    writeProcessedStream('c9d25707d3a84c4d80fdb6b0789bdcf6', html)

    # Compress fonts.
    for pathname in RESOURCES_FONT:
        with open(os.path.join(BASE_DIR, pathname), 'rb') as fp:
            ttf = fp.read()

        identifier = os.path.basename(pathname).replace('.ttf', '')
        md5 = MD5()
        md5.update(identifier)
        filename = md5.hexdigest()

        writeProcessedStream(filename, ttf)

    # Compress MPC-HC configuration.
    from settings.player import MPCHC_INI
    writeProcessedStream('4ebc0ca1e8324ba6a134ca78b1ca3088', MPCHC_INI)


if __name__ == '__main__':
    run()
