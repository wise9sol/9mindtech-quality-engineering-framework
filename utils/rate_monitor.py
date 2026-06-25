"""
Request-rate monitoring for NIST 800-53 SI-4(2) rate-based alerting.

Tracks request arrival times in a sliding window and reports when the in-window
request count exceeds a configured threshold. Uses a monotonic clock for elapsed
measurement (never ``time.time()``), and never sleeps.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import List


@dataclass
class RateMonitor:
    """Sliding-window request-rate monitor (NIST SI-4(2))."""

    threshold: int
    window_seconds: float
    _events: List[float] = field(default_factory=list)

    def record_request(self, client: object, endpoint: str) -> None:
        """Record one request against the monitored client/endpoint.

        ``client`` and ``endpoint`` identify the traffic source; only the request's
        arrival time is needed for rate calculation.
        """
        self._events.append(time.monotonic())

    def _in_window(self) -> int:
        cutoff = time.monotonic() - self.window_seconds
        self._events = [ts for ts in self._events if ts >= cutoff]
        return len(self._events)

    def is_breached(self) -> bool:
        """Return True when the in-window request count exceeds the threshold."""
        return self._in_window() > self.threshold

    def get_violation_count(self) -> int:
        """Return how many in-window requests exceeded the threshold."""
        return max(0, self._in_window() - self.threshold)
