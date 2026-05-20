# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
import pytest
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.regression
def test_homepage(page, base_url: str) -> None:
    """Verify the home page loads and returns the expected title."""
    home_page = HomePage(page)
    home_page.navigate(base_url)
    assert home_page.get_title() == "The Internet"
