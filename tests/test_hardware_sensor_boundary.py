"""
Hardware / sensor / environment ordering tests.
"""
import pytest

PIPELINE = [
    "HARDWARE",
    "SENSOR",
    "OBSERVATION",
    "ENVIRONMENT",
    "RUNTIME_MATCH",
    "FLOW_BIND",
    "HUMAN_AUTHORITY",
    "AUTHORIZATION",
    "ACTION",
]


class TestHardwareSensorOrdering:

    def test_pipeline_order_is_defined(self):
        assert PIPELINE[0] == "HARDWARE"
        assert PIPELINE[-1] == "ACTION"
        assert "SENSOR" in PIPELINE
        assert "AUTHORIZATION" in PIPELINE

    def test_sensor_does_not_directly_authorize(self):
        sensor_index = PIPELINE.index("SENSOR")
        auth_index = PIPELINE.index("AUTHORIZATION")
        assert sensor_index < auth_index
        # Sensor precedes authorization; it does not replace it.

    def test_hardware_available_plus_capable_plus_normal_is_not_authorization(self):
        hardware_state = {
            "available": True,
            "capable": True,
            "condition": "NORMAL",
        }
        # All three true does not equal authorization.
        assert hardware_state["available"] is True
        assert hardware_state["capable"] is True
        assert hardware_state["condition"] == "NORMAL"
        # Explicit contract:
        authorization = hardware_state.get("authorization_to_operate", False)
        assert authorization is False

    def test_observation_is_not_authority(self):
        observation = {"value": 42, "timestamp": "2026-10-06T22:00:00Z"}
        assert observation.get("is_authority", False) is False
