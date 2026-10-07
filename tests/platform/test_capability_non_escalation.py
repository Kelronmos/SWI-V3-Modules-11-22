"""CAPABILITY ≠ PERMISSION ≠ AUTHORITY ≠ AUTHORIZATION."""
from swi_v3.platform.contract import PlatformInfo


def test_capability_does_not_authorize():
    info = PlatformInfo(
        name="linux",
        version="test",
        architecture="x86_64",
        capabilities=frozenset({"filesystem"}),
    )
    assert info.has_capability("filesystem")
    assert not hasattr(info, "authorized_actions")
    assert not hasattr(info, "authority")
    assert not hasattr(info, "authorization")
    assert not hasattr(info, "permit")


def test_platform_info_has_no_execution_hook():
    info = PlatformInfo("android", "test", "arm64", frozenset({"termux"}))
    assert not hasattr(info, "execute")
    assert not hasattr(info, "allow")
