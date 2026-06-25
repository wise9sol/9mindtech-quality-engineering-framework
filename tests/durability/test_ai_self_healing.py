"""
Durability: AI self-healing locators with Claude Sonnet.

Target: ai/self_healer.py
"""

import logging

import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from ai.self_healer import SelfHealingPlugin

logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.durability, pytest.mark.slow]


class TestAISelfHealingDurability:
    """Stress AI locator recovery against dynamic, broken, or hidden elements."""

    def test_self_healing_plugin_registered(self, request: pytest.FixtureRequest) -> None:
        """Verify SelfHealingPlugin is registered with pytest."""
        plugin = request.config.pluginmanager.get_plugin("self_healing")

        assert plugin is not None
        assert isinstance(plugin, SelfHealingPlugin)
        logger.info("SelfHealingPlugin is registered correctly")

    def test_dynamic_content_handling(self, page, base_url: str) -> None:
        """Framework handles dynamic DOM changes on the configured base URL."""
        page.goto(f"{base_url}/dynamic_controls")

        remove_button = page.locator("button:has-text('Remove')")
        assert remove_button.is_visible()

        remove_button.click()

        add_button = page.locator("button:has-text('Add')")
        add_button.wait_for(state="visible", timeout=5000)

        assert add_button.is_visible()
        logger.info("Dynamic content handled successfully")

    def test_timeout_graceful_handling(self, page, base_url: str) -> None:
        """Locator timeouts raise rather than crash the framework."""
        page.goto(f"{base_url}/dynamic_controls")

        with pytest.raises(PlaywrightTimeoutError):
            page.wait_for_selector("#non-existent-element-xyz", timeout=2000)

        logger.info("Timeout handled gracefully")
