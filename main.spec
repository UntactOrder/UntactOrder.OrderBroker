# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['src\main\main.py'],
             pathex=['src\main'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [('server_logo.ico','icon\server_logo.ico','DATA'),
            ('version.rc','src\main\resource\version.rc','DATA'),
            ('version.rc','src\main\resource\new_order_sound.mp3','DATA')
			]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='PosServer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True,
          icon='icon\server_logo.ico',
          version='src\main\resource\version.rc',
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='main')
