"""Hardware specification models.

Specs come from operation + datasheet + system definition — not invented defaults.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(frozen=True)
class ComponentSpec:
    """Required component with measurable operating envelope."""

    component_id: str
    required: bool = True
    # Numeric envelope: None means not required for this check
    v_min: Optional[float] = None
    v_max: Optional[float] = None
    i_min: Optional[float] = None
    i_max: Optional[float] = None
    t_min: Optional[float] = None
    t_max: Optional[float] = None
    drift_max: Optional[float] = None  # absolute |current - reference|
    reference_value: Optional[float] = None
    reference_kind: str = "PREFLIGHT"  # BOOT | PREFLIGHT | CALIBRATION | BASELINE


@dataclass(frozen=True)
class Measurement:
    """A single observation. Observation ≠ acceptability ≠ authorization."""

    name: str  # e.g. voltage, current, temperature
    value: float
    unit: str
    timestamp: str
    component_id: str
    sensor_id: Optional[str] = None
    freshness_ok: bool = True
    calibration_valid: bool = True


@dataclass(frozen=True)
class PortState:
    port_id: str
    status: str  # REQUIRED | OPTIONAL | DISABLED | ISOLATED | UNKNOWN


@dataclass
class SpecCheckResult:
    ok: bool
    reason_codes: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "reason_codes": list(self.reason_codes),
            "details": dict(self.details),
        }


@dataclass
class HardwareBindResult:
    """Technical hardware/environment bind outcome — not a permit."""

    hardware_green: bool
    reason_codes: list[str] = field(default_factory=list)
    component_results: dict[str, SpecCheckResult] = field(default_factory=dict)
    ports_ok: bool = False
    scope_locked: bool = False
    authorization: bool = False  # always False from this interface

    def to_dict(self) -> dict[str, Any]:
        return {
            "hardware_green": self.hardware_green,
            "reason_codes": list(self.reason_codes),
            "component_results": {k: v.to_dict() for k, v in self.component_results.items()},
            "ports_ok": self.ports_ok,
            "scope_locked": self.scope_locked,
            "authorization": False,
            "note": "HARDWARE_GREEN ≠ AUTHORIZATION",
        }
