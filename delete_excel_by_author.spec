# -*- mode: python ; coding: utf-8 -*-


a = Analysis(    ['delete_excel_by_author.py'],
    pathex=[],
    binaries=[
        ('exiftool.exe', '.'),
        ('exiftool_files/exiftool.pl', 'exiftool_files'),
        ('exiftool_files/perl.exe', 'exiftool_files'),
        ('exiftool_files/perl532.dll', 'exiftool_files'),
        ('exiftool_files/libgcc_s_seh-1.dll', 'exiftool_files'),
        ('exiftool_files/libstdc++-6.dll', 'exiftool_files'),
        ('exiftool_files/libwinpthread-1.dll', 'exiftool_files'),
    ],
    datas=[
        ('exiftool_files/lib', 'lib'),
    ],
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
    [],
    exclude_binaries=True,
    name='delete_excel_by_author',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='delete_excel_by_author',
)
