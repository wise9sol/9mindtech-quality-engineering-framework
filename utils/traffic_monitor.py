"""
Outbound traffic analysis for NIST 800-53 SI-4(4) data-exfiltration monitoring.

Aggregates logged outbound requests per destination and raises alerts when the
cumulative volume to a single non-whitelisted destination crosses a byte
threshold. Pure in-memory analysis — no network access.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List

# Cumulative outbound bytes to one non-whitelisted destination before alerting.
DEFAULT_EXFIL_THRESHOLD_BYTES = 10_000_000


@dataclass
class _OutboundRequest:
    """A single recorded outbound request."""

    dest_ip: str
    bytes_sent: int
    destination_domain: str


@dataclass
class TrafficAnalyzer:
    """Detect data-exfiltration patterns in logged outbound traffic (NIST SI-4(4))."""

    exfil_threshold_bytes: int = DEFAULT_EXFIL_THRESHOLD_BYTES
    whitelisted_domains: frozenset[str] = frozenset()
    _requests: List[_OutboundRequest] = field(default_factory=list)

    def log_request(self, dest_ip: str, bytes_sent: int, destination_domain: str) -> None:
        """Record a single outbound request for later analysis."""
        self._requests.append(_OutboundRequest(dest_ip, int(bytes_sent), destination_domain))

    def get_alerts(self, type: str = "data_exfiltration") -> List[Dict[str, object]]:
        """Return exfiltration alerts for non-whitelisted destinations over threshold.

        Args:
            type: Alert category to return. Only ``"data_exfiltration"`` is produced.

        Returns:
            Alerts (highest volume first), each with ``type``, ``destination_domain``,
            ``dest_ip`` and total ``bytes``.
        """
        if type != "data_exfiltration":
            return []

        totals: Dict[str, int] = defaultdict(int)
        ips: Dict[str, str] = {}
        for entry in self._requests:
            if entry.destination_domain in self.whitelisted_domains:
                continue
            totals[entry.destination_domain] += entry.bytes_sent
            ips[entry.destination_domain] = entry.dest_ip

        flagged = [(domain, total) for domain, total in totals.items() if total > self.exfil_threshold_bytes]
        flagged.sort(key=lambda item: item[1], reverse=True)
        return [
            {
                "type": "data_exfiltration",
                "destination_domain": domain,
                "dest_ip": ips[domain],
                "bytes": total,
            }
            for domain, total in flagged
        ]
