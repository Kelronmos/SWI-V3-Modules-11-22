"""Deterministic cross-device fixtures. SOURCE = TEST_FIXTURE only.

Not physical device evidence.
"""
from __future__ import annotations

DEVICE_FIXTURES = {
    "PC": {
        "source": "TEST_FIXTURE",
        "components": ["cpu", "secure_identity", "power_rail", "network"],
        "sensors": ["temperature", "power"],
    },
    "MOBILE": {
        "source": "TEST_FIXTURE",
        "components": ["battery", "secure_identity", "network"],
        "sensors": ["accelerometer", "gyroscope", "gnss", "battery_level"],
    },
    "WATCH": {
        "source": "TEST_FIXTURE",
        "components": ["battery", "optical_sensor", "connectivity"],
        "sensors": ["accelerometer", "gyroscope", "optical"],
    },
}
