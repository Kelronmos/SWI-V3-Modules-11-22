"""Deterministic cross-device fixtures. SOURCE = TEST_FIXTURE only.

Not physical device evidence.
SOFTWARE FIXTURE TEST ≠ PHYSICAL DEVICE TEST
"""
from __future__ import annotations

DEVICE_FIXTURES = {
    "PC": {
        "source": "TEST_FIXTURE",
        "components": ["cpu", "secure_identity", "power_rail", "network", "microphone", "camera"],
        "sensors": ["temperature", "power"],
        "physical_components": ["microphone", "camera"],
    },
    "MOBILE": {
        "source": "TEST_FIXTURE",
        "components": [
            "battery",
            "secure_identity",
            "network",
            "microphone",
            "camera",
            "fingerprint",
        ],
        "sensors": [
            "accelerometer",
            "gyroscope",
            "gnss",
            "battery_level",
            "proximity",
            "ambient_light",
        ],
        "physical_components": ["microphone", "camera", "fingerprint"],
    },
    "WATCH": {
        "source": "TEST_FIXTURE",
        "components": ["battery", "optical_sensor", "connectivity"],
        "sensors": ["accelerometer", "gyroscope", "optical"],
        "physical_components": [],
    },
}

# Explicit: these fixtures are software-only.
PHYSICAL_DEVICE_TEST_STATUS = "NOT_EXECUTED"
HARDWARE_EVIDENCE_TO_SEAL = "NOT_IMPLEMENTED"
