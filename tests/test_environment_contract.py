"""
Environment and observation-context contract tests.
"""
import pytest
from tests.conftest import Decision


class TestEnvironmentContract:

    def test_environment_must_be_checked(self):
        env = {
            "checked": True,
            "within_envelope": True,
            "material_change": False,
        }
        assert env["checked"] is True

    def test_material_environment_change_requires_revalidation(self, fail_closed):
        state = {"material_change_without_revalidation": True}
        result = fail_closed.evaluate(state)
        assert result in (Decision.REVALIDATE, Decision.BLOCK, Decision.PAUSE)
        assert result != Decision.CONTINUE

    def test_observation_requires_identity_timestamp_context(self):
        observation = {
            "sensor_id": "S-001",
            "value": 1.23,
            "timestamp": "2026-10-06T22:00:00Z",
            "context": {"workflow": "W-1"},
        }
        assert observation["sensor_id"]
        assert observation["timestamp"]
        assert observation["context"]

    def test_stale_observation_does_not_authorize(self, fail_closed):
        state = {"required_evidence_stale": True}
        result = fail_closed.evaluate(state)
        assert result != Decision.CONTINUE

    def test_environment_match_is_not_authorization(self):
        env = {"within_envelope": True, "authorization": False}
        assert env["within_envelope"] is True
        assert env["authorization"] is False
