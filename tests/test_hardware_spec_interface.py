"""Hardware spec-check interface tests.

HARDWARE_GREEN ≠ AUTHORIZATION
"""
from __future__ import annotations

from swi_v3.hardware import (
    ComponentSpec,
    HardwareBindInterface,
    Measurement,
    PortState,
    SpecChecker,
    WorkflowScopeLock,
)


class TestSpecChecker:
    def test_voltage_within_spec_passes(self):
        spec = ComponentSpec("rail-12", v_min=11.4, v_max=12.6)
        m = Measurement("voltage", 12.1, "V", "2026-10-08T08:00:00Z", "rail-12")
        r = SpecChecker().check_measurement(spec, m)
        assert r.ok is True

    def test_voltage_below_min_fails(self):
        spec = ComponentSpec("rail-12", v_min=11.4, v_max=12.6)
        m = Measurement("voltage", 10.4, "V", "2026-10-08T08:00:00Z", "rail-12")
        r = SpecChecker().check_measurement(spec, m)
        assert r.ok is False
        assert "HV-005_VOLTAGE_BELOW_MIN" in r.reason_codes

    def test_drift_exceeded(self):
        spec = ComponentSpec(
            "rail-12", v_min=11.0, v_max=13.0, drift_max=0.2, reference_value=12.0
        )
        m = Measurement("voltage", 12.5, "V", "2026-10-08T08:00:00Z", "rail-12")
        r = SpecChecker().check_measurement(spec, m)
        assert r.ok is False
        assert "HV-010_DRIFT_EXCEEDED" in r.reason_codes

    def test_missing_required_component(self):
        spec = ComponentSpec("tpm", required=True)
        r = SpecChecker().check_component(spec, [], present=False)
        assert r.ok is False
        assert "HV-001_REQUIRED_HARDWARE_MISSING" in r.reason_codes


class TestHardwareBindInterface:
    def test_green_is_not_authorization(self):
        iface = HardwareBindInterface()
        spec = ComponentSpec("rail-12", v_min=11.4, v_max=12.6)
        m = Measurement("voltage", 12.1, "V", "2026-10-08T08:00:00Z", "rail-12")
        result = iface.evaluate(
            specs=[spec],
            measurements=[m],
            present={"rail-12": True},
            ports=[PortState("eth0", "REQUIRED")],
        )
        assert result.hardware_green is True
        assert result.authorization is False
        assert result.to_dict()["authorization"] is False

    def test_sensor_pass_does_not_authorize(self):
        iface = HardwareBindInterface()
        result = iface.evaluate(
            specs=[],
            measurements=[],
            present={},
            ports=[],
        )
        # empty required set → technically green path
        assert result.authorization is False

    def test_unknown_port_blocks_green(self):
        iface = HardwareBindInterface()
        result = iface.evaluate(
            specs=[],
            measurements=[],
            present={},
            ports=[PortState("usb1", "UNKNOWN")],
        )
        assert result.hardware_green is False
        assert "HV-017_UNKNOWN_INTERFACE" in result.reason_codes


class TestWorkflowScopeLock:
    def test_new_component_rejected_while_active(self):
        lock = WorkflowScopeLock("W-1")
        lock.start({"phone-gps", "phone-accel"})
        ok, code = lock.accept_component("watch-hr")
        assert ok is False
        assert code == "HV-035_UNBOUND_HARDWARE_REJECTED"

    def test_bound_component_accepted(self):
        lock = WorkflowScopeLock("W-1")
        lock.start({"phone-gps"})
        ok, code = lock.accept_component("phone-gps")
        assert ok is True

    def test_runtime_discovery_does_not_expand_scope(self):
        iface = HardwareBindInterface()
        lock = WorkflowScopeLock("W-1")
        lock.start({"rail-12"})
        result = iface.evaluate(
            specs=[ComponentSpec("rail-12", v_min=11.0, v_max=13.0)],
            measurements=[
                Measurement("voltage", 12.0, "V", "2026-10-08T08:00:00Z", "rail-12")
            ],
            present={"rail-12": True},
            ports=[],
            scope=lock,
            discovered_components={"rail-12", "new-sensor"},
        )
        assert result.hardware_green is False
        assert "HV-035_UNBOUND_HARDWARE_REJECTED" in result.reason_codes
        assert result.authorization is False
