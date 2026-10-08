"""Hardware/environment bind interface.

HARDWARE_BIND is a technical condition. It does not mint a permit.
"""
from __future__ import annotations

from typing import Iterable, Optional

from .models import (
    ComponentSpec,
    HardwareBindResult,
    Measurement,
    PortState,
)
from .scope_lock import WorkflowScopeLock
from .spec_check import SpecChecker


class HardwareBindInterface:
    """Check and verify hardware/environment specs for an operation."""

    def __init__(self, checker: Optional[SpecChecker] = None):
        self.checker = checker or SpecChecker()

    def check_ports(self, ports: Iterable[PortState]) -> tuple[bool, list[str]]:
        reasons: list[str] = []
        ports = list(ports)
        for p in ports:
            st = p.status.upper()
            if st == "UNKNOWN":
                reasons.append("HV-017_UNKNOWN_INTERFACE")
            if st == "REQUIRED":
                pass  # presence of required port entry assumed declared
        # Unaccepted still operational is a policy signal from caller
        for p in ports:
            if p.status.upper() in ("UNKNOWN",) or (
                p.status.upper() not in ("REQUIRED", "OPTIONAL", "DISABLED", "ISOLATED", "UNKNOWN")
            ):
                if p.status.upper() not in ("REQUIRED", "OPTIONAL", "DISABLED", "ISOLATED", "UNKNOWN"):
                    reasons.append("HV-016_UNACCEPTED_INTERFACE_STATE")
        # de-dupe
        uniq = list(dict.fromkeys(reasons))
        return len(uniq) == 0, uniq

    def evaluate(
        self,
        *,
        specs: Iterable[ComponentSpec],
        measurements: Iterable[Measurement],
        present: dict[str, bool],
        ports: Iterable[PortState],
        scope: Optional[WorkflowScopeLock] = None,
        discovered_components: Optional[set[str]] = None,
    ) -> HardwareBindResult:
        reasons: list[str] = []
        component_results = {}
        measurements = list(measurements)

        for spec in specs:
            is_present = present.get(spec.component_id, False)
            result = self.checker.check_component(spec, measurements, present=is_present)
            component_results[spec.component_id] = result
            if not result.ok:
                reasons.extend(result.reason_codes)

        ports_ok, port_reasons = self.check_ports(ports)
        if not ports_ok:
            reasons.extend(port_reasons)

        scope_locked = False
        if scope is not None and scope.active:
            scope_locked = True
            if discovered_components:
                newcomers = scope.detect_new(discovered_components)
                for c in newcomers:
                    ok, code = scope.accept_component(c)
                    if not ok:
                        reasons.append(code)

        # de-dupe reasons
        uniq = list(dict.fromkeys(reasons))
        hardware_green = len(uniq) == 0

        return HardwareBindResult(
            hardware_green=hardware_green,
            reason_codes=uniq,
            component_results=component_results,
            ports_ok=ports_ok,
            scope_locked=scope_locked,
            authorization=False,
        )
