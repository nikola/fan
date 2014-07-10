# coding: utf-8
"""
"""
__author__ = 'Nikola Klaric (nikola@generic.company)'
__copyright__ = 'Copyright (c) 2013-2014 Nikola Klaric'

import os.path
import re
import pylzma
# TODO: pack fonts, too !!!


RESOURCES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'frontend')
BLOBS_PATH = os.path.join(RESOURCES_PATH, '..', 'backend', 'blobs')


RESOURCES_SCRIPT = [
    # 'vendor/lodash/lodash.min.js',
    # 'vendor/bacon/bacon.min.js',
    'vendor/cortex/cortex.min.js',
    'vendor/jquery/jquery.min.js',
    # 'vendor/jquery/jquery.swipe-events.js',

    # 'vendor/jquery/jquery.waitforimages.min.js',
    'vendor/misc/color-thief.min.js',
    'vendor/misc/keypress.min.js',

    'vendor/velocity/velocity.min.js',
    'vendor/velocity/velocity.ui.js',

    'app/js/lib/sockets.js',
    'app/js/lib/colors.js',
    'app/js/lib/l10n.js',
    'app/js/lib/receiver.js',
    'app/js/lib/hotkeys.js',
    'app/js/lib/lang.js',
    'app/js/lib/config.js',
    'app/js/lib/grid.js',
    'app/js/lib/detail.js',
    'app/js/app.js',
]

RESOURCES_STYLE = [
    'app/css/fonts.css',
    'app/css/icons.css',

    'app/css/app.css',

    'app/css/buttons.css',
    'app/css/config.css',
    'app/css/grid.css',
    'app/css/detail.css',
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
    pathname = os.path.join(RESOURCES_PATH, 'app', 'html', 'boot.html')
    html = _readStrip(pathname, '{};')
    compressed = pylzma.compress(html)
    with open(os.path.join(BLOBS_PATH, 'b1932b8b02de45bc9ec66ebf1c75bb15'), 'wb') as fp:
        fp.write(compressed)

    # Compress GUI.
    pathname = os.path.join(RESOURCES_PATH, 'app', 'html', 'gui.html')
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


if __name__ == '__main__':
    run()
