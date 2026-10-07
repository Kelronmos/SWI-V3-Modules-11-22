"""macOS adapter — observation only."""
from __future__ import annotations

from .capabilities import detect_platform
from .contract import PlatformInfo


def get_platform() -> PlatformInfo:
    info = detect_platform()
    if info.name != "macos":
        raise RuntimeError("macOS adapter used on non-macOS platform")
    return info
