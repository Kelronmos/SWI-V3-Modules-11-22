"""
SWI V3 test fixtures.

IMPORTANT:
- These fixtures model decision tables and invariants only.
- They do NOT implement SWI runtime.
- A passing test here means the *defined behavior* was exercised.
- It does NOT mean the system is proven, sealed, authorized, or production-ready.
"""
import pytest


class Decision:
    BLOCK = "BLOCK"
    PAUSE = "PAUSE"
    REVALIDATE = "REVALIDATE"
    CONTINUE = "CONTINUE"
    EXECUTE_DEGRADED = "EXECUTE_DEGRADED"


class FailClosedEvaluator:
    """Pure decision table for the canonical fail-closed rule.

    This is a test harness model of the documented contract.
    It is NOT the SWI runtime.
    """

    def evaluate(self, state: dict) -> str:
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


class DegradedPathEvaluator:
    """Pure decision table for degraded-path control."""

    def evaluate(self, state: dict) -> str:
        if not state.get("required_component_missing"):
            return Decision.CONTINUE

        if not state.get("valid_degraded_path_defined"):
            return Decision.BLOCK
        if not state.get("degraded_conditions_satisfied"):
            return Decision.BLOCK
        if not state.get("human_authority_bound"):
            return Decision.BLOCK
        if not state.get("authorization_valid"):
            return Decision.BLOCK

        return Decision.EXECUTE_DEGRADED


class TemporalState:
    BEFORE = "BEFORE"
    DURING = "DURING"
    AFTER = "AFTER"


@pytest.fixture
def fail_closed():
    return FailClosedEvaluator()


@pytest.fixture
def degraded_path():
    return DegradedPathEvaluator()
