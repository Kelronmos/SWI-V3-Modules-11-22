"""Execution gate.

EXECUTE(a) ⇔
  FLOW_BIND(a)
  ∧ RUNTIME_MATCH(a)
  ∧ HUMAN_AUTHORITY_BOUND(a)
  ∧ AUTHORIZATION_VALID(a)

and fail-closed must not block.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .fail_closed import FailClosedRuntime, Decision
from .degraded import DegradedPathRuntime


@dataclass
class GateResult:
    permitted: bool
    mode: str  # NORMAL | DEGRADED | BLOCKED | REVALIDATE | PAUSE
    decision: str
    reason_codes: list[str] = field(default_factory=list)
    degraded_mode_id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "permitted": self.permitted,
            "mode": self.mode,
            "decision": self.decision,
            "reason_codes": list(self.reason_codes),
            "degraded_mode_id": self.degraded_mode_id,
        }


class ExecutionGate:
    """Executable authority/execution boundary. Does not manufacture authority."""

    def __init__(self):
        self.fail_closed = FailClosedRuntime()
        self.degraded = DegradedPathRuntime()

    def evaluate(self, state: dict[str, Any]) -> GateResult:
        reasons: list[str] = []

        fc = self.fail_closed.evaluate(state)
        if fc == Decision.BLOCK:
            return GateResult(
                permitted=False,
                mode="BLOCKED",
                decision=fc.value,
                reason_codes=self._collect_block_reasons(state),
            )
        if fc == Decision.REVALIDATE:
            return GateResult(
                permitted=False,
                mode="REVALIDATE",
                decision=fc.value,
                reason_codes=self._collect_revalidate_reasons(state),
            )
        if fc == Decision.PAUSE:
            return GateResult(
                permitted=False,
                mode="PAUSE",
                decision=fc.value,
                reason_codes=["PAUSE_REQUIRED"],
            )

        if fc == Decision.EXECUTE_DEGRADED:
            return GateResult(
                permitted=True,
                mode="DEGRADED",
                decision=fc.value,
                reason_codes=["DEGRADED_PATH_AUTHORIZED_CONDITIONS_MET"],
                degraded_mode_id=state.get("degraded_mode_id"),
            )

        # Normal path: four conjuncts
        if not state.get("flow_bind"):
            reasons.append("FLOW_BIND_MISSING")
        if not state.get("runtime_match"):
            reasons.append("RUNTIME_MATCH_MISSING")
        if not state.get("human_authority_bound"):
            reasons.append("HUMAN_AUTHORITY_UNBOUND")
        if not state.get("authorization_valid"):
            reasons.append("AUTHORIZATION_INVALID")

        if reasons:
            return GateResult(
                permitted=False,
                mode="BLOCKED",
                decision=Decision.BLOCK.value,
                reason_codes=reasons,
            )

        return GateResult(
            permitted=True,
            mode="NORMAL",
            decision=Decision.CONTINUE.value,
            reason_codes=[],
        )

    def _collect_block_reasons(self, state: dict) -> list[str]:
        mapping = [
            ("critical_state_unknown", "CRITICAL_STATE_UNKNOWN"),
            ("integrity_failure", "INTEGRITY_FAILURE"),
            ("flow_binding_invalid", "FLOW_BINDING_INVALID"),
            ("human_authority_unbound", "HUMAN_AUTHORITY_UNBOUND"),
            ("authorization_invalid", "AUTHORIZATION_INVALID"),
            ("required_evidence_invalid", "REQUIRED_EVIDENCE_INVALID"),
            ("required_prerequisite_unsatisfied", "REQUIRED_PREREQUISITE_UNSATISFIED"),
            ("required_component_missing", "REQUIRED_COMPONENT_MISSING"),
        ]
        out = [code for key, code in mapping if state.get(key)]
        if state.get("required_component_missing") and not state.get("valid_degraded_path_defined"):
            out.append("NO_VALID_DEGRADED_PATH")
        return out or ["FAIL_CLOSED_BLOCK"]

    def _collect_revalidate_reasons(self, state: dict) -> list[str]:
        mapping = [
            ("required_evidence_stale", "REQUIRED_EVIDENCE_STALE"),
            ("material_change_without_revalidation", "MATERIAL_CHANGE"),
            ("runtime_mismatch", "RUNTIME_MISMATCH"),
        ]
        return [code for key, code in mapping if state.get(key)] or ["REVALIDATE_REQUIRED"]
