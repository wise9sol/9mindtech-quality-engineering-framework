import os
from pathlib import Path
from datetime import datetime

import pytest
from dotenv import load_dotenv
from ai.self_healer import SelfHealingPlugin
from ai.failure_analyst import run_analysis

load_dotenv()


def pytest_configure(config: pytest.Config) -> None:
    config.pluginmanager.register(SelfHealingPlugin(), "self_healing")


@pytest.fixture(scope="session")
def worker_id(request: pytest.FixtureRequest) -> str:
    """Return xdist worker ID, or 'master' when running without parallelism."""
    return getattr(request.config, "workerinput", {}).get("workerid", "master")


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# ── Fixtures ───────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL for UI tests. Explicit override so xdist workers always get the value."""
    return os.getenv("BASE_URL", "https://the-internet.herokuapp.com")


@pytest.fixture(scope="session")
def api_base_url() -> str:
    """Base URL for API tests. Reads API_BASE_URL from .env."""
    return os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")


@pytest.fixture(scope="function")
def context(browser, worker_id):
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)

    ctx = browser.new_context(
        ignore_https_errors=True,
        viewport={"width": 1440, "height": 900},
    )
    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx

    trace_path = artifacts_dir / f"trace_{worker_id}_{_timestamp()}.zip"
    ctx.tracing.stop(path=str(trace_path))
    ctx.close()


@pytest.fixture(scope="function")
def page(context):
    p = context.new_page()
    yield p
    p.close()


# ── Hooks ──────────────────────────────────────────────────────────────────────


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    if exitstatus not in (0, 5):  # 0 = all passed, 5 = no tests collected
        try:
            run_analysis()
        except FileNotFoundError:
            pass  # Allure results not present — skip silently


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
                page.screenshot(path=str(screenshot_path), timeout=5000)
                print(f"\nScreenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"\nScreenshot failed: {e}")
