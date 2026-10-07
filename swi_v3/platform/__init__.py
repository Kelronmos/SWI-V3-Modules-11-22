"""SWI V3 platform adapters — capability observation only.

CAPABILITY ≠ PERMISSION ≠ AUTHORITY ≠ AUTHORIZATION ≠ EXECUTION
"""
from .contract import PlatformInfo
from .capabilities import detect_platform

__all__ = ["PlatformInfo", "detect_platform"]
