"""Linux adapter — observation only."""
from __future__ import annotations

from .capabilities import detect_platform
from .contract import PlatformInfo


def get_platform() -> PlatformInfo:
    info = detect_platform()
    if info.name != "linux":
        raise RuntimeError("Linux adapter used on non-Linux platform")
    return info
