"""Platform contract basic tests."""
from swi_v3.platform.contract import PlatformInfo
from swi_v3.platform.capabilities import detect_platform


def test_platform_info_is_frozen():
    info = PlatformInfo("linux", "test", "x86_64", frozenset())
    assert info.name == "linux"


def test_detect_platform_returns_platform_info():
    info = detect_platform()
    assert isinstance(info, PlatformInfo)
    assert info.name
    assert isinstance(info.capabilities, frozenset)


def test_has_capability():
    info = PlatformInfo("linux", "test", "x86_64", frozenset({"filesystem"}))
    assert info.has_capability("filesystem") is True
    assert info.has_capability("network") is False
