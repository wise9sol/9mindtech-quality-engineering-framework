from pages.home_page import HomePage


def test_homepage(page):
    home_page = HomePage(page)
    home_page.navigate("https://example.com")
    assert home_page.get_title() == "Example Domain"