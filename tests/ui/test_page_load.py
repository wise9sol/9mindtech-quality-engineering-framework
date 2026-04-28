import pytest
from playwright.sync_api import Page, expect


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
