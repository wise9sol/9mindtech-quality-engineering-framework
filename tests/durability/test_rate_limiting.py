"""
Durability: API rate limiting & retry logic.

Target: requests session retry/backoff configuration (durability_api_client fixture).
NIST correlation: SI-4 (System & Information Integrity Monitoring).
"""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.durability, pytest.mark.slow]


def _build_retry_session(total: int = 2, backoff_factor: float = 0.5) -> requests.Session:
    """Return a session whose transport retries on common transient HTTP errors."""
    session = requests.Session()
    retry_strategy = Retry(
        total=total,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


class TestRateLimitingDurability:
    """Stress test the API client's retry/backoff configuration."""

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

    @pytest.mark.skip(reason="Requires live httpbin.org — external service outside our control")
    def test_429_retry_exhaustion_raises(self) -> None:
        """Exhausted retries on HTTP 429 raise RetryError."""
        session = _build_retry_session()
        with pytest.raises(requests.exceptions.RetryError):
            session.get("https://httpbin.org/status/429", timeout=10)

    @pytest.mark.skip(reason="Requires live httpbin.org — external service outside our control")
    def test_500_retry_exhaustion_raises(self) -> None:
        """Exhausted retries on HTTP 500 raise RetryError."""
        session = _build_retry_session()
        with pytest.raises(requests.exceptions.RetryError):
            session.get("https://httpbin.org/status/500", timeout=10)

    @pytest.mark.skip(reason="Requires live httpbin.org — external service outside our control")
    def test_successful_request(self, durability_api_client) -> None:
        """A successful GET returns HTTP 200."""
        response = durability_api_client.get("https://httpbin.org/get")
        assert response.status_code == 200

    @pytest.mark.skip(reason="Requires live httpbin.org — external service outside our control")
    def test_concurrent_requests_no_collision(self, durability_api_client_factory) -> None:
        """Parallel clients complete independently without interfering."""

        def make_requests() -> list[int]:
            client = durability_api_client_factory()
            retry = Retry(total=2, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504])
            client.mount("https://", HTTPAdapter(max_retries=retry))
            return [client.get("https://httpbin.org/get", timeout=10).status_code for _ in range(3)]

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_requests) for _ in range(3)]
            all_results = [future.result() for future in as_completed(futures)]

        for results in all_results:
            assert all(status == 200 for status in results), f"Failed results: {results}"

    @pytest.mark.skip(reason="Requires live httpbin.org — external service outside our control")
    def test_html_response_handling(self, durability_api_client) -> None:
        """A non-JSON HTML response is handled without error."""
        response = durability_api_client.get("https://httpbin.org/html")
        assert response.status_code == 200
        assert "html" in response.text.lower()
