"""Runtime engine — composes observation, gate, and ledger.

Does not manufacture authority or production authorization.
"""
from __future__ import annotations

from typing import Any, Optional

from .gate import ExecutionGate, GateResult
from .observation import ObservationPipeline, Observation
from .ledger import DurableLedger


class RuntimeEngine:
    def __init__(self):
        self.gate = ExecutionGate()
        self.pipeline = ObservationPipeline()
        self.ledger = DurableLedger()

    def observe_and_gate(
        self,
        *,
        hardware_id: str,
        sensor_id: str,
        value: Any,
        context: dict,
        gate_state: dict,
        hardware_available: bool = True,
        hardware_capable: bool = True,
        integrity_ok: bool = True,
        stale: bool = False,
        timestamp: Optional[str] = None,
    ) -> dict:
        self.ledger.append("RECEIVE", {"hardware_id": hardware_id, "sensor_id": sensor_id})
        self.ledger.append("IDENTIFY", {"hardware_id": hardware_id, "sensor_id": sensor_id})

        obs, errors = self.pipeline.observe(
            hardware_id=hardware_id,
            sensor_id=sensor_id,
            value=value,
            context=context,
            hardware_available=hardware_available,
            hardware_capable=hardware_capable,
            integrity_ok=integrity_ok,
            stale=stale,
            timestamp=timestamp,
        )

        obs_state = self.pipeline.to_gate_state(obs, errors)
        merged = dict(gate_state)
        merged.update(obs_state)

        if obs is not None:
            self.ledger.append("OBSERVE", obs.to_dict())
        else:
            self.ledger.append("OBSERVE", {"errors": errors})

        self.ledger.append("VALIDATE", {"gate_state": {k: merged.get(k) for k in merged}})

        result = self.gate.evaluate(merged)

        self.ledger.append(
            "GATE_DECISION",
            result.to_dict(),
            mode=result.mode if result.mode in ("NORMAL", "DEGRADED") else "NORMAL",
            degraded_mode_id=result.degraded_mode_id,
        )

        if result.permitted:
            self.ledger.append(
                "EXECUTE",
                {"mode": result.mode},
                mode=result.mode if result.mode == "DEGRADED" else "NORMAL",
                degraded_mode_id=result.degraded_mode_id,
            )
        else:
            self.ledger.append("BLOCK", result.to_dict())

        return {
            "observation": obs.to_dict() if obs else None,
            "observation_errors": errors,
            "gate": result.to_dict(),
            "ledger_tail": self.ledger.last().to_dict() if self.ledger.last() else None,
        }
