import pytest
from pages.home_page import HomePage
from utils.config import BASE_URL
from utils.logger import logger


@pytest.mark.smoke
@pytest.mark.regression
def test_homepage(page):
    logger.info("Starting homepage test")
    home_page = HomePage(page)

    logger.info(f"Navigating to {BASE_URL}")
    home_page.navigate(BASE_URL)

    title = home_page.get_title()
    logger.info(f"Page title is: {title}")

    assert title == "Example Domain"
    logger.info("Homepage test passed")