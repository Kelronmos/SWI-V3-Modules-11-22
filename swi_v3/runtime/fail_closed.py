"""Canonical fail-closed runtime evaluator.

Source doctrine: docs/SWI-FAIL-CLOSED-RULES.md
"""
from __future__ import annotations

from enum import Enum
from typing import Any


class Decision(str, Enum):
    BLOCK = "BLOCK"
    PAUSE = "PAUSE"
    REVALIDATE = "REVALIDATE"
    CONTINUE = "CONTINUE"
    EXECUTE_DEGRADED = "EXECUTE_DEGRADED"


class FailClosedRuntime:
    """Evaluate critical preconditions. Never silently continues on failure."""

    def evaluate(self, state: dict[str, Any]) -> Decision:
        if state.get("critical_state_unknown"):
            return Decision.BLOCK
        if state.get("integrity_failure"):
            return Decision.BLOCK
        if state.get("flow_binding_invalid"):
            return Decision.BLOCK
        if state.get("human_authority_unbound"):
            return Decision.BLOCK
        if state.get("authorization_invalid"):
            return Decision.BLOCK
        if state.get("required_evidence_invalid"):
            return Decision.BLOCK
        if state.get("required_prerequisite_unsatisfied"):
            return Decision.BLOCK

        if state.get("required_component_missing"):
            if not state.get("valid_degraded_path_defined"):
                return Decision.BLOCK
            if not state.get("degraded_conditions_satisfied"):
                return Decision.BLOCK
            if not state.get("human_authority_bound"):
                return Decision.BLOCK
            if not state.get("authorization_valid"):
                return Decision.BLOCK
            return Decision.EXECUTE_DEGRADED

        if state.get("required_evidence_stale"):
            return Decision.REVALIDATE
        if state.get("material_change_without_revalidation"):
            return Decision.REVALIDATE
        if state.get("runtime_mismatch"):
            return Decision.REVALIDATE

        return Decision.CONTINUE
