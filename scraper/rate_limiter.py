import time


class RateLimiter:
    def __init__(self, min_interval_seconds: float = 4.0):
        self.min_interval_seconds = max(float(min_interval_seconds), 0.5)
        self._last_call = 0.0

    def wait(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_call
        if elapsed < self.min_interval_seconds:
            time.sleep(self.min_interval_seconds - elapsed)
        self._last_call = time.monotonic()
