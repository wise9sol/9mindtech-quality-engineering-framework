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
def test_login_when_offline(page):
    page.goto(f"{BASE_URL}{LOGIN_PATH}")

    page.context.set_offline(True)

    page.fill("#username", VALID_USERNAME)
    page.fill("#password", VALID_PASSWORD)

    try:
        page.click("button[type='submit']", timeout=5000)
        page.wait_for_load_state("networkidle", timeout=5000)
    except Exception:
        pass  # navigation failure is expected when offline

    page.screenshot(path=str(artifact_path("offline_login", ".png")), full_page=True)

    assert SUCCESS_PATH not in page.url, "Login should not succeed while offline"