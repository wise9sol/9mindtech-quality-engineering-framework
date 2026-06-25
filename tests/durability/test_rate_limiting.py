"""
Durability: API rate limiting & retry logic.

Target: requests session retry/backoff configuration (durability_api_client fixture).
NIST correlation: SI-4 (System & Information Integrity Monitoring).

These tests are network-free. The retry *policy* is asserted directly against the
mounted adapter; response handling is exercised with requests-mock. Note that
urllib3's status-based retry loop lives below ``HTTPAdapter.send`` (which requests-mock
replaces), so genuine retry-exhaustion can only be observed against a live server —
hence it is verified here by configuration, not by provoking a RetryError.
"""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest
from requests.adapters import HTTPAdapter

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.durability, pytest.mark.slow]

_GET_URL = "https://httpbin.org/get"
_HTML_URL = "https://httpbin.org/html"


class TestRateLimitingDurability:
    """Stress test the API client's retry configuration and response handling."""

    def test_durability_client_mounts_retry_adapter(self, durability_api_client) -> None:
        """The durability client mounts an HTTPAdapter with a transient-error retry policy.

        Deterministic and network-free — verifies our retry *configuration* rather than
        depending on a live service to provoke a 429/500.
        """
        adapter = durability_api_client.get_adapter("https://example.com")
        assert isinstance(adapter, HTTPAdapter)

        retries = adapter.max_retries
        assert retries.total >= 1
        assert retries.backoff_factor > 0
        for status in (429, 500, 502, 503, 504):
            assert status in retries.status_forcelist

    def test_successful_request(self, requests_mock, durability_api_client) -> None:
        """A successful GET returns HTTP 200 (mocked, no live service)."""
        requests_mock.get(_GET_URL, json={"ok": True}, status_code=200)

        response = durability_api_client.get(_GET_URL)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    def test_html_response_handling(self, requests_mock, durability_api_client) -> None:
        """A non-JSON HTML response is handled without error (mocked)."""
        requests_mock.get(_HTML_URL, text="<html><body>Herman Melville</body></html>")

        response = durability_api_client.get(_HTML_URL)

        assert response.status_code == 200
        assert "html" in response.text.lower()

    def test_429_status_surfaced_to_caller(self, requests_mock, durability_api_client) -> None:
        """A rate-limit (429) response status is surfaced to the caller rather than swallowed.

        Genuine retry-exhaustion (urllib3 RetryError) is not reproducible under requests-mock;
        the configured retry policy is asserted by test_durability_client_mounts_retry_adapter.
        """
        requests_mock.get(_GET_URL, status_code=429)

        response = durability_api_client.get(_GET_URL)

        assert response.status_code == 429

    def test_500_status_surfaced_to_caller(self, requests_mock, durability_api_client) -> None:
        """A server error (500) response status is surfaced to the caller (mocked)."""
        requests_mock.get(_GET_URL, status_code=500)

        response = durability_api_client.get(_GET_URL)

        assert response.status_code == 500

    def test_concurrent_requests_no_collision(self, requests_mock, durability_api_client_factory) -> None:
        """Parallel clients complete independently without interfering (mocked)."""
        requests_mock.get(_GET_URL, json={"ok": True}, status_code=200)

        def make_requests() -> list[int]:
            client = durability_api_client_factory()
            return [client.get(_GET_URL, timeout=10).status_code for _ in range(3)]

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_requests) for _ in range(3)]
            all_results = [future.result() for future in as_completed(futures)]

        for results in all_results:
            assert all(status == 200 for status in results), f"Failed results: {results}"
