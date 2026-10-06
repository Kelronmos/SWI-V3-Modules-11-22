"""Executable runtime boundary tests.

Runtime mechanism tested ≠ SWI proven / sealed / authorized / production-authorized.
"""
from __future__ import annotations

import pytest

from swi_v3.runtime import (
    RuntimeEngine,
    ExecutionGate,
    FailClosedRuntime,
    Decision,
    ObservationPipeline,
    DurableLedger,
)


def base_ok_state(**overrides):
    state = {
        "flow_bind": True,
        "runtime_match": True,
        "human_authority_bound": True,
        "authorization_valid": True,
    }
    state.update(overrides)
    return state


class TestExecutionGateRuntime:
    def test_all_conjuncts_permit_normal(self):
        gate = ExecutionGate()
        r = gate.evaluate(base_ok_state())
        assert r.permitted is True
        assert r.mode == "NORMAL"

    def test_missing_authorization_blocks(self):
        gate = ExecutionGate()
        r = gate.evaluate(base_ok_state(authorization_valid=False))
        assert r.permitted is False
        assert r.mode == "BLOCKED"
        assert "AUTHORIZATION_INVALID" in r.reason_codes

    def test_missing_authority_blocks(self):
        gate = ExecutionGate()
        r = gate.evaluate(base_ok_state(human_authority_bound=False))
        assert r.permitted is False

    def test_runtime_match_alone_does_not_permit(self):
        gate = ExecutionGate()
        r = gate.evaluate({"runtime_match": True})
        assert r.permitted is False

    def test_integrity_failure_blocks(self):
        gate = ExecutionGate()
        r = gate.evaluate(base_ok_state(integrity_failure=True))
        assert r.permitted is False
        assert r.decision == Decision.BLOCK.value

    def test_material_change_revalidates(self):
        gate = ExecutionGate()
        r = gate.evaluate(base_ok_state(material_change_without_revalidation=True))
        assert r.permitted is False
        assert r.mode == "REVALIDATE"

    def test_missing_component_no_degraded_blocks(self):
        gate = ExecutionGate()
        r = gate.evaluate(
            base_ok_state(
                required_component_missing=True,
                valid_degraded_path_defined=False,
            )
        )
        assert r.permitted is False
        assert r.mode == "BLOCKED"

    def test_degraded_path_all_conditions_permits_degraded(self):
        gate = ExecutionGate()
        r = gate.evaluate(
            {
                "required_component_missing": True,
                "valid_degraded_path_defined": True,
                "degraded_conditions_satisfied": True,
                "human_authority_bound": True,
                "authorization_valid": True,
                "degraded_mode_id": "D-A-001",
            }
        )
        assert r.permitted is True
        assert r.mode == "DEGRADED"
        assert r.degraded_mode_id == "D-A-001"

    def test_degraded_without_authorization_blocks(self):
        gate = ExecutionGate()
        r = gate.evaluate(
            {
                "required_component_missing": True,
                "valid_degraded_path_defined": True,
                "degraded_conditions_satisfied": True,
                "human_authority_bound": True,
                "authorization_valid": False,
            }
        )
        assert r.permitted is False


class TestObservationPipeline:
    def test_successful_observation(self):
        pipe = ObservationPipeline()
        obs, errors = pipe.observe(
            hardware_id="HW-1",
            sensor_id="S-1",
            value=42,
            context={"workflow": "W1"},
        )
        assert errors == []
        assert obs is not None
        assert obs.sensor_id == "S-1"

    def test_missing_hardware_errors(self):
        pipe = ObservationPipeline()
        obs, errors = pipe.observe(
            hardware_id="HW-1",
            sensor_id="S-1",
            value=1,
            context={},
            hardware_available=False,
        )
        assert obs is None
        assert "HARDWARE_UNAVAILABLE" in errors

    def test_observation_is_not_authority(self):
        pipe = ObservationPipeline()
        obs, _ = pipe.observe(
            hardware_id="HW-1", sensor_id="S-1", value=1, context={}
        )
        assert obs is not None
        # observation object carries no authorization field by design
        assert not hasattr(obs, "authorization") or getattr(obs, "authorization", None) is None

    def test_stale_maps_to_gate_state(self):
        pipe = ObservationPipeline()
        obs, errors = pipe.observe(
            hardware_id="HW-1",
            sensor_id="S-1",
            value=1,
            context={},
            stale=True,
        )
        state = pipe.to_gate_state(obs, errors)
        assert state.get("required_evidence_stale") is True


class TestDurableLedger:
    def test_append_and_read(self):
        led = DurableLedger()
        ev = led.append("RECEIVE", {"x": 1})
        assert led.last() is ev
        assert len(led.events()) == 1

    def test_degraded_not_claimed_normal(self):
        led = DurableLedger()
        ev = led.append("EXECUTE", {"action": "a"}, mode="DEGRADED", degraded_mode_id="D1")
        assert ev.mode == "DEGRADED"
        assert ev.payload.get("claimed_normal") is False

    def test_conversation_memory_is_not_ledger(self):
        led = DurableLedger()
        conversation = {"role": "temporary"}
        assert led.to_list() != [conversation]


class TestRuntimeEngineIntegration:
    def test_happy_path_executes(self):
        eng = RuntimeEngine()
        out = eng.observe_and_gate(
            hardware_id="HW-1",
            sensor_id="S-1",
            value=10,
            context={"workflow": "W1"},
            gate_state=base_ok_state(),
        )
        assert out["gate"]["permitted"] is True
        assert out["gate"]["mode"] == "NORMAL"
        types = [e.event_type for e in eng.ledger.events()]
        assert "EXECUTE" in types

    def test_missing_sensor_blocks(self):
        eng = RuntimeEngine()
        out = eng.observe_and_gate(
            hardware_id="HW-1",
            sensor_id="",
            value=10,
            context={},
            gate_state=base_ok_state(),
            hardware_available=True,
        )
        assert out["gate"]["permitted"] is False

    def test_unauthorized_blocks_despite_observation(self):
        eng = RuntimeEngine()
        out = eng.observe_and_gate(
            hardware_id="HW-1",
            sensor_id="S-1",
            value=10,
            context={},
            gate_state=base_ok_state(authorization_valid=False),
        )
        assert out["gate"]["permitted"] is False
        types = [e.event_type for e in eng.ledger.events()]
        assert "BLOCK" in types
        assert "EXECUTE" not in types

    def test_runtime_does_not_set_production_authorized(self):
        eng = RuntimeEngine()
        out = eng.observe_and_gate(
            hardware_id="HW-1",
            sensor_id="S-1",
            value=1,
            context={},
            gate_state=base_ok_state(),
        )
        assert out["gate"]["permitted"] is True
        # Engine must not invent production authorization
        assert "PRODUCTION_AUTHORIZED" not in out
