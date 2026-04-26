"""Compatibility wrapper for :mod:`aznuke.src.dependencies`.

The canonical implementation lives under ``aznuke.src``. This module keeps
legacy ``src.dependencies`` imports working without maintaining a second copy of the
logic.
"""

from aznuke.src.dependencies import *  # noqa: F401,F403
