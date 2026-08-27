from dataclasses import dataclass, field
from typing import Any

from mmwo.capabilities import Capability


@dataclass(frozen=True)
class ProviderDescriptor:
    id: str
    capability: Capability
    provider: str
    model: str | None = None
    parameters: dict[str, Any] = field(default_factory=dict)
    resource_profile: dict[str, Any] = field(default_factory=dict)
