from dataclasses import dataclass, field
from typing import Any, Protocol

from .base import ModelCall


@dataclass(frozen=True)
class ImageGenerationRequest:
    task_id: str
    prompt: str
    seed: int | None = None
    input_references: list[str] = field(default_factory=list)
    configuration: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ImageGenerationResponse:
    output_reference: str
    call: ModelCall


class ImageGenerationProvider(Protocol):
    def generate_image(self, request: ImageGenerationRequest) -> ImageGenerationResponse: ...
