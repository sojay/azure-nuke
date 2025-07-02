#!/bin/bash
set -e

# Release script for Azure Nuke
if [ $# -eq 0 ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 0.1.4"
    exit 1
fi

VERSION=$1
echo "Preparing release for version $VERSION..."

# Update version in setup.py and pyproject.toml
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" setup.py
sed -i "s/version = \"[^\"]*\"/version = \"$VERSION\"/" pyproject.toml

# Update version in aznuke module
sed -i "s/__version__ = \"[^\"]*\"/__version__ = \"$VERSION\"/" aznuke/__init__.py

# Create git tag
git add .
git commit -m "chore: bump version to $VERSION"
git tag "v$VERSION"

echo "Release $VERSION prepared!"
echo "Push with: git push origin main --tags"
echo "Then create a GitHub release to trigger the build process." 