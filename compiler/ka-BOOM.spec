# -*- mode: python -*-
from os import urandom
from PyInstaller.loader import pyi_crypto

block_cipher = pyi_crypto.PyiBlockCipher(key=urandom(32))

a = Analysis(
    ['./clean/pyi_bootloader.py'],
    pathex=['C:\\Users\\Niko\\Documents\\GitHub\\ka-BOOM\\compiler\clean'],
    hiddenimports=[],
    hookspath=None,
    runtime_hooks=None,
    cipher=block_cipher,
)

a.datas.append(('shaders/1e57809d2a5d461793d14bddb773a77a.cso', '../shaders/1e57809d2a5d461793d14bddb773a77a.cso', 'DATA'))
a.datas.append(('shaders/4ebc0ca1e8324ba6a134ca78b1ca3088.cso', '../shaders/4ebc0ca1e8324ba6a134ca78b1ca3088.cso', 'DATA'))
a.datas.append(('shaders/030c5b6d1e5715105943ac111d9671bf.cso', '../shaders/030c5b6d1e5715105943ac111d9671bf.cso', 'DATA'))
a.datas.append(('shaders/69dcab4a73aeec2113f69b61e6263da8.cso', '../shaders/69dcab4a73aeec2113f69b61e6263da8.cso', 'DATA'))
a.datas.append(('shaders/781354b1bf474046888a703d21148e65.cso', '../shaders/781354b1bf474046888a703d21148e65.cso', 'DATA'))
a.datas.append(('shaders/af37d08ae228a87dc6b265fd1019c97d.cso', '../shaders/af37d08ae228a87dc6b265fd1019c97d.cso', 'DATA'))
a.datas.append(('shaders/b1932b8b02de45bc9ec66ebf1c75bb15.cso', '../shaders/b1932b8b02de45bc9ec66ebf1c75bb15.cso', 'DATA'))
a.datas.append(('shaders/bd21190449b7e88db48fa0f580a8f666.cso', '../shaders/bd21190449b7e88db48fa0f580a8f666.cso', 'DATA'))
a.datas.append(('shaders/c9d25707d3a84c4d80fdb6b0789bdcf6.cso', '../shaders/c9d25707d3a84c4d80fdb6b0789bdcf6.cso', 'DATA'))
a.datas.append(('shaders/d2062963ddf644299341f12439990aa8.cso', '../shaders/d2062963ddf644299341f12439990aa8.cso', 'DATA'))
a.datas.append(('shaders/de8926be7f2d430fad66927ffadc9f9d.cso', '../shaders/de8926be7f2d430fad66927ffadc9f9d.cso', 'DATA'))
a.datas.append(('shaders/e7edf96693d14aa8a011da221782f4a6.cso', '../shaders/e7edf96693d14aa8a011da221782f4a6.cso', 'DATA'))

a.datas.append(('trident/blink.pak',                    '../trident/blink.pak',                     'DATA'))
a.datas.append(('trident/cef.pak',                      '../trident/cef.pak',                       'DATA'))
a.datas.append(('trident/d3dcompiler_46.dll',           '../trident/d3dcompiler_46.dll',            'DATA'))
a.datas.append(('trident/devtools_resources.pak',       '../trident/devtools_resources.pak',        'DATA'))
a.datas.append(('trident/ffmpegsumo.dll',               '../trident/ffmpegsumo.dll',                'DATA'))
a.datas.append(('trident/icon.ico',                     '../trident/icon.ico',                      'DATA'))
a.datas.append(('trident/icudt.dll',                    '../trident/icudt.dll',                     'DATA'))
a.datas.append(('trident/iexplore.exe',                 '../trident/iexplore.exe',                  'DATA'))
a.datas.append(('trident/libcef.dll',                   '../trident/libcef.dll',                    'DATA'))
a.datas.append(('trident/libEGL.dll',                   '../trident/libEGL.dll',                    'DATA'))
a.datas.append(('trident/libgfx.dll',                   '../trident/libgfx.dll',                    'DATA'))
a.datas.append(('trident/libGLESv2.dll',                '../trident/libGLESv2.dll',                 'DATA'))
a.datas.append(('trident/Microsoft.VC90.CRT.manifest',  '../trident/Microsoft.VC90.CRT.manifest',   'DATA'))
a.datas.append(('trident/msvcm90.dll',                  '../trident/msvcm90.dll',                   'DATA'))
a.datas.append(('trident/msvcp90.dll',                  '../trident/msvcp90.dll',                   'DATA'))
a.datas.append(('trident/msvcr90.dll',                  '../trident//msvcr90.dll',                  'DATA'))

a.datas.append(('tools/convert.exe',  '../tools/convert.exe', 'DATA'))
a.datas.append(('tools/cwebp.exe',    '../tools/cwebp.exe',   'DATA'))
a.datas.append(('tools/vcomp100.dll', '../tools/vcomp100.dll','DATA'))

# a.binaries = [x for x in a.binaries if x[0].lower() != 'kernel32.dll']
pyz = PYZ(
    a.pure, cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts, #  + [('O','','OPTION')],
    a.binaries,
    a.zipfiles,
    a.datas,
    name='ka-BOOM.exe',
    debug=False,
    strip=None,
    upx=True,
    console=True,
    manifest='./ka-BOOM.exe.manifest',
    version='./ka-BOOM.version',
    icon='./ka-BOOM.ico',
)
