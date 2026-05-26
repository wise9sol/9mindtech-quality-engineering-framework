# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.smoke
def test_page_load_completes_for_home(page: Page, base_url: str) -> None:
    """Verify the home page fully loads without JS errors."""
    errors: list[str] = []
    page.on("pageerror", lambda err: errors.append(str(err)))

    page.goto(base_url)
    expect(page).not_to_have_title("")

    assert errors == [], f"JS errors on page load: {errors}"


@pytest.mark.ui
@pytest.mark.regression
def test_page_load_title_is_not_empty(page: Page, base_url: str) -> None:
    """Verify the page title is set after load."""
    page.goto(base_url)

    assert page.title() != ""


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.regression
def test_home_page_title_matches_expected(page: Page, base_url: str) -> None:
    """Verify the home page loads and returns the expected title."""
    home_page = HomePage(page)
    home_page.navigate(base_url)
    assert home_page.get_title() == "The Internet"
