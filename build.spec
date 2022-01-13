# -*- mode: python ; coding: utf-8 -*-
import os
import sys


debug_mode = False
console_mode = False


# CHECK PYSIDE VERSION
PYSIDE_VERSION = ['PySide6.QtSvg', 'shiboken6']
EXCLUDES = ['PySide6.QtNetwork', 'PySide6.QtQml']
with open("src/main/qt_core.py", "rt", encoding='utf-8') as f:
    for line in f.readlines():
        if "SUPPORT_WINDOWS_7" in line:
            if "True" in line:
                PYSIDE_VERSION = ['PySide2.QtSvg', 'shiboken2']
                EXCLUDES = ['PySide2.QtNetwork', 'PySide2.QtQml']
                break
            elif "False" in line:
                break


# GET CRYTO KEY
key_path = "build.key"
if not os.path.isfile(key_path):
    print("ERROR: build.key not found", flush=True)
    while True:
        key = input("16자리 암호화 키를 입력하세요 : ")
        if len(key) == 16:
            with open(key_path, "wt", encoding='utf-8') as f:
                f.write(key)
            break
        else:
            print("ERROR: 입력된 키가 16자리가 아닙니다.")
with open("build.key", "rt", encoding='utf-8') as f:
    CRYPTO_KEY = f.read()
block_cipher = pyi_crypto.PyiBlockCipher(key=CRYPTO_KEY)


# PARSE INFO FROM SETTINGS.JSON
from src.main.gui.core.json_settings import Settings
settings = Settings().items
__NAME__ = settings['app_name'].split()[0]  # 화이트 스페이스 이전까지만 반영
__PRODUCT_NAME__ = settings['app_name']
__DESCRIPTION__ = settings['description']
## 버전 스트링은 4개의 영역으로만 구성되어야 하고, alpha&beta 표기는 '-'기호만을 이용하여 표기해야 한다.
__VERSION__ = settings['version'][1:]  # 맨 앞 v 문자 제거
__VER_SPL__ = __VERSION__.split('-')[0].split('.')[:4]
__COPYRIGHT__ = settings['copyright']
__COMPANY_NAME__ = settings['company_name']


# CREATE VERSION.RC FILE
version = f"""# UTF-8
#
VSVersionInfo(
  ffi=FixedFileInfo(
# filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
# Set not needed items to zero 0.
filevers=({__VER_SPL__[0]}, {__VER_SPL__[1]}, {__VER_SPL__[2]}, {__VER_SPL__[3]}),
prodvers=({__VER_SPL__[0]}, {__VER_SPL__[1]}, {__VER_SPL__[2]}, {__VER_SPL__[3]}),
# Contains a bitmask that specifies the valid bits 'flags'r
mask=0x3f,
# Contains a bitmask that specifies the Boolean attributes of the file.
flags=0x0,
# The operating system for which this file was designed.
# 0x4 - NT and there is no need to change it.
OS=0x40004,
# The general type of file.
# 0x1 - the file is an application.
fileType=0x1,
# The function of the file.
# 0x0 - the function is not defined for this fileType
subtype=0x0,
# Creation date and time stamp.
date=(0, 0)
),
  kids=[
StringFileInfo(
  [
  StringTable(
    u'040904B0',
    [StringStruct(u'CompanyName', u'{__COMPANY_NAME__}'),
    StringStruct(u'FileDescription', u'{__DESCRIPTION__}'),
    StringStruct(u'FileVersion', u'{__VERSION__}'),
    StringStruct(u'InternalName', u'{__NAME__}'),
    StringStruct(u'LegalCopyright', u'{__COPYRIGHT__}'),
    StringStruct(u'OriginalFilename', u'{__NAME__}.exe'),
    StringStruct(u'ProductName', u'{__PRODUCT_NAME__}'),
    StringStruct(u'ProductVersion', u'{__VERSION__}')])
  ]),
VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
if not os.path.isdir('build'):
    os.mkdir('build')
with open('build/version.rc', 'wt', encoding='utf-8') as f:
    f.write(version)


# BUILD
HIDDEN_IMPORTS = PYSIDE_VERSION + []  # write something in [] to import
EXCLUDES = EXCLUDES + []  # write something in [] to exclude

a = Analysis(
    ['src/main/main.py'],
    pathex=[],
    binaries=[],
    datas=[('res/*', 'res')],
    hiddenimports=HIDDEN_IMPORTS,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=EXCLUDES,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

#a.datas += [('icon.ico', 'icon.ico', 'DATA')
#			]  # some files to add (--add-data option)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

if input("\n\n하나의 파일로 압축할까요? (라이센스 주의!; PySide6의 경우 라이센스 위반) (y to yes) : ") == "y":
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name=__NAME__,
        debug=debug_mode,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=console_mode,
        icon='res/icon.ico',
        version='build/version.rc',
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name=__NAME__,
        debug=debug_mode,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        console=console_mode,
        icon='res/icon.ico',
        version='build/version.rc',
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None
    )

    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=False,
        upx_exclude=[],
        name=__NAME__
    )
