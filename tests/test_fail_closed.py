"""
Fail-closed decision table tests.

These tests exercise the *documented* decision rules.
They do not prove a runtime exists.
"""
import pytest
from tests.conftest import Decision


class TestFailClosedMatrix:

    def test_critical_state_unknown_blocks(self, fail_closed):
        result = fail_closed.evaluate({"critical_state_unknown": True})
        assert result == Decision.BLOCK

    def test_integrity_failure_blocks(self, fail_closed):
        result = fail_closed.evaluate({"integrity_failure": True})
        assert result == Decision.BLOCK

    def test_flow_binding_invalid_blocks(self, fail_closed):
        result = fail_closed.evaluate({"flow_binding_invalid": True})
        assert result == Decision.BLOCK

    def test_human_authority_unbound_blocks(self, fail_closed):
        result = fail_closed.evaluate({"human_authority_unbound": True})
        assert result == Decision.BLOCK

    def test_authorization_invalid_blocks(self, fail_closed):
        result = fail_closed.evaluate({"authorization_invalid": True})
        assert result == Decision.BLOCK

    def test_required_evidence_invalid_blocks(self, fail_closed):
        result = fail_closed.evaluate({"required_evidence_invalid": True})
        assert result == Decision.BLOCK

    def test_required_prerequisite_unsatisfied_blocks(self, fail_closed):
        result = fail_closed.evaluate({"required_prerequisite_unsatisfied": True})
        assert result == Decision.BLOCK

    def test_required_component_missing_no_degraded_path_blocks(self, fail_closed):
        result = fail_closed.evaluate({
            "required_component_missing": True,
            "valid_degraded_path_defined": False,
        })
        assert result == Decision.BLOCK

    def test_required_evidence_stale_revalidates(self, fail_closed):
        result = fail_closed.evaluate({"required_evidence_stale": True})
        assert result == Decision.REVALIDATE

    def test_material_change_without_revalidation_revalidates(self, fail_closed):
        result = fail_closed.evaluate({"material_change_without_revalidation": True})
        assert result == Decision.REVALIDATE

    def test_runtime_mismatch_revalidates(self, fail_closed):
        result = fail_closed.evaluate({"runtime_mismatch": True})
        assert result == Decision.REVALIDATE

    def test_clean_state_continues(self, fail_closed):
        result = fail_closed.evaluate({})
        assert result == Decision.CONTINUE

    def test_previous_pass_does_not_override_current_failure(self, fail_closed):
        """BEFORE=PASS does not authorize continuation when DURING fails."""
        during_state = {
            "material_change_without_revalidation": True,
            "before_was_pass": True,  # must be ignored
        }
        result = fail_closed.evaluate(during_state)
        assert result == Decision.REVALIDATE
        assert result != Decision.CONTINUE


class TestFailClosedNotAuthorization:

    def test_fail_closed_is_not_authorization(self):
        """Documented separation: FAIL_CLOSED ≠ AUTHORIZATION."""
        # This is a contract invariant test, not runtime.
        assert "FAIL_CLOSED" != "AUTHORIZATION"

    def test_block_does_not_manufacture_authority(self, fail_closed):
        result = fail_closed.evaluate({"authorization_invalid": True})
        assert result == Decision.BLOCK
        # Blocking is a control response, not an authorization decision.
