"""Android/Termux adapter — observation only; not identical to Linux."""
from __future__ import annotations

import os

from .contract import PlatformInfo


def get_platform() -> PlatformInfo:
    is_android = "ANDROID_ROOT" in os.environ or "ANDROID_DATA" in os.environ
    if not is_android:
        raise RuntimeError("Android environment not detected")
    return PlatformInfo(
        name="android",
        version=os.environ.get("ANDROID_VERSION", "unknown"),
        architecture="unknown",
        capabilities=frozenset(),
    )
