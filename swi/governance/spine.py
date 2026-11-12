"""SWI V3 governance spine (foundation).

STATUS: IMPLEMENTED (candidate) · TESTED (unit) · PROVEN=NO · SEALED=NO · PRODUCTION_AUTHORIZED=NO

Distinctions:
  UNKNOWN ≠ FALSE
  OBSERVATION ≠ EVIDENCE ≠ AUTHORIZATION
  CAPABILITY ≠ PERMISSION
  INSTRUCTION ≠ AUTHORIZATION
  TESTED ≠ PROVEN ≠ SEALED ≠ PRODUCTION_AUTHORIZED

This is the sole authorization evaluator in the V3 foundation package.
CEK, sensors, and patches do not grant permits.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, FrozenSet, Iterable, Mapping, Optional


class PermitOutcome(str, Enum):
    PERMITTED = "PERMITTED"
    REJECTED = "REJECTED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class GoverningEvaluation:
    outcome: PermitOutcome
    reason: str
    conditions: FrozenSet[str]
    layer_status: Mapping[str, str]
    evidence_present: bool
    failed_layers: tuple[str, ...]
    contract_id: str = "swi_v3_governing_permit_v0"
    proven: bool = False
    sealed: bool = False
    production_authorized: bool = False

    def is_permitted(self) -> bool:
        return self.outcome is PermitOutcome.PERMITTED


def _as_frozenset(value: Optional[Iterable[str]]) -> Optional[FrozenSet[str]]:
    if value is None:
        return None
    return frozenset(value)


def _evidence_exists(evidence: Any) -> bool:
    if evidence is None or evidence is False:
        return False
    if isinstance(evidence, (str, bytes, bytearray, list, tuple, set, frozenset, dict)):
        return len(evidence) > 0
    return True


def evaluate_governing_permit(
    *,
    conditions: Iterable[str],
    L: Optional[Iterable[str]] = None,
    G: Optional[Iterable[str]] = None,
    S: Optional[Iterable[str]] = None,
    H: Optional[Iterable[str]] = None,
    evidence: Any = None,
) -> GoverningEvaluation:
    """Permit(a) ⟺ ∀L,G,S,H: C(a) ⊆ L ∩ G ∩ S ∩ H  ∧  E(a) ≠ ∅"""
    C = frozenset(conditions)
    layers: dict[str, Optional[FrozenSet[str]]] = {
        "L": _as_frozenset(L),
        "G": _as_frozenset(G),
        "S": _as_frozenset(S),
        "H": _as_frozenset(H),
    }
    layer_status: dict[str, str] = {}
    failed: list[str] = []
    unknown_layers: list[str] = []

    for name, layer in layers.items():
        if layer is None:
            layer_status[name] = "unknown"
            unknown_layers.append(name)
            continue
        if not C.issubset(layer):
            layer_status[name] = "fail"
            failed.append(name)
        else:
            layer_status[name] = "ok"

    evidence_present = _evidence_exists(evidence)

    if unknown_layers:
        return GoverningEvaluation(
            outcome=PermitOutcome.UNKNOWN,
            reason=f"required_layer_unknown:{','.join(sorted(unknown_layers))}",
            conditions=C,
            layer_status=layer_status,
            evidence_present=evidence_present,
            failed_layers=tuple(failed),
        )
    if failed:
        return GoverningEvaluation(
            outcome=PermitOutcome.REJECTED,
            reason=f"condition_not_subset_of:{','.join(sorted(failed))}",
            conditions=C,
            layer_status=layer_status,
            evidence_present=evidence_present,
            failed_layers=tuple(sorted(failed)),
        )
    if not evidence_present:
        return GoverningEvaluation(
            outcome=PermitOutcome.REJECTED,
            reason="evidence_empty",
            conditions=C,
            layer_status=layer_status,
            evidence_present=False,
            failed_layers=(),
        )
    return GoverningEvaluation(
        outcome=PermitOutcome.PERMITTED,
        reason="all_layers_satisfied_and_evidence_present",
        conditions=C,
        layer_status=layer_status,
        evidence_present=True,
        failed_layers=(),
    )


def observation_does_not_authorize(observation: Any) -> bool:
    return True


def signature_does_not_authorize(signature: Any) -> bool:
    return True
