"""Hardware/environment specification interface.

HARDWARE_GREEN ≠ AUTHORIZATION
SENSOR_PASS ≠ AUTHORIZATION
CAPABILITY ≠ PERMISSION
"""
from .models import (
    ComponentSpec,
    Measurement,
    PortState,
    SpecCheckResult,
    HardwareBindResult,
)
from .spec_check import SpecChecker
from .bind import HardwareBindInterface
from .scope_lock import WorkflowScopeLock

__all__ = [
    "ComponentSpec",
    "Measurement",
    "PortState",
    "SpecCheckResult",
    "HardwareBindResult",
    "SpecChecker",
    "HardwareBindInterface",
    "WorkflowScopeLock",
]
