"""
Durability: long-running stability — memory, thread, and browser-context leaks.
"""

import gc
import logging

import pytest

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.durability, pytest.mark.slow]


class TestLongRunningStability:
    """Memory and resource leak detection over extended runs."""

    @pytest.mark.skip(reason="Requires live quotes.toscrape.com — external service outside our control")
    def test_infinite_scroll_stability(self, page) -> None:
        """Page remains stable during repeated infinite-scroll loads."""
        page.goto("https://quotes.toscrape.com/scroll")

        for scroll_count in range(1, 31):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_load_state("networkidle")

            if scroll_count % 10 == 0:
                gc.collect()
                logger.info("Completed %d scrolls", scroll_count)

        logger.info("Scroll stability test passed")

    def test_context_isolation(self, browser, base_url: str) -> None:
        """Browser contexts are released and do not leak across iterations."""
        initial_contexts = len(browser.contexts)

        for _ in range(10):
            context = browser.new_context()
            page = context.new_page()
            page.goto(base_url)
            context.close()
            gc.collect()

        final_contexts = len(browser.contexts)

        assert final_contexts <= initial_contexts + 1
        logger.info("Context isolation: %d -> %d", initial_contexts, final_contexts)

    def test_socket_cleanup(self, requests_mock, durability_api_client_factory) -> None:
        """API clients are created, used, and closed across many iterations without error.

        Uses requests-mock (no real sockets) — verifies a clean client lifecycle rather
        than provoking real socket exhaustion against a live service.
        """
        requests_mock.get("https://httpbin.org/get", json={"ok": True}, status_code=200)
        clients = [durability_api_client_factory() for _ in range(5)]

        for client in clients:
            for _ in range(10):
                resp = client.get("https://httpbin.org/get", timeout=5)
                assert resp.status_code == 200

        for client in clients:
            client.close()
        gc.collect()

        logger.info("Socket cleanup test passed")
