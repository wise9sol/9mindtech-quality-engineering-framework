# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
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
    """Verify clicking a nav link on the home page loads the correct target page."""
    page.goto(base_url)
    page.get_by_role("link", name="Form Authentication").click()
    expect(page).to_have_url(f"{base_url}/login")
