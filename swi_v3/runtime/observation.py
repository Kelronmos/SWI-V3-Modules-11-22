"""Hardware → Sensor → Observation pipeline (executable boundary).

OBSERVATION ≠ AUTHORITY
SENSOR ≠ AUTHORIZATION
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class Observation:
    sensor_id: str
    value: Any
    timestamp: str
    context: dict
    hardware_id: Optional[str] = None
    integrity_ok: bool = True
    stale: bool = False

    def to_dict(self) -> dict:
        return {
            "sensor_id": self.sensor_id,
            "value": self.value,
            "timestamp": self.timestamp,
            "context": dict(self.context),
            "hardware_id": self.hardware_id,
            "integrity_ok": self.integrity_ok,
            "stale": self.stale,
        }


class ObservationPipeline:
    """Ordered pipeline: HARDWARE → SENSOR → OBSERVATION.

    Does not authorize action.
    """

    def observe(
        self,
        hardware_id: str,
        sensor_id: str,
        value: Any,
        context: dict,
        *,
        hardware_available: bool = True,
        hardware_capable: bool = True,
        timestamp: Optional[str] = None,
        integrity_ok: bool = True,
        stale: bool = False,
    ) -> tuple[Optional[Observation], list[str]]:
        errors: list[str] = []

        if not hardware_available:
            errors.append("HARDWARE_UNAVAILABLE")
        if not hardware_capable:
            errors.append("HARDWARE_NOT_CAPABLE")
        if not sensor_id:
            errors.append("SENSOR_MISSING")
        if not integrity_ok:
            errors.append("INTEGRITY_FAILURE")

        if errors:
            return None, errors

        if timestamp is None:
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        obs = Observation(
            sensor_id=sensor_id,
            value=value,
            timestamp=timestamp,
            context=dict(context),
            hardware_id=hardware_id,
            integrity_ok=integrity_ok,
            stale=stale,
        )
        return obs, []

    def to_gate_state(self, obs: Optional[Observation], errors: list[str]) -> dict:
        """Map observation outcome into fail-closed / gate inputs."""
        state: dict[str, Any] = {}
        if errors:
            if "HARDWARE_UNAVAILABLE" in errors or "SENSOR_MISSING" in errors:
                state["required_component_missing"] = True
            if "INTEGRITY_FAILURE" in errors:
                state["integrity_failure"] = True
            if "HARDWARE_NOT_CAPABLE" in errors:
                state["required_prerequisite_unsatisfied"] = True
            return state

        assert obs is not None
        if not obs.integrity_ok:
            state["integrity_failure"] = True
        if obs.stale:
            state["required_evidence_stale"] = True
        return state
