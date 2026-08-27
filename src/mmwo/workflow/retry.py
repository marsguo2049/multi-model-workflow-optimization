from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")


class RetryExhaustedError(RuntimeError):
    pass


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 2

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")


def run_with_retry(operation: Callable[[], T], policy: RetryPolicy, retry_on: tuple[type[Exception], ...] = (Exception,)) -> T:
    last_error: Exception | None = None
    for _ in range(policy.max_attempts):
        try:
            return operation()
        except retry_on as exc:
            last_error = exc
    raise RetryExhaustedError(f"Operation failed after {policy.max_attempts} attempts") from last_error
