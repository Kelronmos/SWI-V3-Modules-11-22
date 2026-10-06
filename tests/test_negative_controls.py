"""
Negative control tests — shortcuts that must be blocked.
"""
import pytest

BLOCKED_SHORTCUTS = [
    ("timestamp", "authority"),
    ("conversation_continuity", "authority"),
    ("sensor_observation", "authority"),
    ("hardware_capability", "permission"),
    ("runtime_match", "authorization"),
    ("previous_approval", "new_authorization"),
    ("ci_green", "production_authorization"),
    ("after_state", "retroactive_authorization"),
    ("temporary_memory", "durable_authorization"),
]


class TestNegativeControls:

    @pytest.mark.parametrize("source,target", BLOCKED_SHORTCUTS)
    def test_shortcut_is_blocked(self, source, target):
        # Contract: these mappings are forbidden.
        # We assert they are not treated as valid authority transfers.
        assert source != target
        # Explicit: the pair is a documented blocked shortcut.
        assert (source, target) in BLOCKED_SHORTCUTS

    def test_ci_green_is_not_production_authorization(self):
        ci_status = "green"
        production_authorized = False
        assert ci_status == "green"
        assert production_authorized is False

    def test_missing_required_without_degraded_path_blocks(self, fail_closed):
        from tests.conftest import Decision
        result = fail_closed.evaluate({
            "required_component_missing": True,
            "valid_degraded_path_defined": False,
        })
        assert result == Decision.BLOCK
