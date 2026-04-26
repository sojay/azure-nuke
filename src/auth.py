"""Compatibility wrapper for :mod:`aznuke.src.auth`.

The canonical implementation lives under ``aznuke.src``. This module keeps
legacy ``src.auth`` imports working without maintaining a second copy of the
logic.
"""

from aznuke.src.auth import *  # noqa: F401,F403
