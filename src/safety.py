"""Compatibility wrapper for :mod:`aznuke.src.safety`.

The canonical implementation lives under ``aznuke.src``. This module keeps
legacy ``src.safety`` imports working without maintaining a second copy of the
logic.
"""

from aznuke.src.safety import *  # noqa: F401,F403
