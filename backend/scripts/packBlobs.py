# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os.path
import re
import pylzma
from hashlib import md5 as MD5


RESOURCES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..') # , 'frontend')
BLOBS_PATH = os.path.join(RESOURCES_PATH, 'backend', 'blobs')


RESOURCES_SCRIPT = [
    # 'vendor/lodash/lodash.min.js',
    # 'vendor/bacon/bacon.min.js',
    'frontend/vendor/cortex/cortex.min.js',
    'frontend/vendor/jquery/jquery.min.js',
    # 'vendor/jquery/jquery.swipe-events.js',

    # 'vendor/jquery/jquery.waitforimages.min.js',
    'frontend/vendor/misc/color-thief.min.js',
    'frontend/vendor/misc/keypress.min.js',

    'frontend/vendor/velocity/velocity.min.js',
    'frontend/vendor/velocity/velocity.ui.js',

    'frontend/app/js/lib/sockets.js',
    'frontend/app/js/lib/colors.js',
    'frontend/app/js/lib/l10n.js',
    'frontend/app/js/lib/receiver.js',
    'frontend/app/js/lib/hotkeys.js',
    'frontend/app/js/lib/lang.js',
    'frontend/app/js/lib/config.js',
    'frontend/app/js/lib/grid.js',
    'frontend/app/js/lib/detail.js',
    'frontend/app/js/app.js',
]

RESOURCES_STYLE = [
    'frontend/app/css/fonts.css',
    'frontend/app/css/icons.css',

    'frontend/app/css/app.css',

    'frontend/app/css/buttons.css',
    'frontend/app/css/config.css',
    'frontend/app/css/grid.css',
    'frontend/app/css/detail.css',
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
    pathname = os.path.join(RESOURCES_PATH, 'frontend', 'app', 'html', 'boot.html')
    html = _readStrip(pathname, '{};')
    compressed = pylzma.compress(html)
    with open(os.path.join(BLOBS_PATH, 'b1932b8b02de45bc9ec66ebf1c75bb15'), 'wb') as fp:
        fp.write(compressed)

    # Compress GUI.
    pathname = os.path.join(RESOURCES_PATH, 'frontend', 'app', 'html', 'gui.html')
    with open(pathname, 'rb') as fp:
        html = fp.read()
    html = re.sub(r'>\s*<', '><', html)

    stylesheetContent = []
    for pathname in RESOURCES_STYLE:
        content = _readStrip(os.path.join(RESOURCES_PATH, pathname), '{};,')
        stylesheetContent.append(content)
    stylesheetsAmalgamated = ''.join(stylesheetContent)

    scriptContent = []
    for pathname in RESOURCES_SCRIPT:
        content = _readStrip(os.path.join(RESOURCES_PATH, pathname), '{},')
        scriptContent.append(content)
    scriptsAmalgamated = ''.join(scriptContent)

    html = html.replace('</head>', '<script>%s</script><style>%s</style></head>' % (scriptsAmalgamated, stylesheetsAmalgamated))

    compressed = pylzma.compress(html)
    with open(os.path.join(BLOBS_PATH, 'c9d25707d3a84c4d80fdb6b0789bdcf6'), 'wb') as fp:
        fp.write(compressed)

    # Compress fonts.
    for pathname in RESOURCES_FONT:
        with open(os.path.join(RESOURCES_PATH, pathname), 'rb') as fp:
            ttf = fp.read()
        compressed = pylzma.compress(ttf)

        identifier = os.path.basename(pathname).replace('.ttf', '')
        md5 = MD5()
        md5.update(identifier)
        filename = md5.hexdigest()

        with open(os.path.join(BLOBS_PATH, filename), 'wb') as fp:
            fp.write(compressed)


if __name__ == '__main__':
    run()
