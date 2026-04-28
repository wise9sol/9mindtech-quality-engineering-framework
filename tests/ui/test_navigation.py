import re
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
@pytest.mark.smoke
def test_navigation_reaches_home_page(page: Page, base_url: str) -> None:
    """Verify navigating to the base URL loads the home page."""
    page.goto(base_url)
    expect(page).not_to_have_title("")


@pytest.mark.ui
@pytest.mark.regression
def test_navigation_internal_link_loads_target_page(page: Page, base_url: str) -> None:
    """Verify clicking a link navigates away from the home page."""
    page.goto("https://example.com")
    link = page.get_by_text("Learn more").first
    link.click()
    expect(page).to_have_url("https://www.iana.org/help/example-domains")
