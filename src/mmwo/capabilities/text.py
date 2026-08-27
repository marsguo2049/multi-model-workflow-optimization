from dataclasses import dataclass, field
from typing import Any, Protocol

from .base import ModelCall


@dataclass(frozen=True)
class TextRequest:
    task_id: str
    prompt: str
    configuration: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TextResponse:
    text: str
    call: ModelCall


class TextGenerationProvider(Protocol):
    def generate_text(self, request: TextRequest) -> TextResponse: ...


@dataclass(frozen=True)
class PromptRequest:
    task_id: str
    story: str
    shot_index: int
    shot_description: str
    configuration: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PromptResponse:
    prompt: str
    call: ModelCall


class PromptGenerationProvider(Protocol):
    def generate_prompt(self, request: PromptRequest) -> PromptResponse: ...
