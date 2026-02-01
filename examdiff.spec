# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Python ExamDiff Pro
Creates a standalone Windows executable. Guarded so missing optional assets
(icons/resources) do not break the build in development environments.
"""

from pathlib import Path

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        (p, p) for p in ['resources', 'plugins'] if Path(p).exists()
    ],
    hiddenimports=[
        'customtkinter',
        'tkinterdnd2',
        'pygments',
        'pygments.lexers',
        'pygments.styles',
        'chardet',
        'yaml',
        'reportlab',
        'PIL',
        'watchdog',
        'git',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PythonExamDiff',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to False for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icons/app_icon.ico' if Path('resources/icons/app_icon.ico').exists() else None,
    version_file='version_info.txt' if Path('version_info.txt').exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PythonExamDiff',
)
