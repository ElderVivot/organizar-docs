# -*- mode: python ; coding: utf-8 -*-

arquivos = [
    ('./env.json', '.')
]


a = Analysis(
    ['./src/__main__.py'],
    pathex=['./src'],
    binaries=[],
    datas=arquivos,
    hiddenimports=['PySimpleGUI', 'tk', '_tkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='organizar_docs',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
