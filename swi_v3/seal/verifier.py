"""Unified seal verifier."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from .models import SealRecord, SealState, SealType, VerificationOutcome, VerificationResult
from .runtime import RuntimeSealEngine
from .structured import StructuredSealEngine, COMMIT_SHA_RE


class SealVerifier:
    """VERIFY_SEAL(seal, current_state) → structured result."""

    def __init__(self):
        self.structured = StructuredSealEngine()
        self.runtime = RuntimeSealEngine()

    def verify(
        self,
        seal: SealRecord,
        current_state: dict[str, Any],
        verification_time: Optional[str] = None,
    ) -> VerificationResult:
        if verification_time is None:
            verification_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Malformed / missing policy
        if not seal.policy_version:
            return VerificationResult(
                seal_id=getattr(seal, "seal_id", "unknown"),
                subject_commit=seal.subject.get("commit_sha", "") if seal.subject else "",
                subject_tree=None,
                policy_version="",
                verification_time=verification_time,
                verification_result=VerificationOutcome.INVALID.value,
                reason_codes=["POLICY_VERSION_MISMATCH", "MALFORMED_SEAL"],
                integrity_status="FAILED",
            )

        commit = (seal.subject or {}).get("commit_sha", "")
        if not commit or not COMMIT_SHA_RE.match(commit):
            return VerificationResult(
                seal_id=seal.seal_id,
                subject_commit=commit,
                subject_tree=None,
                policy_version=seal.policy_version,
                verification_time=verification_time,
                verification_result=VerificationOutcome.INVALID.value,
                reason_codes=["EXACT_STATE_MISMATCH", "MALFORMED_SEAL"],
                integrity_status="FAILED",
            )

        # TEST_SEAL must never be treated as production
        if current_state.get("require_production_seal") and seal.seal_type == SealType.TEST_SEAL.value:
            return VerificationResult(
                seal_id=seal.seal_id,
                subject_commit=commit,
                subject_tree=seal.subject.get("tree_sha"),
                policy_version=seal.policy_version,
                verification_time=verification_time,
                verification_result=VerificationOutcome.BLOCKED.value,
                reason_codes=["PRODUCTION_CLAIM_FORBIDDEN"],
                integrity_status="FAILED",
            )

        # Seal must never manufacture production authorization
        if current_state.get("infer_production_authorization_from_seal"):
            return VerificationResult(
                seal_id=seal.seal_id,
                subject_commit=commit,
                subject_tree=seal.subject.get("tree_sha"),
                policy_version=seal.policy_version,
                verification_time=verification_time,
                verification_result=VerificationOutcome.BLOCKED.value,
                reason_codes=["PRODUCTION_CLAIM_FORBIDDEN"],
                authority_binding_status="NOT_CREATED_BY_SEAL",
                authorization_status="NOT_CREATED_BY_SEAL",
                integrity_status="OK",
            )

        if seal.state == SealState.INVALIDATED.value:
            return VerificationResult(
                seal_id=seal.seal_id,
                subject_commit=commit,
                subject_tree=seal.subject.get("tree_sha"),
                policy_version=seal.policy_version,
                verification_time=verification_time,
                verification_result=VerificationOutcome.INVALID.value,
                reason_codes=["SEAL_INVALIDATED"],
                material_change_detected=True,
                integrity_status="FAILED",
            )

        return self.runtime.compare(seal, current_state, verification_time=verification_time)
