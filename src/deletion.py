"""Compatibility wrapper for :mod:`aznuke.src.deletion`.

The canonical implementation lives under ``aznuke.src``. This module keeps
legacy ``src.deletion`` imports working without maintaining a second copy of the
logic.
"""

from aznuke.src.deletion import *  # noqa: F401,F403
