import os
from pathlib import Path
from datetime import datetime

import pytest


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


@pytest.fixture(scope="function")
def context(browser):
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)

    context = browser.new_context(
        ignore_https_errors=True,
        viewport={"width": 1440, "height": 900},
    )

    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context

    trace_path = artifacts_dir / f"trace_{_timestamp()}.zip"
    context.tracing.stop(path=str(trace_path))
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()


from pathlib import Path
from datetime import datetime
import pytest


def _timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")

        if page:
            try:
                screenshots_dir = Path("reports/screenshots")
                screenshots_dir.mkdir(parents=True, exist_ok=True)

                screenshot_path = screenshots_dir / f"{item.name}_{_timestamp()}.png"

                page.screenshot(
                    path=str(screenshot_path),
                    timeout=5000  # 🔥 prevents crash
                )

            except Exception as e:
                print(f"⚠️ Screenshot failed safely: {e}")