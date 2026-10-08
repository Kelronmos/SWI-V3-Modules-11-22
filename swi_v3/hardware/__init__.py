"""Hardware/environment specification interface.

HARDWARE_GREEN ≠ AUTHORIZATION
SENSOR_PASS ≠ AUTHORIZATION
CAPABILITY ≠ PERMISSION
BIOMETRIC MATCH ≠ HUMAN AUTHORITY
PHYSICAL COMPONENT PASS ≠ AUTHORIZATION
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
from .components import (
    ComponentType,
    ComponentPhase,
    ConformanceStatus,
    PhysicalComponentObservation,
    ComponentCheckResult,
    PhysicalComponentChecker,
    observations_to_present,
    observations_to_specs,
)
from .adapters import (
    PhysicalDeviceAdapter,
    ANDROID_SENSOR_COMMAND,
    ANDROID_CAMERA_COMMAND,
    ANDROID_MIC_COMMAND,
    ANDROID_BIOMETRIC_COMMAND,
    PHYSICAL_SENSOR_TEST,
)
from .phases import TemporalHardwareValidator, PhaseEvaluation

__all__ = [
    "ComponentSpec",
    "Measurement",
    "PortState",
    "SpecCheckResult",
    "HardwareBindResult",
    "SpecChecker",
    "HardwareBindInterface",
    "WorkflowScopeLock",
    "ComponentType",
    "ComponentPhase",
    "ConformanceStatus",
    "PhysicalComponentObservation",
    "ComponentCheckResult",
    "PhysicalComponentChecker",
    "observations_to_present",
    "observations_to_specs",
    "PhysicalDeviceAdapter",
    "ANDROID_SENSOR_COMMAND",
    "ANDROID_CAMERA_COMMAND",
    "ANDROID_MIC_COMMAND",
    "ANDROID_BIOMETRIC_COMMAND",
    "PHYSICAL_SENSOR_TEST",
    "TemporalHardwareValidator",
    "PhaseEvaluation",
]
