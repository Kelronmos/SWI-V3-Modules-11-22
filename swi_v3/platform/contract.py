"""Platform contract — describes environment; does not authorize."""
from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet


@dataclass(frozen=True)
class PlatformInfo:
    """Environment description only. Not authority. Not authorization."""

    name: str
    version: str
    architecture: str
    capabilities: FrozenSet[str]

    def has_capability(self, capability: str) -> bool:
        return capability in self.capabilities
