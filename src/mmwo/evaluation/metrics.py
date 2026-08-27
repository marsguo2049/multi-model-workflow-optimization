from dataclasses import dataclass


@dataclass(frozen=True)
class MetricDefinition:
    name: str
    description: str
    higher_is_better: bool = True
    minimum: float | None = None
    maximum: float | None = None
