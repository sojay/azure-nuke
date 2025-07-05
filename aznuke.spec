# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

# Try to import pyfiglet, but don't fail if it's not available
try:
    import pyfiglet
    pyfiglet_data = [(pyfiglet.__path__[0] + '/fonts', 'pyfiglet/fonts')]
    pyfiglet_imports = ['pyfiglet', 'pyfiglet.fonts']
except ImportError:
    pyfiglet_data = []
    pyfiglet_imports = []

# Determine data files based on what exists
data_files = []
if os.path.exists('config/exclusions.yaml'):
    data_files.append(('config/exclusions.yaml', 'config'))
if os.path.exists('aznuke/config/exclusions.yaml'):
    data_files.append(('aznuke/config/exclusions.yaml', 'aznuke/config'))

a = Analysis(
    ['cli_entry.py'],
    pathex=[],
    binaries=[],
    datas=data_files + pyfiglet_data,
    hiddenimports=[
        'azure.identity',
        'azure.mgmt.resource',
        'azure.mgmt.subscription',
        'azure.mgmt.compute',
        'azure.mgmt.network',
        'azure.mgmt.storage',
        'azure.mgmt.keyvault',
        'azure.mgmt.monitor',
        'azure.core',
        'azure.core.credentials',
        'azure.core.exceptions',
        'yaml',
        'colorama',
        'tqdm',
        'aznuke',
        'aznuke.cli',
        'aznuke.src',
        'aznuke.src.auth',
        'aznuke.src.discovery',
        'aznuke.src.filtering',
        'aznuke.src.deletion',
        'aznuke.src.safety',
        'aznuke.src.animations',
        'aznuke.src.dependencies',
        'asyncio',
        'argparse',
        'json',
        'msal',
        'msal_extensions',
        'pkg_resources',
    ] + pyfiglet_imports,
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='aznuke',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
) 