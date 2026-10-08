"""Deterministic hardware-bind test records and replay.

REPLAY PASS ≠ AUTHORIZATION
SOURCE = TEST_FIXTURE for synthetic data
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any, Optional


@dataclass
class HardwareTestRecord:
    test_id: str
    workflow_id: str
    operation_id: str
    device_class: str
    component_set: list[str]
    sensor_set: list[str]
    expected_spec: dict[str, Any]
    observations: dict[str, Any]
    before: Optional[dict[str, Any]] = None
    during: Optional[dict[str, Any]] = None
    after: Optional[dict[str, Any]] = None
    drift: Optional[dict[str, Any]] = None
    violations: list[str] = field(default_factory=list)
    hardware_green: bool = False
    authorization: bool = False
    decision: str = "UNKNOWN"
    source: str = "TEST_FIXTURE"

    def canonical(self) -> str:
        payload = asdict(self)
        # Force authorization false in canonical form for integrity of non-escalation
        payload["authorization"] = False
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

    def digest(self) -> str:
        return hashlib.sha256(self.canonical().encode("utf-8")).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["authorization"] = False
        d["record_sha256"] = self.digest()
        return d


def replay_digest(record: HardwareTestRecord) -> str:
    return record.digest()


def replay_twice(record: HardwareTestRecord) -> tuple[str, str, bool]:
    a = replay_digest(record)
    b = replay_digest(record)
    return a, b, a == b
