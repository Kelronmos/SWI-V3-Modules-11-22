"""Hardware bind kernel integration + adversarial tests.

SOURCE = TEST_FIXTURE. HARDWARE_GREEN ≠ AUTHORIZATION.
"""
from __future__ import annotations

from swi_v3.hardware import (
    ComponentSpec,
    HardwareBindInterface,
    Measurement,
    PortState,
    WorkflowScopeLock,
)
from swi_v3.hardware.records import HardwareTestRecord, replay_twice
from swi_v3.runtime.engine import RuntimeEngine


def _rail_spec(**kw):
    base = dict(component_id="rail-12", v_min=11.4, v_max=12.6)
    base.update(kw)
    return ComponentSpec(**base)


class TestKernelHardwareIntegration:
    def test_evaluate_hardware_never_authorizes(self):
        eng = RuntimeEngine()
        hb = eng.evaluate_hardware(
            specs=[_rail_spec()],
            measurements=[Measurement("voltage", 12.1, "V", "t0", "rail-12")],
            present={"rail-12": True},
            ports=[PortState("eth0", "REQUIRED")],
        )
        assert hb.hardware_green is True
        assert hb.authorization is False

    def test_observe_and_gate_with_failed_bind_does_not_permit_via_hardware(self):
        eng = RuntimeEngine()
        hb = eng.evaluate_hardware(
            specs=[_rail_spec()],
            measurements=[Measurement("voltage", 10.0, "V", "t0", "rail-12")],
            present={"rail-12": True},
            ports=[],
        )
        assert hb.hardware_green is False
        out = eng.observe_and_gate(
            hardware_id="rail-12",
            sensor_id="vmon",
            value=10.0,
            context={"workflow": "W-1"},
            gate_state={
                "flow_bound": True,
                "runtime_match": True,
                "human_authority_bound": True,
                "authorization_valid": True,
            },
            hardware_bind=hb,
        )
        # Gate may block; hardware must not set authorization True
        assert out.get("hardware_bind", {}).get("authorization") is False


class TestAdversarialHardware:
    def test_hb_013_unbound_component_mid_flow(self):
        lock = WorkflowScopeLock("W-mobile")
        lock.start({"phone-gps", "phone-accel"})
        iface = HardwareBindInterface()
        r = iface.evaluate(
            specs=[],
            measurements=[],
            present={},
            ports=[],
            scope=lock,
            discovered_components={"phone-gps", "phone-accel", "watch-hr"},
        )
        assert r.hardware_green is False
        assert "HV-035_UNBOUND_HARDWARE_REJECTED" in r.reason_codes
        assert r.authorization is False

    def test_hb_018_watch_halfway_rejected(self):
        lock = WorkflowScopeLock("W-mobile")
        lock.start({"phone-gps"})
        ok, code = lock.accept_component("watch-hr")
        assert ok is False
        assert code == "HV-035_UNBOUND_HARDWARE_REJECTED"

    def test_before_during_after_not_collapsed(self):
        checker = HardwareBindInterface()
        spec = _rail_spec(drift_max=0.15, reference_value=12.0)
        before = checker.evaluate(
            specs=[spec],
            measurements=[Measurement("voltage", 12.0, "V", "t0", "rail-12")],
            present={"rail-12": True},
            ports=[],
        )
        during = checker.evaluate(
            specs=[spec],
            measurements=[Measurement("voltage", 10.4, "V", "t1", "rail-12")],
            present={"rail-12": True},
            ports=[],
        )
        after = checker.evaluate(
            specs=[spec],
            measurements=[Measurement("voltage", 12.0, "V", "t2", "rail-12")],
            present={"rail-12": True},
            ports=[],
        )
        assert before.hardware_green is True
        assert during.hardware_green is False
        assert after.hardware_green is True
        # BEFORE pass must not authorize DURING
        assert during.authorization is False

    def test_green_cannot_mint_authorization(self):
        iface = HardwareBindInterface()
        r = iface.evaluate(
            specs=[_rail_spec()],
            measurements=[Measurement("voltage", 12.1, "V", "t0", "rail-12")],
            present={"rail-12": True},
            ports=[],
        )
        assert r.hardware_green is True
        # Explicit adversarial: no field path yields authorization True
        assert r.authorization is False
        assert r.to_dict()["authorization"] is False

    def test_stale_and_calibration_fail(self):
        iface = HardwareBindInterface()
        r = iface.evaluate(
            specs=[_rail_spec()],
            measurements=[
                Measurement(
                    "voltage", 12.1, "V", "t0", "rail-12",
                    freshness_ok=False, calibration_valid=False,
                )
            ],
            present={"rail-12": True},
            ports=[],
        )
        assert r.hardware_green is False
        assert "HV-012_SENSOR_STALE" in r.reason_codes
        assert "HV-013_CALIBRATION_INVALID" in r.reason_codes


class TestHardwareRecordsReplay:
    def test_record_replay_deterministic(self):
        rec = HardwareTestRecord(
            test_id="HB-003",
            workflow_id="W-1",
            operation_id="op-rail",
            device_class="PC",
            component_set=["rail-12"],
            sensor_set=["vmon"],
            expected_spec={"v_min": 11.4, "v_max": 12.6},
            observations={"voltage": 10.0},
            violations=["HV-005_VOLTAGE_BELOW_MIN"],
            hardware_green=False,
            authorization=False,
            decision="FAIL",
            source="TEST_FIXTURE",
        )
        a, b, ok = replay_twice(rec)
        assert ok is True
        assert a == b
        assert rec.authorization is False
