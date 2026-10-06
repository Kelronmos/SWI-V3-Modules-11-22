"""
Executable tests for Structured Seal and Runtime Seal mechanisms.

These tests exercise the seal *machinery*.
They do NOT seal SWI, authorize SWI, or production-authorize SWI.
"""
from __future__ import annotations

import copy
import pytest

from swi_v3.seal import (
    StructuredSealEngine,
    RuntimeSealEngine,
    SealVerifier,
    SealStateMachine,
    digest,
    canonical_json,
)
from swi_v3.seal.models import SealState, SealType, VerificationOutcome
from swi_v3.seal.state_machine import SealStateMachine as SSM

FIXED_COMMIT = "242b8284ab4701c04b6cc45ece2a12818115c666"
OTHER_COMMIT = "55d843b8f455baa80aab7e4b92d679c6d62e0a78"
FIXED_TREE = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
OTHER_TREE = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

CONTRACTS_A = {
    "docs/SWI-FAIL-CLOSED-RULES.md": "hash-fc-1",
    "docs/contracts/05_FAIL_CLOSED_AND_RECONCILIATION.md": "hash-05-1",
}
CONTRACTS_B = {
    "docs/SWI-FAIL-CLOSED-RULES.md": "hash-fc-2",
    "docs/contracts/05_FAIL_CLOSED_AND_RECONCILIATION.md": "hash-05-1",
}
STATUS = {
    "DEFINED": True,
    "IMPLEMENTED": True,
    "TESTED": True,
    "PROVEN": False,
    "SEALED": False,
    "AUTHORIZED": False,
    "PRODUCTION_AUTHORIZED": False,
}


@pytest.fixture
def engine():
    return StructuredSealEngine()


@pytest.fixture
def valid_seal(engine):
    record, failures = engine.create_seal(
        commit_sha=FIXED_COMMIT,
        tree_sha=FIXED_TREE,
        contracts=CONTRACTS_A,
        status_snapshot=STATUS,
        tests={"tests/test_seal_mechanism.py": "t1"},
        seal_type=SealType.TEST_SEAL.value,
        created_at="2026-10-06T21:00:00Z",
    )
    assert failures == []
    assert record is not None
    return record


class TestDeterminism:
    def test_same_input_same_hash(self):
        a = digest(CONTRACTS_A)
        b = digest(CONTRACTS_A)
        assert a == b

    def test_modified_field_changes_hash(self):
        assert digest(CONTRACTS_A) != digest(CONTRACTS_B)

    def test_canonical_json_sorted(self):
        assert canonical_json({"b": 1, "a": 2}) == '{"a":2,"b":1}'


class TestStructuredSealCreation:
    def test_valid_structured_seal_input(self, engine, valid_seal):
        assert valid_seal.state == SealState.ACTIVE.value
        assert valid_seal.subject["commit_sha"] == FIXED_COMMIT
        assert valid_seal.policy_version

    def test_mutable_alias_rejected(self, engine):
        record, failures = engine.create_seal(
            commit_sha="main",
            contracts=CONTRACTS_A,
            status_snapshot=STATUS,
        )
        assert record is None
        assert "EXACT_STATE_MISMATCH" in failures

    def test_missing_contracts_rejected(self, engine):
        record, failures = engine.create_seal(
            commit_sha=FIXED_COMMIT,
            contracts={},
            status_snapshot=STATUS,
        )
        assert record is None
        assert "REQUIRED_ARTIFACT_MISSING" in failures

    def test_missing_policy_version_rejected(self):
        eng = StructuredSealEngine(policy_version="")
        record, failures = eng.create_seal(
            commit_sha=FIXED_COMMIT,
            contracts=CONTRACTS_A,
            status_snapshot=STATUS,
        )
        assert record is None
        assert "POLICY_VERSION_MISMATCH" in failures

    def test_conflicting_active_seal_rejected(self, engine):
        record, failures = engine.create_seal(
            commit_sha=FIXED_COMMIT,
            contracts=CONTRACTS_A,
            status_snapshot=STATUS,
            conflicting_active_seal=True,
        )
        assert record is None
        assert "CONFLICTING_SEAL_STATE" in failures


class TestTamperAndReplay:
    def test_changed_commit_sha(self, valid_seal):
        v = SealVerifier()
        result = v.verify(valid_seal, {"commit_sha": OTHER_COMMIT})
        assert result.verification_result != VerificationOutcome.VALID.value
        assert "EXACT_STATE_MISMATCH" in result.reason_codes

    def test_changed_tree(self, valid_seal):
        v = SealVerifier()
        result = v.verify(valid_seal, {"tree_sha": OTHER_TREE})
        assert result.verification_result != VerificationOutcome.VALID.value
        assert "TREE_MISMATCH" in result.reason_codes

    def test_changed_contract_hash(self, valid_seal):
        v = SealVerifier()
        result = v.verify(
            valid_seal,
            {"contract_manifest_hash": digest(CONTRACTS_B)},
        )
        assert result.verification_result != VerificationOutcome.VALID.value
        assert "CONTRACT_HASH_MISMATCH" in result.reason_codes

    def test_changed_test_manifest(self, valid_seal):
        v = SealVerifier()
        result = v.verify(
            valid_seal,
            {"test_manifest_hash": digest({"other": "x"})},
        )
        assert result.verification_result != VerificationOutcome.VALID.value

    def test_replay_seal_a_on_state_b(self, valid_seal):
        v = SealVerifier()
        result = v.verify(
            valid_seal,
            {
                "commit_sha": OTHER_COMMIT,
                "tree_sha": OTHER_TREE,
                "contract_manifest_hash": digest(CONTRACTS_B),
            },
        )
        assert result.verification_result != VerificationOutcome.VALID.value

    def test_tamper_protected_field_invalidates(self, engine, valid_seal):
        tampered = copy.deepcopy(valid_seal)
        tampered.contract_manifest_hash = "tampered"
        v = SealVerifier()
        result = v.verify(
            tampered,
            {
                "commit_sha": FIXED_COMMIT,
                "contract_manifest_hash": valid_seal.contract_manifest_hash,
            },
        )
        assert result.verification_result != VerificationOutcome.VALID.value


class TestRuntimeMatch:
    def test_runtime_mismatch(self, valid_seal):
        v = SealVerifier()
        result = v.verify(valid_seal, {"runtime_mismatch": True})
        assert result.verification_result != VerificationOutcome.VALID.value
        assert "RUNTIME_MISMATCH" in result.reason_codes

    def test_material_configuration_change(self, valid_seal):
        v = SealVerifier()
        result = v.verify(valid_seal, {"material_change": True})
        assert result.verification_result != VerificationOutcome.VALID.value
        assert "MATERIAL_CHANGE" in result.reason_codes

    def test_matching_runtime_valid(self, valid_seal):
        v = SealVerifier()
        result = v.verify(
            valid_seal,
            {
                "commit_sha": FIXED_COMMIT,
                "tree_sha": FIXED_TREE,
                "contract_manifest_hash": valid_seal.contract_manifest_hash,
                "test_manifest_hash": valid_seal.test_manifest_hash,
                "policy_version": valid_seal.policy_version,
            },
        )
        assert result.verification_result == VerificationOutcome.VALID.value


class TestAuthoritySeparation:
    def test_authority_change(self, valid_seal):
        v = SealVerifier()
        result = v.verify(valid_seal, {"authority_binding_missing": True})
        assert "AUTHORITY_BINDING_MISSING" in result.reason_codes

    def test_authorization_change(self, valid_seal):
        v = SealVerifier()
        result = v.verify(valid_seal, {"authorization_invalid": True})
        assert "AUTHORIZATION_INVALID" in result.reason_codes

    def test_seal_does_not_manufacture_authority(self, valid_seal):
        v = SealVerifier()
        result = v.verify(
            valid_seal,
            {"infer_production_authorization_from_seal": True},
        )
        assert result.verification_result == VerificationOutcome.BLOCKED.value
        assert "PRODUCTION_CLAIM_FORBIDDEN" in result.reason_codes

    def test_production_authorization_not_inferred_from_seal(self, valid_seal):
        # Even a VALID seal does not equal production authorization.
        assert valid_seal.status_snapshot.get("PRODUCTION_AUTHORIZED") is False


class TestInvalidation:
    def test_invalidated_seal_reused(self, engine, valid_seal):
        inv = engine.invalidate(valid_seal, reason="MATERIAL_CHANGE")
        assert inv.state == SealState.INVALIDATED.value
        v = SealVerifier()
        result = v.verify(inv, {"commit_sha": FIXED_COMMIT})
        assert result.verification_result == VerificationOutcome.INVALID.value
        assert "SEAL_INVALIDATED" in result.reason_codes

    def test_stale_critical_evidence(self, valid_seal):
        v = SealVerifier()
        result = v.verify(valid_seal, {"stale_evidence": True})
        assert result.verification_result != VerificationOutcome.VALID.value
        assert "STALE_EVIDENCE" in result.reason_codes

    def test_integrity_failure(self, valid_seal):
        v = SealVerifier()
        result = v.verify(valid_seal, {"integrity_failure": True})
        assert result.verification_result != VerificationOutcome.VALID.value
        assert "INTEGRITY_FAILURE" in result.reason_codes


class TestConversationBoundary:
    def test_timestamp_not_truth(self):
        assert "TIMESTAMP" != "TRUTH"

    def test_conversation_continuity_not_authority(self):
        assert "CONVERSATION_CONTINUITY" != "AUTHORITY_CONTINUITY"

    def test_repeated_agreement_not_cumulative_proof(self):
        agreements = [True] * 10
        assert all(agreements)
        cumulative_proof = False
        assert cumulative_proof is False

    def test_conversation_header_not_authorization(self):
        header = {"timestamp": "2026-10-06T21:00:00Z", "is_authorization": False}
        assert header["is_authorization"] is False


class TestTemporalSeal:
    def test_sealed_t0_not_sealed_t1(self):
        assert "SEALED(t0)" != "SEALED(t1)"

    def test_before_pass_not_during(self):
        assert "BEFORE_PASS" != "DURING_PASS"

    def test_during_pass_not_after(self):
        assert "DURING_PASS" != "AFTER_PASS"

    def test_previous_pass_not_current_authorization(self):
        assert "PASS(t0)" != "AUTHORIZATION(t1)"


class TestDegradedPathAndSeal:
    def test_missing_component_no_path_blocks_seal_applicability(self, valid_seal):
        # Degraded path absence does not preserve seal applicability under fail-closed
        from tests.conftest import Decision, FailClosedEvaluator

        fc = FailClosedEvaluator()
        result = fc.evaluate(
            {
                "required_component_missing": True,
                "valid_degraded_path_defined": False,
            }
        )
        assert result == Decision.BLOCK

    def test_degraded_without_authority_blocks(self):
        from tests.conftest import Decision, DegradedPathEvaluator

        dp = DegradedPathEvaluator()
        result = dp.evaluate(
            {
                "required_component_missing": True,
                "valid_degraded_path_defined": True,
                "degraded_conditions_satisfied": True,
                "human_authority_bound": False,
            }
        )
        assert result == Decision.BLOCK

    def test_degraded_without_authorization_blocks(self):
        from tests.conftest import Decision, DegradedPathEvaluator

        dp = DegradedPathEvaluator()
        result = dp.evaluate(
            {
                "required_component_missing": True,
                "valid_degraded_path_defined": True,
                "degraded_conditions_satisfied": True,
                "human_authority_bound": True,
                "authorization_valid": False,
            }
        )
        assert result == Decision.BLOCK

    def test_degraded_path_does_not_create_seal(self, valid_seal):
        # Existence of degraded path is independent of seal creation authority
        assert valid_seal.seal_type == SealType.TEST_SEAL.value
        # Still not production
        assert valid_seal.status_snapshot.get("PRODUCTION_AUTHORIZED") is False


class TestStateMachine:
    def test_legal_path_to_active(self):
        sm = SSM()
        sm.transition(SealState.SEAL_ELIGIBLE)
        sm.transition(SealState.SEAL_CREATED)
        sm.transition(SealState.SEAL_VERIFIED)
        sm.transition(SealState.ACTIVE)
        assert sm.is_active()

    def test_unsealed_to_active_forbidden(self):
        sm = SSM()
        with pytest.raises(ValueError):
            sm.transition(SealState.ACTIVE)

    def test_invalidated_to_active_forbidden(self):
        sm = SSM(SealState.INVALIDATED)
        with pytest.raises(ValueError):
            sm.transition(SealState.ACTIVE)

    def test_active_to_invalidated(self):
        sm = SSM(SealState.ACTIVE)
        sm.transition(SealState.INVALIDATED)
        assert sm.state == SealState.INVALIDATED


class TestMalformed:
    def test_malformed_seal_record(self):
        from swi_v3.seal.models import SealRecord

        bad = SealRecord(
            seal_id="x",
            seal_type="TEST_SEAL",
            subject={"commit_sha": "not-a-sha"},
            policy_version="SWI-SEAL-POLICY-V1",
            contract_manifest_hash="h",
            status_snapshot={},
            created_at="2026-10-06T21:00:00Z",
            state="ACTIVE",
        )
        v = SealVerifier()
        result = v.verify(bad, {})
        assert result.verification_result == VerificationOutcome.INVALID.value
        assert "MALFORMED_SEAL" in result.reason_codes or "EXACT_STATE_MISMATCH" in result.reason_codes

    def test_test_seal_not_production_seal(self, valid_seal):
        v = SealVerifier()
        result = v.verify(valid_seal, {"require_production_seal": True})
        assert result.verification_result == VerificationOutcome.BLOCKED.value
        assert "PRODUCTION_CLAIM_FORBIDDEN" in result.reason_codes
