"""Deterministic serialization and hashing for seal identity."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(obj: Any) -> str:
    """Deterministic JSON: sorted keys, no insignificant whitespace."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(obj: Any) -> str:
    """SHA-256 hex digest of the canonical JSON of obj."""
    payload = canonical_json(obj).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
