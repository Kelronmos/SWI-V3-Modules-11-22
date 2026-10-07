"""Conservative platform detection — no automatic capability grants."""
from __future__ import annotations

import platform

from .contract import PlatformInfo


def detect_platform() -> PlatformInfo:
    system = platform.system().lower()
    if system == "linux":
        name = "linux"
    elif system == "darwin":
        name = "macos"
    else:
        name = system or "unknown"

    # Do not automatically grant capabilities merely because OS is recognized.
    return PlatformInfo(
        name=name,
        version=platform.release(),
        architecture=platform.machine(),
        capabilities=frozenset(),
    )
