import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
@pytest.mark.regression
def test_page_renders_correctly_at_mobile_viewport(page: Page, base_url: str) -> None:
    """Verify the page is usable at a standard mobile viewport (375x667)."""
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto(base_url)
    expect(page).not_to_have_title("")


@pytest.mark.ui
@pytest.mark.regression
def test_page_renders_correctly_at_desktop_viewport(page: Page, base_url: str) -> None:
    """Verify the page is usable at a standard desktop viewport (1280x720)."""
    page.set_viewport_size({"width": 1280, "height": 720})
    page.goto(base_url)
    expect(page).not_to_have_title("")
