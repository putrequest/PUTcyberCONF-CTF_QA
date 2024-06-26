# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('./assets/check_icon/circle-question-solid.png', 'assets/check_icon'), ('./assets/check_icon/circle-check-solid.png', 'assets/check_icon'), ('./assets/check_icon/circle-xmark-solid.png', 'assets/check_icon'), ('./assets/app_icon/icon.ico', 'assets/app_icon'), ('./assets/fonts/AnonymousPro-Bold.ttf', 'assets/fonts'), ('./assets/fonts/AtkinsonHyperlegible-Regular.ttf', 'assets/fonts')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CTF-QA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/app_icon/icon.ico',
)
