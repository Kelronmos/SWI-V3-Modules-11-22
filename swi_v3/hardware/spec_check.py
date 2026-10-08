"""Check measurements against component specifications.

MEASURED ≠ ACCEPTABLE
ACCEPTABLE ≠ AUTHORIZED
"""
from __future__ import annotations

from typing import Iterable, Optional

from .models import ComponentSpec, Measurement, SpecCheckResult


class SpecChecker:
    """Verify observed values against declared specs. Does not authorize."""

    def check_measurement(
        self,
        spec: ComponentSpec,
        measurement: Measurement,
        *,
        reference_override: Optional[float] = None,
    ) -> SpecCheckResult:
        reasons: list[str] = []
        details: dict = {
            "component_id": spec.component_id,
            "measurement": measurement.name,
            "value": measurement.value,
            "unit": measurement.unit,
        }

        if measurement.component_id != spec.component_id:
            reasons.append("HV-003_IDENTITY_MISMATCH")

        if not measurement.freshness_ok:
            reasons.append("HV-012_SENSOR_STALE")

        if not measurement.calibration_valid:
            reasons.append("HV-013_CALIBRATION_INVALID")

        name = measurement.name.lower()
        v = measurement.value

        if name in ("voltage", "v") and spec.v_min is not None and spec.v_max is not None:
            details["v_min"] = spec.v_min
            details["v_max"] = spec.v_max
            if v < spec.v_min:
                reasons.append("HV-005_VOLTAGE_BELOW_MIN")
            if v > spec.v_max:
                reasons.append("HV-006_VOLTAGE_ABOVE_MAX")

        if name in ("current", "i") and spec.i_min is not None and spec.i_max is not None:
            details["i_min"] = spec.i_min
            details["i_max"] = spec.i_max
            if v < spec.i_min:
                reasons.append("HV-007_CURRENT_OUT_OF_RANGE")
            if v > spec.i_max:
                reasons.append("HV-007_CURRENT_OUT_OF_RANGE")

        if name in ("temperature", "temp", "t") and spec.t_min is not None and spec.t_max is not None:
            details["t_min"] = spec.t_min
            details["t_max"] = spec.t_max
            if v < spec.t_min or v > spec.t_max:
                reasons.append("HV-008_TEMPERATURE_OUT_OF_RANGE")

        if spec.drift_max is not None:
            ref = reference_override if reference_override is not None else spec.reference_value
            if ref is None:
                reasons.append("HV-010_DRIFT_REFERENCE_MISSING")
            else:
                delta = abs(v - ref)
                details["drift"] = delta
                details["drift_max"] = spec.drift_max
                details["reference"] = ref
                details["reference_kind"] = spec.reference_kind
                if delta > spec.drift_max:
                    reasons.append("HV-010_DRIFT_EXCEEDED")

        return SpecCheckResult(ok=len(reasons) == 0, reason_codes=reasons, details=details)

    def check_component(
        self,
        spec: ComponentSpec,
        measurements: Iterable[Measurement],
        *,
        present: bool,
    ) -> SpecCheckResult:
        reasons: list[str] = []
        details: dict = {"component_id": spec.component_id, "present": present}

        if spec.required and not present:
            reasons.append("HV-001_REQUIRED_HARDWARE_MISSING")
            return SpecCheckResult(ok=False, reason_codes=reasons, details=details)

        if not present:
            return SpecCheckResult(ok=True, reason_codes=[], details=details)

        ms = [m for m in measurements if m.component_id == spec.component_id]
        if spec.required and not ms:
            reasons.append("HV-011_REQUIRED_SENSOR_UNAVAILABLE")
            return SpecCheckResult(ok=False, reason_codes=reasons, details=details)

        for m in ms:
            r = self.check_measurement(spec, m)
            if not r.ok:
                reasons.extend(r.reason_codes)
                details[m.name] = r.details

        # de-dupe while preserving order
        seen: set[str] = set()
        uniq: list[str] = []
        for code in reasons:
            if code not in seen:
                seen.add(code)
                uniq.append(code)

        return SpecCheckResult(ok=len(uniq) == 0, reason_codes=uniq, details=details)
