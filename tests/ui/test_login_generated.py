import re

import pytest
from playwright.sync_api import expect, Page
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page, base_url):
    login = LoginPage(page)
    page.goto(f"{base_url}/login")
    return login


@pytest.fixture
def valid_credentials():
    return {"username": "tomsmith", "password": "SuperSecretPassword!"}


@pytest.fixture
def invalid_credentials():
    return {"username": "invalid_user", "password": "wrong_password"}


class TestLoginHappyPath:

    @pytest.mark.ai_generated
    @pytest.mark.smoke
    def test_login_successful_with_valid_credentials(self, login_page, valid_credentials, page):
        "AI generated: 2026-04-27. Tests successful login with valid username and password."
        login_page.login(valid_credentials["username"], valid_credentials["password"])
        expect(page).to_have_url(re.compile(r"secure"), timeout=5000)

    @pytest.mark.ai_generated
    @pytest.mark.smoke
    def test_login_redirects_to_dashboard_after_success(self, login_page, valid_credentials, page):
        "AI generated: 2026-04-27. Tests user is redirected to dashboard after successful login."
        login_page.login(valid_credentials["username"], valid_credentials["password"])
        expect(page).not_to_have_url(re.compile(r"login"))

    @pytest.mark.ai_generated
    def test_login_button_clickable_with_filled_fields(self, login_page, valid_credentials, page):
        "AI generated: 2026-04-27. Tests login button remains clickable when fields are filled."
        login_page.fill(login_page.username, valid_credentials["username"])
        login_page.fill(login_page.password, valid_credentials["password"])
        expect(page.locator(login_page.login_button)).to_be_enabled()


class TestLoginSadPath:

    @pytest.mark.ai_generated
    @pytest.mark.regression
    def test_login_fails_with_invalid_username(self, login_page, page):
        "AI generated: 2026-04-27. Tests login fails with invalid username and valid password."
        login_page.login("nonexistent_user", "Test@12345")
        expect(page.locator(".flash.error")).to_be_visible(timeout=3000)

    @pytest.mark.ai_generated
    @pytest.mark.regression
    def test_login_fails_with_invalid_password(self, login_page, page):
        "AI generated: 2026-04-27. Tests login fails with valid username and invalid password."
        login_page.login("testuser", "wrongpassword")
        expect(page.locator(".flash.error")).to_be_visible(timeout=3000)

    @pytest.mark.ai_generated
    @pytest.mark.regression
    def test_login_fails_with_both_invalid_credentials(self, login_page, invalid_credentials, page):
        "AI generated: 2026-04-27. Tests login fails when both username and password are invalid."
        login_page.login(invalid_credentials["username"], invalid_credentials["password"])
        expect(page.locator(".flash.error")).to_be_visible(timeout=3000)

    @pytest.mark.ai_generated
    @pytest.mark.regression
    def test_login_error_message_displayed_on_failure(self, login_page, invalid_credentials, page):
        "AI generated: 2026-04-27. Tests error message is displayed after failed login attempt."
        login_page.login(invalid_credentials["username"], invalid_credentials["password"])
        expect(page.locator(".flash.error")).to_be_visible(timeout=3000)

    @pytest.mark.ai_generated
    @pytest.mark.regression
    def test_login_stays_on_login_page_after_failure(self, login_page, invalid_credentials, page):
        "AI generated: 2026-04-27. Tests user remains on login page after failed login."
        login_page.login(invalid_credentials["username"], invalid_credentials["password"])
        expect(page).to_have_url(re.compile(r"login"))


class TestLoginEdgeCases:

    @pytest.mark.ai_generated
    @pytest.mark.regression
    def test_login_fails_with_empty_username(self, login_page, page):
        "AI generated: 2026-04-27. Tests login fails when username field is empty."
        login_page.login("", "Test@12345")
        expect(page.locator(".flash.error")).to_be_visible(timeout=3000)

    @pytest.mark.ai_generated
    @pytest.mark.regression
    def test_login_fails_with_empty_password(self, login_page, page):
        "AI generated: 2026-04-27. Tests login fails when password field is empty."
        login_page.login("testuser", "")
        expect(page.locator(".flash.error")).to_be_visible(timeout=3000)

    @pytest.mark.ai_generated
    @pytest.mark.regression
    def test_login_fails_with_both_fields_empty(self, login_page, page):
        "AI generated: 2026-04-27. Tests login fails when both username and password are empty."
        login_page.login("", "")
        expect(page.locator(".flash.error")).to_be_visible(timeout=3000)

    @pytest.mark.ai_generated
    @pytest.mark.regression
    def test_login_handles_whitespace_only_username(self, login_page, page):
        "AI generated: 2026-04-27. Tests login handles username with only whitespace characters."
        login_page.login("   ", "Test@12345")
        expect(page.locator(".flash.error")).to_be_visible(timeout=3000)

    @pytest.mark.ai_generated
    @pytest.mark.regression
    def test_login_handles_whitespace_only_password(self, login_page, page):
        "AI generated: 2026-04-27. Tests login handles password with only whitespace characters."
        login_page.login("testuser", "   ")
        expect(page.locator(".flash.error")).to_be_visible(timeout=3000)

    @pytest.mark.ai_generated
    @pytest.mark.regression
    def test_login_handles_special_characters_in_username(self, login_page, page):
        "AI generated: 2026-04-27. Tests login handles special characters in username field."
        login_page.login("user@#$%^&*()", "Test@12345")
        expect(page.locator(".flash.error")).to_be_visible(timeout=3000)

    @pytest.mark.ai_generated
    @pytest.mark.regression
    def test_login_handles_sql_injection_attempt_username(self, login_page, page):
        "AI generated: 2026-04-27. Tests login safely handles SQL injection attempt in username."
        login_page.login("' OR '1'='1", "Test@12345")
        expect(page.locator(".flash.error")).to_be_visible(timeout=3000)

    @pytest.mark.ai_generated
    @pytest.mark.regression
    def test_login_handles_sql_injection_attempt_password(self, login_page, page):
        "AI generated: 2026-04-27. Tests login safely handles SQL injection attempt in password."
        login_page.login("testuser", "' OR '1'='1")
        expect(page.locator(".flash.error")).to_be_visible(timeout=3000)

    @pytest.mark.ai_generated
    @pytest.mark.regression
    def test_login_handles_xss_attempt_in_username(self, login_page, page):
        "AI generated: 2026-04-27. Tests login safely handles XSS attempt in username field."
        login_page.login("<script>alert('xss')</script>", "Test@12345")
        expect(page.locator(".flash.error")).to_be_visible(timeout=3000)