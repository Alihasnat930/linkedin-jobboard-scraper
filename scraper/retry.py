import functools
import time
from typing import Callable, Iterable, TypeVar

F = TypeVar("F", bound=Callable)


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    backoff_factor: float = 2.0,
    retryable_exceptions: Iterable[type[BaseException]] = (Exception,),
):
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc: BaseException | None = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as exc:  # type: ignore[misc]
                    last_exc = exc
                    if attempt >= max_retries:
                        raise
                    delay = base_delay * (backoff_factor ** attempt)
                    time.sleep(delay)
            if last_exc is not None:
                raise last_exc
            raise RuntimeError("Retry loop exited without a result")

        return wrapper  # type: ignore[return-value]

    return decorator
