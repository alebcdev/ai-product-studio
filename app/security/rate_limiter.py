from __future__ import annotations
from math import ceil
from collections import defaultdict, deque
from collections.abc import Callable
from threading import Lock
from time import monotonic


class RateLimiter:
    """Limit requests per client using an in-memory sliding time window.

    State is local to this process and resets when the application restarts.
    Deployments with multiple workers maintain independent limits, and clients
    behind the same proxy may share a visible client address.
    """

    def __init__(
        self,
        max_requests: int,
        window_seconds: float,
        clock: Callable[[], float] = monotonic,
    ):
        if max_requests < 1:
            raise ValueError("max_requests must be greater than zero")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be greater than zero")

        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._clock = clock
        self._requests: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def check(self, client_id: str) -> tuple[bool, int]:
        """Record a request and return ``(allowed, retry_after_seconds)``."""
        now = self._clock()
        cutoff = now - self.window_seconds

        with self._lock:
            for stored_client_id, timestamps in list(self._requests.items()):
                while timestamps and timestamps[0] <= cutoff:
                    timestamps.popleft()
                if not timestamps:
                    del self._requests[stored_client_id]

            timestamps = self._requests[client_id]

            if len(timestamps) >= self.max_requests:
                retry_after = max(
                    1,
                    ceil(timestamps[0] + self.window_seconds - now)
                    )
                return False, retry_after

            timestamps.append(now)
            return True, 0

    def reset(self) -> None:
        """Clear all in-memory request state."""
        with self._lock:
            self._requests.clear()
