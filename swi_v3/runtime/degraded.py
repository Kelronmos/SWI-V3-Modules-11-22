"""Degraded-path runtime control.

DEGRADED_PATH ≠ FALLBACK
DEGRADED_PATH ≠ AUTOMATIC_PERMISSION
DEGRADED_PATH ≠ NEW_AUTHORITY
"""
from __future__ import annotations

from typing import Any

from .fail_closed import Decision


class DegradedPathRuntime:
    def evaluate(self, state: dict[str, Any]) -> Decision:
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
