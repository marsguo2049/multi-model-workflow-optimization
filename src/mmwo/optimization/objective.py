from dataclasses import dataclass


@dataclass(frozen=True)
class ObjectiveWeights:
    cost: float = 1.0
    latency: float = 1.0
    resources: float = 1.0


def scalarized_objective(quality: float, cost: float, latency: float, resources: float, weights: ObjectiveWeights) -> float:
    """Transparent baseline only; inputs must come from real measurements."""
    return quality - weights.cost * cost - weights.latency * latency - weights.resources * resources
