from playwright.sync_api import expect

from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for the-internet.herokuapp.com home page."""

    HEADING = "h1.heading"
    EXAMPLES_LIST = "ul li"
    EXAMPLE_LINK = "ul li a[href='/{slug}']"

    def load(self, base_url: str) -> None:
        """Navigate to the home page and wait for the heading to be visible."""
        self.page.goto(base_url)
        expect(self.page.locator(self.HEADING)).to_be_visible()

    def get_heading(self) -> str:
        """Return the main heading text."""
        return self.page.locator(self.HEADING).inner_text()

    def get_example_count(self) -> int:
        """Return the number of example links listed on the page."""
        return self.page.locator(self.EXAMPLES_LIST).count()

    def navigate_to_example(self, slug: str) -> None:
        """Click an example link by its URL slug (e.g. 'login', 'checkboxes')."""
        locator = self.EXAMPLE_LINK.format(slug=slug)
        expect(self.page.locator(locator)).to_be_visible()
        self.page.click(locator)

    def has_example(self, slug: str) -> bool:
        """Return True if an example with the given slug exists in the list."""
        locator = self.EXAMPLE_LINK.format(slug=slug)
        return self.page.locator(locator).count() > 0
