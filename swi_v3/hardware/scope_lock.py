"""Workflow scope lock: bound component set is fixed while ACTIVE.

RUNTIME_DISCOVERY ⊬ WORKFLOW_SCOPE_EXPANSION
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class WorkflowScopeLock:
    workflow_id: str
    bound_components: set[str] = field(default_factory=set)
    active: bool = False

    def start(self, bound: set[str]) -> None:
        self.bound_components = set(bound)
        self.active = True

    def stop(self) -> None:
        self.active = False

    def accept_component(self, component_id: str) -> tuple[bool, str]:
        """Return (accepted, reason_code)."""
        if not self.active:
            return False, "SCOPE_NOT_ACTIVE"
        if component_id in self.bound_components:
            return True, "IN_BINDING"
        return False, "HV-035_UNBOUND_HARDWARE_REJECTED"

    def detect_new(self, discovered: set[str]) -> list[str]:
        if not self.active:
            return []
        return sorted(discovered - self.bound_components)
