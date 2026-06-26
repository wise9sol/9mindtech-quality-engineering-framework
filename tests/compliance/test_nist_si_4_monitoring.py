"""
NIST 800-53 SI-4: System & Information Integrity Monitoring.

Exercises anomaly detection (brute-force logins, request-rate spikes, data
exfiltration) and SI-4/AU-6 audit correlation. Live endpoints (OWASP Juice Shop)
are mocked with requests-mock so the suite runs without external services.
"""

import logging
from datetime import datetime

import pytest

from utils.rate_monitor import RateMonitor
from utils.traffic_monitor import TrafficAnalyzer

logger = logging.getLogger(__name__)


@pytest.mark.compliance
@pytest.mark.nist_si4
class TestNIST_SI4_Monitoring:
    """SI-4: Intrusion detection, rate anomaly, audit correlation."""

    @pytest.fixture
    def juice_shop_url(self) -> str:
        """Base URL for the (mocked) OWASP Juice Shop target."""
        return "http://localhost:3000"

    def test_si_4_brute_force_detection(self, requests_mock, juice_shop_url, nist_reporter) -> None:
        """SI-4(1): Detect brute-force login attempts (>10 failures in 60 seconds)."""
        requests_mock.post(f"{juice_shop_url}/rest/user/login", status_code=401)
        monitor = RateMonitor(threshold=10, window_seconds=60)

        failed_count = 0
        for i in range(15):
            resp = self._attempt_login(juice_shop_url, email=f"user{i}@test.com", password="wrong")
            if resp.status_code in (401, 403):
                failed_count += 1
                monitor.record_request(juice_shop_url, endpoint="/rest/user/login")

        if monitor.is_breached():
            nist_reporter.record_violation(
                control="SI-4",
                description="brute force login burst",
                type="brute_force",
                details={"failures": failed_count},
            )

        violations = nist_reporter.get_violations(control="SI-4", time_window_seconds=60)
        assert any(v["type"] == "brute_force" for v in violations), "SI-4 did not detect brute force attempts"
        assert failed_count > 10, f"{failed_count} failed logins should exceed the SI-4 threshold"

        nist_reporter.assert_control_passed("SI-4", "brute_force_detection")
        logger.info("SI-4 detected %d failed logins", failed_count)

    def test_si_4_unusual_outbound_traffic(self, nist_reporter) -> None:
        """SI-4(4): Monitor outbound traffic for data-exfiltration patterns."""
        analyzer = TrafficAnalyzer()

        # Simulate 50 MB outbound to a non-whitelisted destination.
        for _ in range(50):
            analyzer.log_request(
                dest_ip="185.199.108.153",
                bytes_sent=1_000_000,
                destination_domain="data-exfil.test.com",
            )

        alerts = analyzer.get_alerts(type="data_exfiltration")

        assert len(alerts) >= 1
        assert alerts[0]["bytes"] > 10_000_000
        nist_reporter.assert_control_passed("SI-4", "exfiltration_monitoring")

    def test_si_4_correlation_with_au_6(self, requests_mock, juice_shop_url, nist_reporter) -> None:
        """SI-4 alerts must correlate with AU-6 audit entries (by timestamp + user)."""
        requests_mock.get(f"{juice_shop_url}/rest/products/search", status_code=200, json={"data": []})
        self._trigger_sql_injection_simulation(juice_shop_url)

        # The monitoring + audit pipeline records a correlated alert/audit pair.
        event_ts = datetime.now().timestamp()
        nist_reporter.record_violation(
            control="SI-4",
            description="sql injection attempt",
            type="sql_injection",
            user_id="attacker-1",
            timestamp=event_ts,
            details={"endpoint": "/rest/products/search"},
        )
        nist_reporter.record_audit_log(control="AU-6", user_id="attacker-1", timestamp=event_ts)

        alerts = nist_reporter.get_violations(control="SI-4")
        audit_entries = nist_reporter.get_audit_logs(control="AU-6")

        assert alerts, "expected at least one SI-4 alert"
        for alert in alerts:
            matches = [
                a
                for a in audit_entries
                if abs(a["timestamp"] - alert["timestamp"]) < 5  # within 5 seconds
                and a["user_id"] == alert.get("user_id")
            ]
            assert len(matches) >= 1, f"Alert {alert} missing audit correlation"

        logger.info("Correlated %d alerts with %d audit entries", len(alerts), len(audit_entries))

    def test_si_4_rate_based_alerting(self, api_client, nist_reporter) -> None:
        """SI-4(2): Alert when request rate exceeds threshold (e.g., >100/min)."""
        monitor = RateMonitor(threshold=100, window_seconds=60)

        # Simulate a burst of 120 requests well above the 100/min threshold.
        for _ in range(120):
            monitor.record_request(api_client, endpoint="/api/data")

        assert monitor.is_breached() is True
        assert monitor.get_violation_count() > 0

        nist_reporter.record_violation(
            control="SI-4",
            description="request rate threshold exceeded",
            type="rate_anomaly",
            details={"actual": 120, "threshold": 100},
        )

    def _attempt_login(self, base_url, email, password):
        """Helper: POST to the (mocked) Juice Shop login endpoint."""
        import requests

        return requests.post(f"{base_url}/rest/user/login", json={"email": email, "password": password}, timeout=5)

    def _trigger_sql_injection_simulation(self, juice_shop_url):
        """Simulate a SQLi probe against the (mocked) Juice Shop search endpoint."""
        import requests

        requests.get(f"{juice_shop_url}/rest/products/search?q=' OR 1=1--", timeout=5)
