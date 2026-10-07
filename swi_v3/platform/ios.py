"""iOS adapter scaffold — adapter exists ≠ iOS runtime exists."""
from __future__ import annotations

from .contract import PlatformInfo


def get_platform() -> PlatformInfo:
    return PlatformInfo(
        name="ios",
        version="unknown",
        architecture="unknown",
        capabilities=frozenset(),
    )
