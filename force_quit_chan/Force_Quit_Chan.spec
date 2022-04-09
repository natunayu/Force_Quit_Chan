# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['Force_Quit_Chan.py'],
             pathex=['.\\'],
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
a.datas += [('on.png', '.\\on.png', 'DATA')]
a.datas += [('off.png', '.\\off.png', 'DATA')]
a.datas += [('force_quit_chan.bak', '.\\force_quit_chan.bak', 'DATA')]
a.datas += [('force_quit_chan.dat', '.\\force_quit_chan.dat', 'DATA')]
a.datas += [('force_quit_chan.dir', '.\\force_quit_chan.dir', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.datas,  
          [],
          name='Force_Quit_Chan',
          debug=False,
          strip=False,
          upx=True,
          console=False, )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Force_Quit_Chan')