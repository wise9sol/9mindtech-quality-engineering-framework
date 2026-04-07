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
def test_login_on_slow_network(page):
    browser_name = page.context.browser.browser_type.name
    if browser_name != "chromium":
        pytest.skip("CDP network emulation is only available for Chromium in this demo")

    cdp = page.context.new_cdp_session(page)
    cdp.send("Network.enable")
    cdp.send(
        "Network.emulateNetworkConditions",
        {
            "offline": False,
            "latency": 1500,  # milliseconds
            "downloadThroughput": 50 * 1024 / 8,  # 50 kbps approx
            "uploadThroughput": 20 * 1024 / 8,    # 20 kbps approx
            "connectionType": "cellular3g",
        },
    )

    page.goto(f"{BASE_URL}{LOGIN_PATH}")
    page.fill("#username", VALID_USERNAME)
    page.fill("#password", VALID_PASSWORD)
    page.click("button[type='submit']")

    page.screenshot(path=str(artifact_path("slow_login", ".png")), full_page=True)

    assert SUCCESS_PATH in page.url
    assert page.locator("#flash").is_visible()