from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class Capability(str, Enum):
    TEXT_GENERATION = "text_generation"
    PROMPT_GENERATION = "prompt_generation"
    IMAGE_GENERATION = "image_generation"
    VIDEO_GENERATION = "video_generation"
    EVALUATION = "evaluation"


class CallStatus(str, Enum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(frozen=True)
class ModelCall:
    call_id: str
    task_id: str
    capability: Capability
    provider: str
    model: str | None
    configuration: dict[str, Any]
    input_references: list[str]
    output_references: list[str]
    status: CallStatus
    runtime_ms: float
    seed: int | None = None
    cost_usd: float | None = None
    compute: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["capability"] = self.capability.value
        data["status"] = self.status.value
        return data
