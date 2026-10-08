"""Physical component bind tests — software fixtures only.

PHYSICAL_TEST = NOT_EXECUTED
HARDWARE_GREEN ≠ AUTHORIZATION
BIOMETRIC MATCH ≠ HUMAN AUTHORITY
"""
from __future__ import annotations

from swi_v3.hardware import (
    ComponentType,
    ComponentPhase,
    ConformanceStatus,
    PhysicalComponentChecker,
    PhysicalDeviceAdapter,
    TemporalHardwareValidator,
    WorkflowScopeLock,
    HardwareBindInterface,
    ComponentSpec,
    Measurement,
    PortState,
)
from swi_v3.hardware.fixtures import (
    PHYSICAL_DEVICE_TEST_STATUS,
    HARDWARE_EVIDENCE_TO_SEAL,
)
from swi_v3.runtime.engine import RuntimeEngine


def _ok_mic(device="dev-1"):
    return PhysicalDeviceAdapter().fixture_observation(
        ComponentType.MICROPHONE,
        component_id="mic-0",
        device_id=device,
        identity="mic-0",
    )


def _ok_cam(device="dev-1"):
    return PhysicalDeviceAdapter().fixture_observation(
        ComponentType.CAMERA,
        component_id="cam-0",
        device_id=device,
        identity="cam-0",
    )


def _ok_fp(device="dev-1", match=None):
    return PhysicalDeviceAdapter().fixture_observation(
        ComponentType.FINGERPRINT,
        component_id="fp-0",
        device_id=device,
        identity="fp-0",
        biometric_match=match,
    )


def _ok_accel(device="dev-1"):
    return PhysicalDeviceAdapter().fixture_observation(
        ComponentType.SENSOR,
        component_id="accel-0",
        device_id=device,
        identity="accel-0",
        sensor_subtype="accelerometer",
    )


class TestPhysicalComponentChecker:
    def test_microphone_conformant_fixture(self):
        r = PhysicalComponentChecker().check_observation(_ok_mic())
        assert r.ok is True
        assert r.conformance == ConformanceStatus.HARDWARE_CONFORMANT
        assert r.authorization is False

    def test_microphone_missing_blocks(self):
        obs = PhysicalDeviceAdapter().fixture_observation(
            ComponentType.MICROPHONE,
            component_id="mic-0",
            device_id="dev-1",
            available=False,
            required=True,
        )
        r = PhysicalComponentChecker().check_observation(obs)
        assert r.ok is False
        assert "HV-041_MICROPHONE_MISSING" in r.reason_codes

    def test_camera_missing_blocks(self):
        obs = PhysicalDeviceAdapter().fixture_observation(
            ComponentType.CAMERA,
            component_id="cam-0",
            device_id="dev-1",
            available=False,
        )
        r = PhysicalComponentChecker().check_observation(obs)
        assert r.ok is False
        assert "HV-042_CAMERA_MISSING" in r.reason_codes

    def test_fingerprint_missing_blocks(self):
        obs = PhysicalDeviceAdapter().fixture_observation(
            ComponentType.FINGERPRINT,
            component_id="fp-0",
            device_id="dev-1",
            available=False,
        )
        r = PhysicalComponentChecker().check_observation(obs)
        assert r.ok is False
        assert "HV-043_FINGERPRINT_MISSING" in r.reason_codes

    def test_fingerprint_match_is_not_authority(self):
        r = PhysicalComponentChecker().check_observation(_ok_fp(match=True))
        assert r.ok is True
        assert r.authorization is False
        assert r.observation.biometric_match is True

    def test_stale_sensor_blocks(self):
        obs = PhysicalDeviceAdapter().fixture_observation(
            ComponentType.SENSOR,
            component_id="gyro-0",
            device_id="dev-1",
            freshness_ok=False,
            sensor_subtype="gyroscope",
        )
        r = PhysicalComponentChecker().check_observation(obs)
        assert r.ok is False
        assert "HV-012_SENSOR_STALE" in r.reason_codes

    def test_identity_mismatch(self):
        obs = _ok_mic()
        r = PhysicalComponentChecker().check_observation(
            obs, expected_identity="mic-OTHER"
        )
        assert r.ok is False
        assert "HV-003_IDENTITY_MISMATCH" in r.reason_codes

    def test_permission_denied(self):
        obs = PhysicalDeviceAdapter().fixture_observation(
            ComponentType.CAMERA,
            component_id="cam-0",
            device_id="dev-1",
            permission_observable=False,
        )
        r = PhysicalComponentChecker().check_observation(obs)
        assert r.ok is False
        assert "HV-044_PERMISSION_NOT_GRANTED" in r.reason_codes

    def test_invalid_calibration(self):
        obs = PhysicalDeviceAdapter().fixture_observation(
            ComponentType.SENSOR,
            component_id="baro-0",
            device_id="dev-1",
            calibration_state="INVALID",
            sensor_subtype="barometer",
        )
        r = PhysicalComponentChecker().check_observation(obs)
        assert r.ok is False
        assert "HV-013_CALIBRATION_INVALID" in r.reason_codes


class TestScopeLockPhysical:
    def test_fingerprint_appearing_mid_flow_rejected(self):
        scope = WorkflowScopeLock("wf-phys-1")
        scope.start({"mic-0", "cam-0", "accel-0"})
        checker = PhysicalComponentChecker()
        # fingerprint not in B0
        result = checker.evaluate_set(
            [_ok_mic(), _ok_cam(), _ok_accel(), _ok_fp()],
            scope=scope,
        )
        assert result.hardware_green is False
        assert "HV-035_UNBOUND_HARDWARE_REJECTED" in result.reason_codes
        assert result.authorization is False

    def test_microphone_appearing_mid_flow_rejected(self):
        scope = WorkflowScopeLock("wf-phys-2")
        scope.start({"cam-0"})
        result = PhysicalComponentChecker().evaluate_set(
            [_ok_cam(), _ok_mic()],
            scope=scope,
        )
        assert result.hardware_green is False
        assert "HV-035_UNBOUND_HARDWARE_REJECTED" in result.reason_codes


class TestTemporalPhases:
    def test_before_during_after_fixture_sequence(self):
        tv = TemporalHardwareValidator()
        base = [_ok_mic(), _ok_cam(), _ok_accel()]
        seq = tv.evaluate_sequence(pre=base, during=base, post=base)
        assert seq["all_phases_conformant"] is True
        assert seq["authorization"] is False

    def test_during_disappearance_fails(self):
        tv = TemporalHardwareValidator()
        pre = [_ok_mic()]
        during = [
            PhysicalDeviceAdapter().fixture_observation(
                ComponentType.MICROPHONE,
                component_id="mic-0",
                device_id="dev-1",
                available=False,
            )
        ]
        post = [_ok_mic()]
        seq = tv.evaluate_sequence(pre=pre, during=during, post=post)
        assert seq["during"]["hardware_green"] is False
        assert seq["all_phases_conformant"] is False


class TestAdapterBoundary:
    def test_physical_adapter_not_implemented(self):
        ad = PhysicalDeviceAdapter()
        assert ad.ADAPTER_STATUS == "NOT_IMPLEMENTED"
        assert ad.PHYSICAL_ANDROID_SENSOR_ADAPTER == "NOT_IMPLEMENTED"
        obs = ad.acquire(ComponentType.MICROPHONE, component_id="mic-0", device_id="dev-1")
        assert obs.available is False
        assert obs.source == "UNKNOWN"

    def test_physical_test_status_not_executed(self):
        assert PHYSICAL_DEVICE_TEST_STATUS == "NOT_EXECUTED"
        assert HARDWARE_EVIDENCE_TO_SEAL == "NOT_IMPLEMENTED"


class TestNoAuthorizationEscalation:
    def test_component_pass_does_not_authorize_via_runtime(self):
        engine = RuntimeEngine()
        bind = PhysicalComponentChecker().evaluate_set([_ok_mic(), _ok_cam(), _ok_fp(match=True)])
        assert bind.hardware_green is True
        assert bind.authorization is False
        out = engine.observe_and_gate(
            hardware_id="dev-1",
            sensor_id="mic-0",
            value=0.0,
            context={},
            gate_state={
                "flow_bound": True,
                "runtime_match": True,
                "human_authority_bound": False,
                "authorization_valid": False,
            },
            hardware_bind=bind,
        )
        assert out["authorization"] is False
        assert out.get("note") == "HARDWARE_GREEN ≠ AUTHORIZATION"

    def test_existing_bind_still_green_not_auth(self):
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
