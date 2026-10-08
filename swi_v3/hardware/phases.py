"""Before / during / after hardware revalidation phases.

MATCH(t0) does not authorize at t1.
PRE/DURING/POST are technical checkpoints only.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional

from .components import (
    ComponentPhase,
    PhysicalComponentChecker,
    PhysicalComponentObservation,
)
from .models import HardwareBindResult
from .scope_lock import WorkflowScopeLock


@dataclass
class PhaseEvaluation:
    phase: ComponentPhase
    result: HardwareBindResult
    reason_codes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "phase": self.phase.value,
            "hardware_green": self.result.hardware_green,
            "reason_codes": list(self.reason_codes),
            "authorization": False,
            "note": "PHASE_CHECK ≠ AUTHORIZATION",
        }


class TemporalHardwareValidator:
    """Run component checks at PRE / DURING / POST using existing checker."""

    def __init__(self, checker: Optional[PhysicalComponentChecker] = None):
        self.checker = checker or PhysicalComponentChecker()

    def evaluate_phase(
        self,
        phase: ComponentPhase,
        observations: Iterable[PhysicalComponentObservation],
        *,
        scope: Optional[WorkflowScopeLock] = None,
        expected_identities: Optional[dict[str, str]] = None,
    ) -> PhaseEvaluation:
        result = self.checker.evaluate_set(
            observations,
            phase=phase,
            expected_identities=expected_identities,
            scope=scope,
        )
        return PhaseEvaluation(
            phase=phase,
            result=result,
            reason_codes=list(result.reason_codes),
        )

    def evaluate_sequence(
        self,
        *,
        pre: Iterable[PhysicalComponentObservation],
        during: Iterable[PhysicalComponentObservation],
        post: Iterable[PhysicalComponentObservation],
        scope: Optional[WorkflowScopeLock] = None,
        expected_identities: Optional[dict[str, str]] = None,
    ) -> dict:
        pre_r = self.evaluate_phase(
            ComponentPhase.PRE_EXECUTION, pre, scope=scope, expected_identities=expected_identities
        )
        during_r = self.evaluate_phase(
            ComponentPhase.DURING_EXECUTION,
            during,
            scope=scope,
            expected_identities=expected_identities,
        )
        post_r = self.evaluate_phase(
            ComponentPhase.POST_EXECUTION, post, scope=scope, expected_identities=expected_identities
        )
        all_green = (
            pre_r.result.hardware_green
            and during_r.result.hardware_green
            and post_r.result.hardware_green
        )
        return {
            "pre": pre_r.to_dict(),
            "during": during_r.to_dict(),
            "post": post_r.to_dict(),
            "all_phases_conformant": all_green,
            "authorization": False,
            "note": "TEMPORAL_CONFORMANCE ≠ AUTHORIZATION",
        }
