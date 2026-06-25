# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""Root conftest — all shared fixtures, hooks, and plugin registration for the 9MindTech framework."""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Generator

import allure

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page

from ai.self_healer import SelfHealingPlugin
from ai.failure_analyst import run_analysis
from pages.login_page import LoginPage

load_dotenv()


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--save-traces",
        action="store_true",
        default=False,
        help="Save Playwright traces to artifacts/ on test failure.",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.pluginmanager.register(SelfHealingPlugin(), "self_healing")
    config.addinivalue_line("markers", "nist_ac2: NIST 800-53 AC-2 Account Management")
    config.addinivalue_line("markers", "nist_ac3: NIST 800-53 AC-3 Access Enforcement")
    config.addinivalue_line("markers", "nist_ac17: NIST 800-53 AC-17 Remote Access")
    config.addinivalue_line("markers", "nist_au2: NIST 800-53 AU-2 Event Logging")
    config.addinivalue_line("markers", "nist_au9: NIST 800-53 AU-9 Protection of Audit Information")
    config.addinivalue_line("markers", "nist_au12: NIST 800-53 AU-12 Audit Record Generation")
    config.addinivalue_line("markers", "nist_si2: NIST 800-53 SI-2 Flaw Remediation")
    config.addinivalue_line("markers", "nist_si10: NIST 800-53 SI-10 Information Input Validation")
    config.addinivalue_line("markers", "nist_si12: NIST 800-53 SI-12 Information Management and Retention")
    config.addinivalue_line("markers", "nist_ir5: NIST 800-53 IR-5 Incident Monitoring")
    config.addinivalue_line("markers", "nist_ir6: NIST 800-53 IR-6 Incident Reporting")
    config.addinivalue_line("markers", "nist_sc8: NIST 800-53 SC-8 Transmission Confidentiality and Integrity")
    config.addinivalue_line("markers", "nist_sc28: NIST 800-53 SC-28 Protection of Information at Rest")
    config.addinivalue_line("markers", "nist_ia2: NIST 800-53 IA-2 Identification and Authentication")
    config.addinivalue_line("markers", "nist_ia5: NIST 800-53 IA-5 Authenticator Management")
    config.addinivalue_line("markers", "nist_cm2: NIST 800-53 CM-2 Baseline Configuration")
    config.addinivalue_line("markers", "nist_cm6: NIST 800-53 CM-6 Configuration Settings")
    config.addinivalue_line("markers", "nist_cm7: NIST 800-53 CM-7 Least Functionality")
    config.addinivalue_line("markers", "nist_cm8: NIST 800-53 CM-8 System Component Inventory")
    config.addinivalue_line("markers", "nist_ia3: NIST 800-53 IA-3 Device Identification and Authentication")
    config.addinivalue_line("markers", "nist_ia4: NIST 800-53 IA-4 Identifier Management")
    config.addinivalue_line("markers", "nist_ia8: NIST 800-53 IA-8 Non-Organisational Users")
    config.addinivalue_line("markers", "compliance: cross-cutting compliance tests")
    config.addinivalue_line("markers", "healthcare: healthcare regulatory tests")
    config.addinivalue_line("markers", "finance: finance regulatory tests")
    config.addinivalue_line("markers", "durability: marks tests that stress framework robustness")
    config.addinivalue_line("markers", "nist_si4: NIST 800-53 SI-4 System Monitoring")
    config.addinivalue_line("markers", "slow: tests that take > 5 minutes")


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


@pytest.fixture
def valid_credentials() -> dict[str, str]:
    """Valid login credentials for the-internet.herokuapp.com."""
    return {
        "username": os.getenv("TEST_USERNAME", "tomsmith").strip("﻿").strip(),
        "password": os.getenv("TEST_PASSWORD", "SuperSecretPassword!").strip("﻿").strip(),
    }


@pytest.fixture
def invalid_credentials() -> dict[str, str]:
    """Invalid login credentials for negative test cases."""
    return {"username": "invalid_user", "password": "wrong_password"}


@pytest.fixture
def login_page(page: Page, base_url: str) -> LoginPage:
    """Navigate to /login and return a LoginPage instance."""
    login = LoginPage(page)
    page.goto(f"{base_url}/login")
    return login


@pytest.fixture(scope="function")
def context(browser: Browser, worker_id: str, request: pytest.FixtureRequest) -> Generator[BrowserContext, None, None]:
    """Playwright browser context. Pass --save-traces to capture traces on failure."""
    save_traces = request.config.getoption("--save-traces", default=False)

    ctx = browser.new_context(
        ignore_https_errors=True,
        viewport={"width": 1440, "height": 900},
    )
    if save_traces:
        ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx

    if save_traces:
        rep = getattr(request.node, "rep_call", None)
        if rep is not None and rep.failed:
            artifacts_dir = Path("artifacts")
            artifacts_dir.mkdir(exist_ok=True)
            trace_path = artifacts_dir / f"trace_{worker_id}_{_timestamp()}.zip"
            ctx.tracing.stop(path=str(trace_path))
        else:
            ctx.tracing.stop()
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Create a new Playwright page within the shared context."""
    p = context.new_page()
    yield p
    p.close()


# ── Hooks ──────────────────────────────────────────────────────────────────────


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Trigger AI failure analysis when the test session ends with failures."""
    if exitstatus == 1:  # 1 = tests failed; not interrupted (2) or internal error (3)
        try:
            run_analysis()
        except FileNotFoundError:
            pass  # Allure results not present — skip silently


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, pytest.TestReport, pytest.TestReport]:
    """Save a screenshot on failure and stash the report on the item for trace teardown."""
    report = yield

    if report.when == "call":
        item.rep_call = report  # type: ignore[attr-defined]

        if report.failed:
            page = item.funcargs.get("page")  # type: ignore[attr-defined]
            if page:
                try:
                    screenshots_dir = Path("reports/screenshots")
                    screenshots_dir.mkdir(parents=True, exist_ok=True)
                    screenshot_path = screenshots_dir / f"{item.name}_{_timestamp()}.png"
                    page.screenshot(path=str(screenshot_path), timeout=5000)
                    print(f"\nScreenshot saved: {screenshot_path}")
                except Exception as e:
                    print(f"\nScreenshot failed: {e}")

            nist_controls = [
                re.sub(r"([A-Z]+)(\d+)", r"\1-\2", m.name.replace("nist_", "").upper())
                for m in item.iter_markers()
                if m.name.startswith("nist_")
            ]
            if nist_controls:
                allure.attach(
                    f"Test: {item.name}\nFailing controls: {', '.join(nist_controls)}",
                    name="NIST 800-53 Failing Controls",
                    attachment_type=allure.attachment_type.TEXT,
                )

    return report


# ... all your existing code above ...


# ===== DURABILITY FIXTURES =====


@pytest.fixture(scope="session")
def durability_api_client():
    """Session-scoped API client with retry config for durability tests."""
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    session = requests.Session()
    retry_strategy = Retry(
        total=4,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


@pytest.fixture
def durability_api_client_factory():
    """Factory for isolated API clients (parallel durability tests)."""
    import requests
    import uuid

    def _create():
        session = requests.Session()
        session.headers.update({"X-Test-Session": uuid.uuid4().hex})
        return session

    return _create


@pytest.fixture
def nist_reporter(tmp_path):
    """NIST 800-53 compliance reporter for durability tests."""
    from datetime import datetime
    from dataclasses import dataclass, field
    from typing import List, Dict, Any
    from pathlib import Path

    @dataclass
    class NISTReport:
        output_dir: Path
        _violations: List[Dict[str, Any]] = field(default_factory=list)

        def record_violation(self, control: str, description: str, details: Dict[str, Any] = None):
            self._violations.append(
                {
                    "control": control,
                    "description": description,
                    "details": details or {},
                    "timestamp": datetime.now().isoformat(),
                }
            )

        def get_violations(self, control: str = None, time_window_seconds: int = None) -> List[Dict]:
            result = self._violations
            if control:
                result = [v for v in result if v["control"] == control]
            if time_window_seconds:
                cutoff = datetime.now().timestamp() - time_window_seconds
                result = [v for v in result if datetime.fromisoformat(v["timestamp"]).timestamp() > cutoff]
            return result

        def assert_control_passed(self, control: str, description: str = None):
            violations = self.get_violations(control=control)
            if description:
                violations = [v for v in violations if description in v["description"]]
            assert len(violations) == 0, f"NIST {control} failed: {violations}"

    report_dir = tmp_path / "nist-validation-report"
    report_dir.mkdir(exist_ok=True)
    return NISTReport(output_dir=report_dir)
