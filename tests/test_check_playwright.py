def test_playwright_setup(page):
    page.goto("https://example.com")
    assert "Example" in page.title()