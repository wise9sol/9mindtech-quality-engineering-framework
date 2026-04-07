import pytest
from utils.network_config import (
    BASE_URL,
    LOGIN_PATH,
    VALID_USERNAME,
    VALID_PASSWORD,
    SUCCESS_PATH,
)
from utils.artifacts import artifact_path


@pytest.mark.ui
@pytest.mark.network
def test_normal_login(page):
    page.goto(f"{BASE_URL}{LOGIN_PATH}")

    page.fill("#username", VALID_USERNAME)
    page.fill("#password", VALID_PASSWORD)
    page.click("button[type='submit']")

    page.screenshot(path=str(artifact_path("normal_login", ".png")), full_page=True)

    assert SUCCESS_PATH in page.url
    assert page.locator("#flash").is_visible()