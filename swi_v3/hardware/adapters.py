"""Physical device adapter boundary.

PHYSICAL_ANDROID_SENSOR_ADAPTER = NOT_IMPLEMENTED
PHYSICAL device acquisition is not performed in this module.

Use explicit placeholders for platform commands. Never treat placeholders
as executed physical tests.

SOFTWARE FIXTURE TEST ≠ PHYSICAL DEVICE TEST
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from .components import ComponentType, PhysicalComponentObservation


# Explicit placeholders — not executables
ANDROID_SENSOR_COMMAND = "<ANDROID_SENSOR_COMMAND>"
ANDROID_CAMERA_COMMAND = "<ANDROID_CAMERA_COMMAND>"
ANDROID_MIC_COMMAND = "<ANDROID_MIC_COMMAND>"
ANDROID_BIOMETRIC_COMMAND = "<ANDROID_BIOMETRIC_COMMAND>"
PHYSICAL_SENSOR_TEST = "<PHYSICAL_SENSOR_TEST>"


@dataclass(frozen=True)
class AdapterCapability:
    name: str
    implemented: bool
    physical: bool
    note: str


class PhysicalDeviceAdapter:
    """Adapter boundary for real hardware acquisition.

    Default implementation does not read physical sensors.
    """

    ADAPTER_STATUS = "NOT_IMPLEMENTED"
    PHYSICAL_ANDROID_SENSOR_ADAPTER = "NOT_IMPLEMENTED"

    def capabilities(self) -> list[AdapterCapability]:
        return [
            AdapterCapability(
                "microphone",
                implemented=False,
                physical=True,
                note=f"Use {ANDROID_MIC_COMMAND} when platform provides it",
            ),
            AdapterCapability(
                "camera",
                implemented=False,
                physical=True,
                note=f"Use {ANDROID_CAMERA_COMMAND} when platform provides it",
            ),
            AdapterCapability(
                "fingerprint",
                implemented=False,
                physical=True,
                note=f"Use {ANDROID_BIOMETRIC_COMMAND} when platform provides it",
            ),
            AdapterCapability(
                "general_sensors",
                implemented=False,
                physical=True,
                note=f"Use {ANDROID_SENSOR_COMMAND} / {PHYSICAL_SENSOR_TEST}",
            ),
        ]

    def acquire(
        self,
        component_type: ComponentType,
        *,
        component_id: str,
        device_id: str,
        required: bool = True,
    ) -> PhysicalComponentObservation:
        """Attempt physical acquisition — always returns UNKNOWN/unavailable here.

        Does not fabricate physical readings.
        """
        return PhysicalComponentObservation(
            component_id=component_id,
            component_type=component_type,
            device_id=device_id,
            available=False,
            required=required,
            identity=None,
            permission_observable=None,
            stream_or_capture_available=None,
            measurement_valid=None,
            calibration_state="UNKNOWN",
            freshness_ok=False,
            source="UNKNOWN",
            details={
                "adapter_status": self.ADAPTER_STATUS,
                "physical_android_sensor_adapter": self.PHYSICAL_ANDROID_SENSOR_ADAPTER,
                "note": "PHYSICAL_ACQUISITION_NOT_IMPLEMENTED",
            },
        )

    def fixture_observation(
        self,
        component_type: ComponentType,
        *,
        component_id: str,
        device_id: str,
        available: bool = True,
        required: bool = True,
        identity: Optional[str] = None,
        permission_observable: Optional[bool] = True,
        stream_or_capture_available: Optional[bool] = True,
        measurement_valid: Optional[bool] = True,
        calibration_state: str = "VALID",
        timestamp: str = "2026-10-08T00:00:00Z",
        freshness_ok: bool = True,
        sensor_subtype: Optional[str] = None,
        biometric_match: Optional[bool] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> PhysicalComponentObservation:
        """Construct an explicitly labelled TEST_FIXTURE observation."""
        return PhysicalComponentObservation(
            component_id=component_id,
            component_type=component_type,
            device_id=device_id,
            available=available,
            required=required,
            identity=identity or component_id,
            permission_observable=permission_observable,
            stream_or_capture_available=stream_or_capture_available,
            measurement_valid=measurement_valid,
            calibration_state=calibration_state,
            timestamp=timestamp,
            freshness_ok=freshness_ok,
            sensor_subtype=sensor_subtype,
            source="TEST_FIXTURE",
            biometric_match=biometric_match,
            details=dict(details or {}, fixture=True),
        )
