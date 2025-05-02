#!/bin/bash
set -e

# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Install build dependencies
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade setuptools wheel twine

# Build distributions
python3 setup.py sdist bdist_wheel

# Check the distribution
python3 -m twine check dist/*

# Prompt before uploading to PyPI
echo ""
echo "The package is ready to upload to PyPI."
echo "Do you want to proceed with uploading? (y/n)"
read answer

if [ "$answer" == "y" ]; then
    echo "Uploading to PyPI..."
    python3 -m twine upload dist/*
    echo "Upload complete!"
else
    echo "Upload cancelled."
    echo "You can upload the package later with: python3 -m twine upload dist/*"
fi 