"""Seal record models and verification result types."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Optional


class SealType(str, Enum):
    STRUCTURED = "STRUCTURED"
    RUNTIME = "RUNTIME"
    TEST_SEAL = "TEST_SEAL"


class SealState(str, Enum):
    UNSEALED = "UNSEALED"
    SEAL_ELIGIBLE = "SEAL_ELIGIBLE"
    SEAL_CREATED = "SEAL_CREATED"
    SEAL_VERIFIED = "SEAL_VERIFIED"
    ACTIVE = "ACTIVE"
    INVALIDATED = "INVALIDATED"
    REVALIDATION_REQUIRED = "REVALIDATION_REQUIRED"
    FAILED = "FAILED"


class VerificationOutcome(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    REVALIDATION_REQUIRED = "REVALIDATION_REQUIRED"
    BLOCKED = "BLOCKED"


@dataclass
class SealRecord:
    seal_id: str
    seal_type: str
    subject: dict
    policy_version: str
    contract_manifest_hash: str
    status_snapshot: dict
    created_at: str
    state: str
    test_manifest_hash: Optional[str] = None
    invalidated_at: Optional[str] = None
    invalidation_reason: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SealRecord":
        return cls(
            seal_id=data["seal_id"],
            seal_type=data["seal_type"],
            subject=data["subject"],
            policy_version=data["policy_version"],
            contract_manifest_hash=data["contract_manifest_hash"],
            status_snapshot=data.get("status_snapshot", {}),
            created_at=data["created_at"],
            state=data["state"],
            test_manifest_hash=data.get("test_manifest_hash"),
            invalidated_at=data.get("invalidated_at"),
            invalidation_reason=data.get("invalidation_reason"),
        )


@dataclass
class VerificationResult:
    seal_id: str
    subject_commit: str
    subject_tree: Optional[str]
    policy_version: str
    verification_time: str
    verification_result: str
    reason_codes: list[str] = field(default_factory=list)
    material_change_detected: bool = False
    runtime_match: Optional[bool] = None
    authority_binding_status: Optional[str] = None
    authorization_status: Optional[str] = None
    integrity_status: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)
