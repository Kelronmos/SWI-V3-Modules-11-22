"""Durable validation ledger (in-process authoritative record for this runtime).

Conversation memory is not the authoritative record.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Optional
import uuid

EVENT_SEQUENCE = [
    "RECEIVE",
    "IDENTIFY",
    "OBSERVE",
    "VALIDATE",
    "BIND",
    "AUTHORIZE",
    "EXECUTE",
    "MONITOR",
    "REVALIDATE",
    "RECONCILE",
    "CLOSE",
]


@dataclass
class LedgerEvent:
    event_id: str
    event_type: str
    timestamp: str
    payload: dict
    mode: str = "NORMAL"  # NORMAL | DEGRADED
    degraded_mode_id: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


class DurableLedger:
    """Append-only in-memory ledger for runtime evidence.

    Not a distributed store; establishes the runtime boundary API.
    """

    def __init__(self):
        self._events: list[LedgerEvent] = []

    def append(
        self,
        event_type: str,
        payload: dict,
        *,
        mode: str = "NORMAL",
        degraded_mode_id: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> LedgerEvent:
        if event_type not in EVENT_SEQUENCE and event_type not in {
            "FAIL_CLOSED",
            "BLOCK",
            "GATE_DECISION",
            "SEAL_VERIFY",
        }:
            # allow extended operational events beyond the core sequence
            pass

        if timestamp is None:
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Enforce: do not claim NORMAL when degraded
        if mode == "DEGRADED":
            payload = dict(payload)
            payload["claimed_normal"] = False

        ev = LedgerEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            timestamp=timestamp,
            payload=dict(payload),
            mode=mode,
            degraded_mode_id=degraded_mode_id,
        )
        self._events.append(ev)
        return ev

    def events(self) -> list[LedgerEvent]:
        return list(self._events)

    def by_type(self, event_type: str) -> list[LedgerEvent]:
        return [e for e in self._events if e.event_type == event_type]

    def last(self) -> Optional[LedgerEvent]:
        return self._events[-1] if self._events else None

    def to_list(self) -> list[dict]:
        return [e.to_dict() for e in self._events]
