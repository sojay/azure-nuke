# Publishing to PyPI

This document provides instructions for publishing the `aznuke` package to PyPI.

## Prerequisites

- A PyPI account
- Twine installed: `pip install twine`
- Wheel installed: `pip install wheel`

## Steps to Publish

1. Update the version number in `setup.py`

2. Make sure all changes are committed to git

3. Run the publication script:

```bash
./pypi_publish.sh
```

OR follow these steps manually:

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build distributions
python setup.py sdist bdist_wheel

# Check the distribution
twine check dist/*

# Upload to PyPI (you'll be prompted for your PyPI credentials)
twine upload dist/*
```

## Testing Before Publishing

To test the package locally before publishing:

1. Build the package:
```bash
python setup.py sdist bdist_wheel
```

2. Install it locally (in a virtual environment):
```bash
pip install dist/aznuke-X.Y.Z-py3-none-any.whl
```

3. Test that it works:
```bash
aznuke --help
```

## Creating a PyPI API Token

Rather than using your PyPI password, it's recommended to create an API token:

1. Log in to PyPI and go to your account settings
2. Under "API tokens", create a new token with appropriate scope
3. Use this token as your password when uploading with Twine

You can save your credentials in a `~/.pypirc` file:

```
[pypi]
username = __token__
password = pypi-xxxx-xxxx-xxxx-xxxx
``` 