import pytest

from mmwo.workflow import RetryExhaustedError, RetryPolicy, run_with_retry


def test_retry_eventually_succeeds() -> None:
    attempts = 0

    def flaky() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("temporary")
        return "ok"

    assert run_with_retry(flaky, RetryPolicy(max_attempts=3)) == "ok"
    assert attempts == 3


def test_retry_reports_exhaustion() -> None:
    with pytest.raises(RetryExhaustedError):
        run_with_retry(lambda: (_ for _ in ()).throw(ValueError("no")), RetryPolicy(max_attempts=2))
