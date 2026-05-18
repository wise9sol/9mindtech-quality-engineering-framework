from playwright.sync_api import Page


class BasePage:
    """Base class for all Page Objects. Wraps common Playwright interactions."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, url: str) -> None:
        """Navigate to the given URL and wait for the page to load."""
        self.page.goto(url)

    def click(self, locator: str) -> None:
        """Click the element matching the given locator."""
        self.page.click(locator)

    def fill(self, locator: str, text: str) -> None:
        """Fill the input matching the given locator with text."""
        self.page.fill(locator, text)

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()
