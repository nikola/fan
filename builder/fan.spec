# coding: utf-8
import os
import inspect

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(inspect.stack()[0][1])), '..'))

def _getAssets(sourceDir, *args):
    for root, dirnames, filenames in os.walk(sourceDir):
        for filename in filenames:
            if filename.endswith(args):
                directory = os.path.dirname(os.path.normpath(os.path.join(root, filename))).replace(sourceDir, '')
                if directory.startswith('\\'):
                    directory = directory[1:]

                yield os.path.join(directory, filename).replace('\\', '/')

a = Analysis(
    ['../backend/start.py'],
    pathex=['../backend'],
    hiddenimports=[],
    hookspath=None,
    runtime_hooks=None,
)

a.datas.append(('assets/fan.ico', '../assets/fan.ico', 'DATA'))
a.datas.append(('config/default.json', '../config/default.json', 'DATA'))

for pathname in _getAssets(os.path.join(BASE_DIR, 'thirdparty'), '.exe', '.dll', '.pyd', '.pak', '.txt'):
    a.datas.append(('thirdparty/%s' % pathname, '../thirdparty/%s' % pathname, 'DATA'))

for pathname in _getAssets(os.path.join(BASE_DIR, 'frontend'), '.html', '.js', '.css', '.gif', '.otf'):
    a.datas.append(('frontend/%s' % pathname, '../frontend/%s' % pathname, 'DATA'))

pyz = PYZ(
    a.pure,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='fan.exe',
    debug=False,
    strip=None,
    upx=True,
    console=False,
    version='fan.version',
    icon='fan.ico',
)

# import subprocess
# subprocess.call([
#    "SIGNTOOL.EXE",
#    "/F", "path-to-key.pfx",
#    "/P", "your-password",
#    "/T", "time-stamping url",
#    exe.name
# ])
