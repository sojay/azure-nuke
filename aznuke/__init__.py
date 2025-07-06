"""Azure Nuke - A powerful CLI tool for scanning and cleaning up Azure resources."""

try:
    from ._version import version as __version__
except ImportError:
    # Fallback for development installations
    __version__ = "unknown"

__author__ = "Samuel Okorie"
__email__ = "thesamokorie@gmail.com"

from .cli import main

__all__ = ["main"] 