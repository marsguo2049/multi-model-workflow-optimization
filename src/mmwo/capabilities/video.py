from dataclasses import dataclass, field
from typing import Any, Protocol

from .base import ModelCall


@dataclass(frozen=True)
class VideoGenerationRequest:
    task_id: str
    prompt: str
    start_image_reference: str
    end_image_reference: str | None = None
    seed: int | None = None
    configuration: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VideoGenerationResponse:
    output_reference: str
    call: ModelCall


class VideoGenerationProvider(Protocol):
    def generate_video(self, request: VideoGenerationRequest) -> VideoGenerationResponse: ...
