"""Runtime Seal engine — compares sealed specification to observed runtime."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from .models import SealRecord, SealState, VerificationOutcome, VerificationResult
from .canonical import digest


class RuntimeSealEngine:
    """Verify observed runtime against a structured seal.

    Does not auto-repair mismatches. Does not create authority.
    """

    def compare(
        self,
        seal: SealRecord,
        observed: dict[str, Any],
        verification_time: Optional[str] = None,
    ) -> VerificationResult:
        if verification_time is None:
            verification_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        reasons: list[str] = []
        material_change = False
        runtime_match: Optional[bool] = None

        if seal.state != SealState.ACTIVE.value:
            reasons.append("SEAL_INVALIDATED")
            return VerificationResult(
                seal_id=seal.seal_id,
                subject_commit=seal.subject.get("commit_sha", ""),
                subject_tree=seal.subject.get("tree_sha"),
                policy_version=seal.policy_version,
                verification_time=verification_time,
                verification_result=VerificationOutcome.INVALID.value,
                reason_codes=reasons,
                material_change_detected=True,
                runtime_match=False,
                integrity_status="FAILED",
            )

        # Exact commit identity
        obs_commit = observed.get("commit_sha")
        if obs_commit and obs_commit != seal.subject.get("commit_sha"):
            reasons.append("EXACT_STATE_MISMATCH")
            material_change = True

        obs_tree = observed.get("tree_sha")
        if obs_tree and seal.subject.get("tree_sha") and obs_tree != seal.subject.get("tree_sha"):
            reasons.append("TREE_MISMATCH")
            material_change = True

        # Contract hash
        obs_contract_hash = observed.get("contract_manifest_hash")
        if obs_contract_hash and obs_contract_hash != seal.contract_manifest_hash:
            reasons.append("CONTRACT_HASH_MISMATCH")
            material_change = True

        # Test manifest
        obs_test_hash = observed.get("test_manifest_hash")
        if (
            seal.test_manifest_hash
            and obs_test_hash
            and obs_test_hash != seal.test_manifest_hash
        ):
            reasons.append("TEST_MANIFEST_MISMATCH")
            material_change = True

        # Policy version
        if observed.get("policy_version") and observed["policy_version"] != seal.policy_version:
            reasons.append("POLICY_VERSION_MISMATCH")
            material_change = True

        # Runtime identity
        if observed.get("runtime_mismatch") is True:
            reasons.append("RUNTIME_MISMATCH")
            material_change = True
            runtime_match = False
        elif observed.get("runtime_identity") is not None:
            sealed_rt = seal.status_snapshot.get("runtime_identity")
            if sealed_rt is not None and observed["runtime_identity"] != sealed_rt:
                reasons.append("RUNTIME_MISMATCH")
                material_change = True
                runtime_match = False
            else:
                runtime_match = True

        # Material configuration / authority / authorization
        if observed.get("material_change") is True:
            reasons.append("MATERIAL_CHANGE")
            material_change = True

        if observed.get("authority_binding_missing") is True:
            reasons.append("AUTHORITY_BINDING_MISSING")

        if observed.get("authorization_invalid") is True:
            reasons.append("AUTHORIZATION_INVALID")

        if observed.get("stale_evidence") is True:
            reasons.append("STALE_EVIDENCE")
            material_change = True

        if observed.get("integrity_failure") is True:
            reasons.append("INTEGRITY_FAILURE")
            material_change = True

        authority_status = "BOUND" if not observed.get("authority_binding_missing") else "UNBOUND"
        authz_status = "INVALID" if observed.get("authorization_invalid") else "OK"

        if reasons:
            outcome = (
                VerificationOutcome.REVALIDATION_REQUIRED.value
                if any(
                    r in reasons
                    for r in ("MATERIAL_CHANGE", "STALE_EVIDENCE", "RUNTIME_MISMATCH")
                )
                and not any(
                    r in reasons
                    for r in ("INTEGRITY_FAILURE", "AUTHORIZATION_INVALID")
                )
                else VerificationOutcome.INVALID.value
            )
            if "INTEGRITY_FAILURE" in reasons or "AUTHORIZATION_INVALID" in reasons:
                outcome = VerificationOutcome.BLOCKED.value if "INTEGRITY_FAILURE" in reasons else VerificationOutcome.INVALID.value
            return VerificationResult(
                seal_id=seal.seal_id,
                subject_commit=seal.subject.get("commit_sha", ""),
                subject_tree=seal.subject.get("tree_sha"),
                policy_version=seal.policy_version,
                verification_time=verification_time,
                verification_result=outcome,
                reason_codes=reasons,
                material_change_detected=material_change,
                runtime_match=runtime_match if runtime_match is not None else False,
                authority_binding_status=authority_status,
                authorization_status=authz_status,
                integrity_status="FAILED" if "INTEGRITY_FAILURE" in reasons else "OK",
            )

        return VerificationResult(
            seal_id=seal.seal_id,
            subject_commit=seal.subject.get("commit_sha", ""),
            subject_tree=seal.subject.get("tree_sha"),
            policy_version=seal.policy_version,
            verification_time=verification_time,
            verification_result=VerificationOutcome.VALID.value,
            reason_codes=[],
            material_change_detected=False,
            runtime_match=True,
            authority_binding_status=authority_status,
            authorization_status=authz_status,
            integrity_status="OK",
        )
