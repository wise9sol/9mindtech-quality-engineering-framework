# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for the-internet.herokuapp.com/login."""

    username = "#username"
    password = "#password"  # nosec B105 — CSS selector, not a credential
    login_button = "button[type='submit']"

    def login(self, user: str, pwd: str) -> None:
        """Fill credentials and submit the login form."""
        self.fill(self.username, user)
        self.fill(self.password, pwd)
        self.click(self.login_button)
