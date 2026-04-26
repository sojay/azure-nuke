"""Compatibility wrapper for :mod:`aznuke.src.discovery`.

The canonical implementation lives under ``aznuke.src``. This module keeps
legacy ``src.discovery`` imports working without maintaining a second copy of the
logic.
"""

from aznuke.src.discovery import *  # noqa: F401,F403
