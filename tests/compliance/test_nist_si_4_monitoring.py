"""
NIST 800-53 SI-4: System & Information Integrity Monitoring
Tests: Framework must detect anomalous behavior (failed logins, rapid requests, data exfiltration)
Target: Your monitoring hooks + nist-validation-report/
"""

import pytest
import time
import json
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

# NOTE: `nist_reporter` is supplied by the fixture in conftest.py, which defines
# NISTReport as a fixture-local dataclass. There is no importable utils.nist_reporter
# module, and the previously-imported utils.security_monitor.SecurityMonitor was unused.
# Both module-level imports were removed so this module collects cleanly.


# Tracking: https://github.com/wise9sol/9mindtech-quality-engineering-framework/issues/2
# These tests collect cleanly but cannot run yet — they depend on unimplemented
# modules/fixtures (utils.traffic_monitor, utils.rate_monitor, an api_client fixture,
# an imported logger) and a local OWASP Juice Shop at localhost:3000. xfail keeps them
# visible without blocking CI; remove the markers once issue #2 is resolved.
_SI4_XFAIL_REASON = "Missing deps (utils.traffic_monitor/rate_monitor, api_client fixture, logger, local Juice Shop) — see issue #2"


@pytest.mark.xfail(reason=_SI4_XFAIL_REASON, run=False)
class TestNIST_SI4_Monitoring:
    """SI-4: Intrusion detection, rate anomaly, audit correlation"""

    @pytest.fixture
    def juice_shop_url(self):
        """OWASP Juice Shop (run locally: docker run -p 3000:3000 bkimminich/juice-shop)"""
        return "http://localhost:3000"

    def test_si_4_brute_force_detection(self, juice_shop_url, nist_reporter):
        """
        SI-4(1): Detect brute force login attempts (>10 failures in 60 seconds)
        """
        failed_count = 0
        start_time = time.time()

        # Simulate 15 rapid failed logins
        for i in range(15):
            resp = self._attempt_login(juice_shop_url, email=f"user{i}@test.com", password="wrong")
            if resp.status_code in [401, 403]:
                failed_count += 1
            time.sleep(0.5)  # realistic

        elapsed = time.time() - start_time
        rate = failed_count / elapsed if elapsed > 0 else 0

        # Your monitoring should flag this as SI-4 violation
        violations = nist_reporter.get_violations(control="SI-4", time_window_seconds=60)

        assert any(v["type"] == "brute_force" for v in violations), \
            "SI-4 did not detect brute force attempts"
        assert rate > 5, f"Failure rate {rate:.1f}/sec should trigger alert"

        nist_reporter.assert_control_passed("SI-4", "brute_force_detection")
        logger.info(f"SI-4 detected {failed_count} failures at {rate:.2f}/sec")

    def test_si_4_unusual_outbound_traffic(self, nist_reporter):
        """
        SI-4(4): Monitor outbound traffic for data exfiltration patterns
        """
        # Simulate large data transfer to unexpected domain
        from utils.traffic_monitor import TrafficAnalyzer  # your module

        analyzer = TrafficAnalyzer()

        # Simulate 50MB outbound to non-whitelisted IP
        for _ in range(50):
            analyzer.log_request(
                dest_ip="185.199.108.153",  # GitHub, suspiciously large
                bytes_sent=1_000_000,
                destination_domain="data-exfil.test.com"
            )

        alerts = analyzer.get_alerts(type="data_exfiltration")

        assert len(alerts) >= 1
        assert alerts[0]["bytes"] > 10_000_000
        nist_reporter.assert_control_passed("SI-4", "exfiltration_monitoring")

    def test_si_4_correlation_with_au_6(self, juice_shop_url, nist_reporter):
        """
        SI-4 data must correlate with AU-6 (Audit Review)
        Every security alert must have corresponding audit log entry
        """
        # Trigger an anomaly
        self._trigger_sql_injection_simulation(juice_shop_url)

        # Fetch SI-4 alerts and AU-6 audit logs
        alerts = nist_reporter.get_violations(control="SI-4")
        audit_entries = nist_reporter.get_audit_logs(control="AU-6")

        # Each alert should have a matching audit entry (by timestamp + user)
        for alert in alerts:
            matches = [a for a in audit_entries
                       if abs(a["timestamp"] - alert["timestamp"]) < 5  # within 5 seconds
                       and a["user_id"] == alert.get("user_id")]
            assert len(matches) >= 1, f"Alert {alert['id']} missing audit correlation"

        logger.info(f"Correlated {len(alerts)} alerts with {len(audit_entries)} audit entries")

    def test_si_4_rate_based_alerting(self, api_client):
        """
        SI-4(2): Alert when request rate exceeds threshold (e.g., >100/min)
        """
        from utils.rate_monitor import RateMonitor

        monitor = RateMonitor(threshold=100, window_seconds=60)

        # Simulate 120 requests in 30 seconds
        for _ in range(120):
            monitor.record_request(api_client, endpoint="/api/data")
            time.sleep(0.25)  # 30 seconds total

        assert monitor.is_breached() is True
        assert monitor.get_violation_count() > 0

        # Your NIST report should include this SI-4 violation
        nist_reporter.record_violation(
            control="SI-4",
            description="Rate threshold exceeded",
            details={"actual_rate": 240, "threshold": 100}
        )

    def _attempt_login(self, base_url, email, password):
        """Helper: real POST to Juice Shop login"""
        import requests
        return requests.post(
            f"{base_url}/rest/user/login",
            json={"email": email, "password": password},
            timeout=5
        )

    def _trigger_sql_injection_simulation(self, juice_shop_url):
        """Simulate SQLi attempt (Juice Shop is intentionally vulnerable)"""
        import requests
        # Known vulnerable endpoint in Juice Shop
        requests.get(
            f"{juice_shop_url}/rest/products/search?q=' OR 1=1--",
            timeout=5
        )