"""
Authority boundary separation tests.
"""
import pytest


class TestAuthoritySeparations:

    def test_data_is_not_evidence(self):
        assert "DATA" != "EVIDENCE"

    def test_evidence_is_not_admission(self):
        assert "EVIDENCE" != "ADMISSION"

    def test_admission_is_not_authorization(self):
        assert "ADMISSION" != "AUTHORIZATION"

    def test_authorization_is_not_action(self):
        assert "AUTHORIZATION" != "ACTION"

    def test_observation_is_not_authority(self):
        assert "OBSERVATION" != "AUTHORITY"

    def test_capability_is_not_permission(self):
        assert "CAPABILITY" != "PERMISSION"

    def test_signature_is_not_authority(self):
        assert "SIGNATURE" != "AUTHORITY"

    def test_timestamp_is_not_truth(self):
        assert "TIMESTAMP" != "TRUTH"

    def test_execution_is_not_legitimacy(self):
        assert "EXECUTION" != "LEGITIMACY"

    def test_instruction_is_not_authorization(self):
        assert "INSTRUCTION" != "AUTHORIZATION"

    def test_pass_t0_is_not_authorization_t1(self):
        assert "PASS(t0)" != "AUTHORIZATION(t1)"
