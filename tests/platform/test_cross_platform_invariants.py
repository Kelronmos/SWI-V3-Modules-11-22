"""Same governance model across platforms — platform is not authority."""
from swi_v3.platform.contract import PlatformInfo


def test_platform_identity_is_not_authority():
    platforms = [
        PlatformInfo("linux", "test", "x86_64", frozenset()),
        PlatformInfo("macos", "test", "arm64", frozenset()),
        PlatformInfo("android", "test", "arm64", frozenset()),
        PlatformInfo("ios", "test", "arm64", frozenset()),
    ]
    for platform in platforms:
        assert not hasattr(platform, "authority")
        assert not hasattr(platform, "authorization")
        assert not hasattr(platform, "authorized_actions")
        assert not hasattr(platform, "permit")


def test_capability_set_does_not_imply_permission():
    info = PlatformInfo(
        "linux", "test", "x86_64", frozenset({"filesystem", "network", "gpu"})
    )
    # Capabilities may be declared; they never become permissions on the object.
    for cap in info.capabilities:
        assert info.has_capability(cap)
    assert not hasattr(info, "permissions")
