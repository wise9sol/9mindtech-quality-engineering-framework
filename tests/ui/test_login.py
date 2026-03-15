from pages.home_page import HomePage
from utils.config import BASE_URL


def test_homepage(page):
    home_page = HomePage(page)
    home_page.navigate(BASE_URL)
    assert home_page.get_title() == "Example Domain"