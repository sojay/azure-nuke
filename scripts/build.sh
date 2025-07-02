#!/bin/bash
set -e

# Build script for Azure Nuke
echo "Building Azure Nuke..."

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Install build dependencies
pip install build twine pyinstaller

# Build Python package
python -m build

# Build binary with PyInstaller
pyinstaller aznuke.spec --clean

echo "Build completed successfully!"
echo "Binary: dist/aznuke"
echo "Python package: dist/aznuke-*.whl" 