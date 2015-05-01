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

# upx --compress-exports=0 madHcCtrl.exe

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
