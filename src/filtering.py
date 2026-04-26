"""Compatibility wrapper for :mod:`aznuke.src.filtering`.

The canonical implementation lives under ``aznuke.src``. This module keeps
legacy ``src.filtering`` imports working without maintaining a second copy of the
logic.
"""

from aznuke.src.filtering import *  # noqa: F401,F403
