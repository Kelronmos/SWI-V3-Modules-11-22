"""Physical component types for hardware bind — technical only.

AVAILABLE ≠ REQUIRED ≠ VALID ≠ CONFORMANT ≠ TRUSTED ≠ AUTHORIZED
BIOMETRIC MATCH ≠ HUMAN AUTHORITY ≠ AUTHORIZATION
MICROPHONE_PASS / CAMERA_PASS / SENSOR_PASS ≠ AUTHORIZATION

Physical device acquisition is not implemented here.
SOURCE = TEST_FIXTURE for synthetic observations unless explicitly marked otherwise.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Optional

from .models import ComponentSpec, HardwareBindResult, Measurement, PortState, SpecCheckResult
from .bind import HardwareBindInterface
from .scope_lock import WorkflowScopeLock


class ComponentType(str, Enum):
    MICROPHONE = "MICROPHONE"
    CAMERA = "CAMERA"
    FINGERPRINT = "FINGERPRINT"
    SENSOR = "SENSOR"
    OTHER = "OTHER"


class ComponentPhase(str, Enum):
    PRE_EXECUTION = "PRE_EXECUTION"
    DURING_EXECUTION = "DURING_EXECUTION"
    POST_EXECUTION = "POST_EXECUTION"


class ConformanceStatus(str, Enum):
    HARDWARE_CONFORMANT = "HARDWARE_CONFORMANT"
    HARDWARE_NONCONFORMANT = "HARDWARE_NONCONFORMANT"
    HARDWARE_INDETERMINATE = "HARDWARE_INDETERMINATE"


@dataclass(frozen=True)
class PhysicalComponentObservation:
    """Observation of a physical component. Observation ≠ authorization."""

    component_id: str
    component_type: ComponentType
    device_id: str
    available: bool
    required: bool = True
    identity: Optional[str] = None
    interface_id: Optional[str] = None
    capability: Optional[str] = None
    permission_observable: Optional[bool] = None  # None = unknown
    stream_or_capture_available: Optional[bool] = None
    measurement_valid: Optional[bool] = None
    calibration_state: Optional[str] = None  # VALID | INVALID | UNKNOWN
    timestamp: Optional[str] = None
    freshness_ok: bool = True
    sensor_subtype: Optional[str] = None  # accelerometer, gyroscope, etc.
    source: str = "TEST_FIXTURE"  # TEST_FIXTURE | PHYSICAL_DEVICE | UNKNOWN
    biometric_match: Optional[bool] = None  # observation only; never authority
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "component_id": self.component_id,
            "component_type": self.component_type.value,
            "device_id": self.device_id,
            "available": self.available,
            "required": self.required,
            "identity": self.identity,
            "interface_id": self.interface_id,
            "capability": self.capability,
            "permission_observable": self.permission_observable,
            "stream_or_capture_available": self.stream_or_capture_available,
            "measurement_valid": self.measurement_valid,
            "calibration_state": self.calibration_state,
            "timestamp": self.timestamp,
            "freshness_ok": self.freshness_ok,
            "sensor_subtype": self.sensor_subtype,
            "source": self.source,
            "biometric_match": self.biometric_match,
            "details": dict(self.details),
            "note": "COMPONENT_OBSERVATION ≠ AUTHORIZATION",
        }


@dataclass
class ComponentCheckResult:
    ok: bool
    conformance: ConformanceStatus
    reason_codes: list[str] = field(default_factory=list)
    observation: Optional[PhysicalComponentObservation] = None
    phase: Optional[str] = None
    authorization: bool = False  # always False

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "conformance": self.conformance.value,
            "reason_codes": list(self.reason_codes),
            "observation": self.observation.to_dict() if self.observation else None,
            "phase": self.phase,
            "authorization": False,
            "note": "HARDWARE_CONFORMANT ≠ AUTHORIZATION",
        }


class PhysicalComponentChecker:
    """Evaluate physical component observations into technical reason codes.

    Does not acquire sensors. Does not authorize.
    """

    def check_observation(
        self,
        obs: PhysicalComponentObservation,
        *,
        phase: Optional[ComponentPhase] = None,
        expected_identity: Optional[str] = None,
    ) -> ComponentCheckResult:
        reasons: list[str] = []

        if obs.source not in ("TEST_FIXTURE", "PHYSICAL_DEVICE", "UNKNOWN"):
            reasons.append("HV-040_SOURCE_UNRECOGNIZED")

        if obs.required and not obs.available:
            reasons.append("HV-001_REQUIRED_HARDWARE_MISSING")
            if obs.component_type == ComponentType.MICROPHONE:
                reasons.append("HV-041_MICROPHONE_MISSING")
            elif obs.component_type == ComponentType.CAMERA:
                reasons.append("HV-042_CAMERA_MISSING")
            elif obs.component_type == ComponentType.FINGERPRINT:
                reasons.append("HV-043_FINGERPRINT_MISSING")
            elif obs.component_type == ComponentType.SENSOR:
                reasons.append("HV-011_REQUIRED_SENSOR_UNAVAILABLE")

        if obs.available:
            if expected_identity is not None and obs.identity is not None:
                if obs.identity != expected_identity:
                    reasons.append("HV-003_IDENTITY_MISMATCH")
            if obs.permission_observable is False:
                reasons.append("HV-044_PERMISSION_NOT_GRANTED")
            if obs.permission_observable is None and obs.required:
                reasons.append("HV-045_PERMISSION_STATE_UNKNOWN")
            if obs.stream_or_capture_available is False and obs.required:
                reasons.append("HV-046_STREAM_OR_CAPTURE_UNAVAILABLE")
            if obs.measurement_valid is False:
                reasons.append("HV-047_MEASUREMENT_INVALID")
            if obs.calibration_state == "INVALID":
                reasons.append("HV-013_CALIBRATION_INVALID")
            if obs.calibration_state == "UNKNOWN" and obs.required:
                reasons.append("HV-048_CALIBRATION_UNKNOWN")
            if not obs.freshness_ok:
                reasons.append("HV-012_SENSOR_STALE")
            if obs.timestamp is None and obs.required:
                reasons.append("HV-049_TIMESTAMP_MISSING")

        # Biometric match is observation only — never elevates to authority
        if obs.component_type == ComponentType.FINGERPRINT and obs.biometric_match is True:
            # Explicit non-escalation marker in details; no reason (not a failure)
            pass

        uniq = list(dict.fromkeys(reasons))
        if not uniq:
            conf = ConformanceStatus.HARDWARE_CONFORMANT
            if obs.available and obs.permission_observable is None and not obs.required:
                conf = ConformanceStatus.HARDWARE_INDETERMINATE
        else:
            # unknown/missing evidence → nonconformant (fail closed for required)
            conf = ConformanceStatus.HARDWARE_NONCONFORMANT
            if any(c.endswith("_UNKNOWN") or "UNKNOWN" in c for c in uniq) and not any(
                c.endswith("_MISSING") for c in uniq
            ):
                conf = ConformanceStatus.HARDWARE_INDETERMINATE

        return ComponentCheckResult(
            ok=len(uniq) == 0,
            conformance=conf,
            reason_codes=uniq,
            observation=obs,
            phase=phase.value if phase else None,
            authorization=False,
        )

    def evaluate_set(
        self,
        observations: Iterable[PhysicalComponentObservation],
        *,
        phase: Optional[ComponentPhase] = None,
        expected_identities: Optional[dict[str, str]] = None,
        scope: Optional[WorkflowScopeLock] = None,
    ) -> HardwareBindResult:
        """Fold component checks into existing HardwareBindResult shape."""
        expected_identities = expected_identities or {}
        reasons: list[str] = []
        component_results: dict[str, SpecCheckResult] = {}
        observations = list(observations)

        if scope is not None and scope.active:
            discovered = {o.component_id for o in observations}
            newcomers = scope.detect_new(discovered)
            for c in newcomers:
                ok, code = scope.accept_component(c)
                if not ok:
                    reasons.append(code)

        for obs in observations:
            cr = self.check_observation(
                obs,
                phase=phase,
                expected_identity=expected_identities.get(obs.component_id),
            )
            component_results[obs.component_id] = SpecCheckResult(
                ok=cr.ok,
                reason_codes=list(cr.reason_codes),
                details=cr.to_dict(),
            )
            if not cr.ok:
                reasons.extend(cr.reason_codes)

        uniq = list(dict.fromkeys(reasons))
        return HardwareBindResult(
            hardware_green=len(uniq) == 0,
            reason_codes=uniq,
            component_results=component_results,
            ports_ok=True,
            scope_locked=bool(scope and scope.active),
            authorization=False,
        )


def observations_to_present(
    observations: Iterable[PhysicalComponentObservation],
) -> dict[str, bool]:
    return {o.component_id: o.available for o in observations}


def observations_to_specs(
    observations: Iterable[PhysicalComponentObservation],
) -> list[ComponentSpec]:
    """Minimal ComponentSpec list for bind.evaluate present/required checks."""
    return [
        ComponentSpec(component_id=o.component_id, required=o.required)
        for o in observations
    ]
