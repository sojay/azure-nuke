"""Compatibility wrapper for :mod:`aznuke.src.animations`.

The canonical implementation lives under ``aznuke.src``. This module keeps
legacy ``src.animations`` imports working without maintaining a second copy of the
logic.
"""

from aznuke.src.animations import *  # noqa: F401,F403
