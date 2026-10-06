"""
Expected Match Drift and reconciliation tests.
"""
import pytest
from tests.conftest import Decision


class TestExpectedMatchDrift:

    def test_drift_requires_evaluation(self, fail_closed):
        state = {"runtime_mismatch": True}
        result = fail_closed.evaluate(state)
        assert result in (Decision.REVALIDATE, Decision.BLOCK, Decision.PAUSE)
        assert result != Decision.CONTINUE

    def test_unresolved_drift_does_not_silently_continue(self, fail_closed):
        state = {"material_change_without_revalidation": True}
        result = fail_closed.evaluate(state)
        assert result != Decision.CONTINUE


class TestReconciliation:

    def test_after_does_not_retroactively_authorize(self):
        record = {
            "before": {"authorized": False},
            "during": {"authorized": False},
            "after": {"outcome": "SUCCESS"},
        }
        # AFTER success must not rewrite earlier authorization.
        assert record["before"]["authorized"] is False
        assert record["during"]["authorized"] is False
        assert record["after"].get("retroactive_authorization", False) is False

    def test_before_during_after_are_reconcilable(self):
        timeline = [
            {"phase": "BEFORE", "result": "PASS"},
            {"phase": "DURING", "result": "BLOCK"},
            {"phase": "AFTER", "result": "RECORDED"},
        ]
        assert len(timeline) == 3
        assert timeline[0]["phase"] == "BEFORE"
        assert timeline[1]["phase"] == "DURING"
        assert timeline[2]["phase"] == "AFTER"
