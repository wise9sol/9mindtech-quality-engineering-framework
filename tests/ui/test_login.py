import pytest
from pages.home_page import HomePage
from utils.logger import logger


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.regression
def test_homepage(page, base_url: str) -> None:
    """Verify the home page loads and returns the expected title."""
    logger.info("Starting homepage test")
    home_page = HomePage(page)

    logger.info(f"Navigating to {base_url}")
    home_page.navigate(base_url)

    title = home_page.get_title()
    logger.info(f"Page title is: {title}")

    assert title == "The Internet"
    logger.info("Homepage test passed")
