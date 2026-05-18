import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
@pytest.mark.smoke
def test_playwright_setup(page: Page, base_url: str) -> None:
    """Verify Playwright can reach and load the target application."""
    page.goto(base_url)
    expect(page).not_to_have_title("")
