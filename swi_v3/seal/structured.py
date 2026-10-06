"""Structured Seal engine — binds an immutable verification record to exact state."""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from .canonical import digest
from .models import SealRecord, SealState, SealType

POLICY_VERSION = "SWI-SEAL-POLICY-V1"

COMMIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
MUTABLE_ALIASES = {"latest", "current", "main", "head", "HEAD", "master"}


class StructuredSealEngine:
    """Create and evaluate structured seal eligibility.

    Does NOT create authority or production authorization.
    """

    def __init__(self, policy_version: str = POLICY_VERSION):
        self.policy_version = policy_version

    def build_contract_manifest_hash(self, contracts: dict[str, str]) -> str:
        """contracts: ordered mapping of path -> content hash or content."""
        return digest(contracts)

    def build_test_manifest_hash(self, tests: Optional[dict[str, str]]) -> Optional[str]:
        if tests is None:
            return None
        return digest(tests)

    def validate_preconditions(
        self,
        commit_sha: str,
        contracts: dict[str, str],
        status_snapshot: dict,
        tree_sha: Optional[str] = None,
        conflicting_active_seal: bool = False,
        policy_version: Optional[str] = None,
    ) -> list[str]:
        """Return list of failed reason codes. Empty = eligible."""
        failures: list[str] = []

        if not commit_sha or commit_sha in MUTABLE_ALIASES:
            failures.append("EXACT_STATE_MISMATCH")
        elif not COMMIT_SHA_RE.match(commit_sha):
            failures.append("EXACT_STATE_MISMATCH")

        if not contracts:
            failures.append("REQUIRED_ARTIFACT_MISSING")
            failures.append("CONTRACT_SET_IDENTIFIED_FAILED")

        if status_snapshot is None:
            failures.append("STATUS_SNAPSHOT_MISSING")

        pv = policy_version or self.policy_version
        if not pv:
            failures.append("POLICY_VERSION_MISMATCH")

        if conflicting_active_seal:
            failures.append("CONFLICTING_SEAL_STATE")

        # Prohibited claims in status snapshot
        prohibited = ["PRODUCTION_AUTHORIZED", "AUTHORIZED", "SEALED"]
        for key in prohibited:
            if status_snapshot and status_snapshot.get(key) is True:
                # Recording the claim is allowed; claiming it as established evidence here is not
                # We only flag if someone tries to pass SEALED=True as a precondition success
                if key == "SEALED" and status_snapshot.get("SEALED") is True:
                    failures.append("PROHIBITED_STATUS_CLAIM")

        return failures

    def create_seal(
        self,
        commit_sha: str,
        contracts: dict[str, str],
        status_snapshot: dict,
        tree_sha: Optional[str] = None,
        subject_id: str = "SWI-V3",
        subject_version: str = "V3-0006",
        tests: Optional[dict[str, str]] = None,
        seal_type: str = SealType.TEST_SEAL.value,
        conflicting_active_seal: bool = False,
        created_at: Optional[str] = None,
    ) -> tuple[Optional[SealRecord], list[str]]:
        """Attempt seal creation. Returns (record|None, failure_codes)."""
        failures = self.validate_preconditions(
            commit_sha=commit_sha,
            contracts=contracts,
            status_snapshot=status_snapshot,
            tree_sha=tree_sha,
            conflicting_active_seal=conflicting_active_seal,
        )
        if failures:
            return None, failures

        if created_at is None:
            created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        record = SealRecord(
            seal_id=str(uuid.uuid4()),
            seal_type=seal_type,
            subject={
                "commit_sha": commit_sha,
                "tree_sha": tree_sha,
                "subject_id": subject_id,
                "subject_version": subject_version,
            },
            policy_version=self.policy_version,
            contract_manifest_hash=self.build_contract_manifest_hash(contracts),
            test_manifest_hash=self.build_test_manifest_hash(tests),
            status_snapshot=status_snapshot,
            created_at=created_at,
            state=SealState.ACTIVE.value,
        )
        return record, []

    def invalidate(
        self,
        record: SealRecord,
        reason: str,
        invalidated_at: Optional[str] = None,
    ) -> SealRecord:
        if invalidated_at is None:
            invalidated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        record.state = SealState.INVALIDATED.value
        record.invalidated_at = invalidated_at
        record.invalidation_reason = reason
        return record
