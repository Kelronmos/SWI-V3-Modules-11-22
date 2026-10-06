"""SWI V3 Seal mechanism.

STRUCTURED_SEAL ≠ RUNTIME_SEAL
SEAL ≠ AUTHORIZATION
SEAL ≠ PRODUCTION_READINESS

This package implements the machinery that can later determine whether a
specific state is sealable. It does not declare SWI sealed.
"""

from .canonical import canonical_json, digest
from .models import SealRecord, SealType, SealState, VerificationResult
from .structured import StructuredSealEngine
from .runtime import RuntimeSealEngine
from .verifier import SealVerifier
from .state_machine import SealStateMachine

__all__ = [
    "canonical_json",
    "digest",
    "SealRecord",
    "SealType",
    "SealState",
    "VerificationResult",
    "StructuredSealEngine",
    "RuntimeSealEngine",
    "SealVerifier",
    "SealStateMachine",
]
