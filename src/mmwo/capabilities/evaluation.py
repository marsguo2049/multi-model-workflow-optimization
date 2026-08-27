from dataclasses import dataclass, field
from typing import Any, Protocol

from .base import ModelCall


@dataclass(frozen=True)
class EvaluationRequest:
    task_id: str
    capability_under_test: str
    output_reference: str
    expected: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EvaluationResponse:
    accepted: bool
    scores: dict[str, float]
    notes: str
    call: ModelCall


class EvaluationProvider(Protocol):
    def evaluate(self, request: EvaluationRequest) -> EvaluationResponse: ...
