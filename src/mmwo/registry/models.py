from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ModelConfiguration:
    id: str
    provider: str
    model: str | None
    parameters: dict[str, Any] = field(default_factory=dict)
    resource_profile: dict[str, Any] = field(default_factory=dict)
