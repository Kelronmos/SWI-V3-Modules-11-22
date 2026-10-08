"""Runtime engine — observation, hardware bind, gate, ledger.

Does not manufacture authority or production authorization.
HARDWARE_GREEN ≠ AUTHORIZATION
"""
from __future__ import annotations

from typing import Any, Optional

from .gate import ExecutionGate, GateResult
from .observation import ObservationPipeline, Observation
from .ledger import DurableLedger

from swi_v3.hardware import HardwareBindInterface, HardwareBindResult
from swi_v3.hardware.models import ComponentSpec, Measurement, PortState
from swi_v3.hardware.scope_lock import WorkflowScopeLock


class RuntimeEngine:
    def __init__(self):
        self.gate = ExecutionGate()
        self.pipeline = ObservationPipeline()
        self.ledger = DurableLedger()
        self.hardware = HardwareBindInterface()

    def evaluate_hardware(
        self,
        *,
        specs: list[ComponentSpec],
        measurements: list[Measurement],
        present: dict[str, bool],
        ports: list[PortState],
        scope: Optional[WorkflowScopeLock] = None,
        discovered_components: Optional[set[str]] = None,
    ) -> HardwareBindResult:
        """Technical hardware/environment check. Never sets authorization."""
        result = self.hardware.evaluate(
            specs=specs,
            measurements=measurements,
            present=present,
            ports=ports,
            scope=scope,
            discovered_components=discovered_components,
        )
        self.ledger.append(
            "HARDWARE_CHECK",
            result.to_dict(),
        )
        # Refuse any attempt to treat green as authorization
        assert result.authorization is False
        return result

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
        hardware_bind: Optional[HardwareBindResult] = None,
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

        if hardware_bind is not None:
            self.ledger.append("HARDWARE_CHECK", hardware_bind.to_dict())
            if not hardware_bind.hardware_green:
                # Technical fail-closed signal into gate state; not authorization
                merged["hardware_green"] = False
                merged["hardware_bind_failed"] = True
                if hardware_bind.reason_codes:
                    merged["integrity_compromised"] = True
            else:
                merged["hardware_green"] = True
            # Never inject authorization from hardware
            merged.pop("authorization_from_hardware", None)

        if obs is not None:
            self.ledger.append("OBSERVE", obs.to_dict())
        else:
            self.ledger.append("OBSERVE", {"errors": errors})

        self.ledger.append("VALIDATE", {"gate_state_keys": sorted(merged.keys())})

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
            "permitted": result.permitted,
            "hardware_bind": hardware_bind.to_dict() if hardware_bind else None,
            "authorization": False if hardware_bind else gate_state.get("authorization_valid", False),
            "ledger_tail": self.ledger.entries[-5:] if hasattr(self.ledger, "entries") else None,
            "note": "HARDWARE_GREEN ≠ AUTHORIZATION",
        }
