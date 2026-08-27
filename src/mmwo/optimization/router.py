from typing import Sequence, TypeVar

T = TypeVar("T")


class FirstAvailableRouter:
    """Deterministic baseline; not an optimizer."""

    def choose(self, candidates: Sequence[T]) -> T:
        if not candidates:
            raise LookupError("No provider candidates are available")
        return candidates[0]
