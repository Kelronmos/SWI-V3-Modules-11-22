"""Seal state machine.

UNSEALED → SEAL_ELIGIBLE → SEAL_CREATED → SEAL_VERIFIED → ACTIVE
SEAL_ELIGIBLE → FAILED
ACTIVE → INVALIDATED → REVALIDATION_REQUIRED
"""

from __future__ import annotations

from .models import SealState


ALLOWED_TRANSITIONS = {
    SealState.UNSEALED: {SealState.SEAL_ELIGIBLE},
    SealState.SEAL_ELIGIBLE: {SealState.SEAL_CREATED, SealState.FAILED},
    SealState.SEAL_CREATED: {SealState.SEAL_VERIFIED, SealState.FAILED},
    SealState.SEAL_VERIFIED: {SealState.ACTIVE, SealState.FAILED},
    SealState.ACTIVE: {SealState.INVALIDATED, SealState.REVALIDATION_REQUIRED},
    SealState.INVALIDATED: {SealState.REVALIDATION_REQUIRED},
    SealState.REVALIDATION_REQUIRED: {SealState.SEAL_ELIGIBLE},  # new process only
    SealState.FAILED: {SealState.SEAL_ELIGIBLE},  # retry eligibility only
}


class SealStateMachine:
    def __init__(self, state: SealState = SealState.UNSEALED):
        self.state = state

    def can_transition(self, target: SealState) -> bool:
        return target in ALLOWED_TRANSITIONS.get(self.state, set())

    def transition(self, target: SealState) -> SealState:
        if not self.can_transition(target):
            raise ValueError(f"Illegal transition {self.state.value} → {target.value}")
        self.state = target
        return self.state

    def is_active(self) -> bool:
        return self.state == SealState.ACTIVE

    def is_usable(self) -> bool:
        return self.state == SealState.ACTIVE
