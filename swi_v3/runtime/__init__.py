"""SWI V3 executable runtime boundary.

Implements execution gate, observation path, and durable ledger machinery.
Does NOT authorize, seal, prove, or production-authorize SWI.
"""

from .fail_closed import FailClosedRuntime, Decision
from .degraded import DegradedPathRuntime
from .gate import ExecutionGate, GateResult
from .observation import ObservationPipeline, Observation
from .ledger import DurableLedger, LedgerEvent
from .engine import RuntimeEngine

__all__ = [
    "FailClosedRuntime",
    "Decision",
    "DegradedPathRuntime",
    "ExecutionGate",
    "GateResult",
    "ObservationPipeline",
    "Observation",
    "DurableLedger",
    "LedgerEvent",
    "RuntimeEngine",
]
