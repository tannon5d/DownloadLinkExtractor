from kivy.deps import sdl2, glew
# -*- mode: python -*-

block_cipher = None


a = Analysis(['DownloadLinkExtractor.py'],
             pathex=['D:\\OneDrive\\Python\\DownloadLinkExtractor'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
		  *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          [],
          name='DownloadLinkExtractor',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
