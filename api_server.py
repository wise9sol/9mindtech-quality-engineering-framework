"""
QualiOps API Server - The product wrapper for your AI QA engine.
Clients send natural language test specs, get back results.
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import subprocess

from ai.client import get_client, CLAUDE_MODEL, extract_text

app = FastAPI(
    title="QualiOps AI Quality Engine",
    description="Natural language test automation with AI self-healing",
    version="1.0.0",
)

PROJECT_ROOT = Path(__file__).parent
GENERATED_DIR = PROJECT_ROOT / "tests" / "generated"

# Ensure required directories exist at startup
GENERATED_DIR.mkdir(parents=True, exist_ok=True)
(PROJECT_ROOT / "reports" / "allure-results").mkdir(parents=True, exist_ok=True)

# In-memory run store — replace with Redis/DB for production
run_status: dict = {}


class TestRunRequest(BaseModel):
    """Payload a client sends to start a test run."""

    client_id: str
    test_spec: str  # Plain-English description of what to test
    webhook_url: Optional[str] = None


class TestStep(BaseModel):
    step: str


# ── Endpoints ──────────────────────────────────────────────────────────────────


@app.get("/")
def root():
    return {
        "service": "QualiOps AI Quality Engine",
        "status": "operational",
        "endpoints": [
            "POST /run    — Execute a test suite from natural language",
            "GET  /status/{run_id} — Poll test run status",
            "GET  /report/{run_id} — Download test report",
            "POST /translate       — Preview NL→code translation",
        ],
    }


@app.post("/translate")
def translate_steps(steps: list[TestStep]):
    """Preview: show what code the AI would generate. No execution."""
    from tools.nl_translator import translate_step_to_code

    # Real method signatures from LoginPage / BasePage
    available_methods = [
        "login_page.navigate('https://the-internet.herokuapp.com/login')",
        "login_page.login('tomsmith', 'SuperSecretPassword!')",
        "login_page.fill(login_page.username, 'value')",
        "login_page.fill(login_page.password, 'value')",
        "login_page.click(login_page.login_button)",
        "login_page.get_title()",
    ]

    translations = []
    for step in steps:
        code = translate_step_to_code(step.step, available_methods)
        translations.append({"original": step.step, "generated_code": code})

    return {"translations": translations}


@app.post("/run")
def run_test(request: TestRunRequest, background_tasks: BackgroundTasks):
    """
    Start a test run from a plain-English spec.
    Returns a run_id immediately; tests execute in the background.
    """
    run_id = str(uuid.uuid4())[:8]

    run_status[run_id] = {
        "status": "queued",
        "client_id": request.client_id,
        "started_at": datetime.now().isoformat(),
        "result": None,
    }

    background_tasks.add_task(execute_test_suite, run_id, request)

    return {
        "run_id": run_id,
        "status": "queued",
        "message": f"Test run queued. Poll /status/{run_id} for results.",
    }


@app.get("/status/{run_id}")
def get_status(run_id: str):
    """Poll this endpoint to check whether a test run is done."""
    if run_id not in run_status:
        raise HTTPException(status_code=404, detail="Run ID not found")
    return run_status[run_id]


@app.get("/report/{run_id}")
def get_report(run_id: str):
    """Return a JSON summary of results for a completed run."""
    if run_id not in run_status:
        raise HTTPException(status_code=404, detail="Run ID not found")

    report_dir = PROJECT_ROOT / "reports" / "allure-results" / run_id
    if not report_dir.exists():
        raise HTTPException(status_code=404, detail="Report not ready yet")

    return JSONResponse(content=run_status[run_id])


# ── Background execution ────────────────────────────────────────────────────────


def execute_test_suite(run_id: str, request: TestRunRequest) -> None:
    """
    Generate a pytest test from the natural-language spec, run it with the
    project's page objects, and store the result.
    """
    test_file = GENERATED_DIR / f"test_{run_id}.py"

    try:
        run_status[run_id]["status"] = "running"

        # 1 — Generate test code via Claude
        test_code = generate_test_from_spec(request.test_spec)
        test_file.write_text(test_code, encoding="utf-8")

        # 2 — Prepare per-run Allure output directory
        allure_dir = PROJECT_ROOT / "reports" / "allure-results" / run_id
        allure_dir.mkdir(parents=True, exist_ok=True)

        # 3 — Add project root to PYTHONPATH so page object imports resolve
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT) + os.pathsep + env.get("PYTHONPATH", "")

        # 4 — Run pytest
        #   --override-ini addopts=  clears the global --html flag from pytest.ini
        #   so concurrent runs don't clobber each other's report file.
        #   --browser chromium  is required by pytest-playwright when the page
        #   fixture is used (our conftest.py wraps the playwright browser fixture).
        pytest_exe = PROJECT_ROOT / ".venv" / "Scripts" / "pytest"
        result = subprocess.run(
            [
                str(pytest_exe),
                str(test_file),
                "-v",
                "--tb=short",
                "--override-ini",
                "addopts=",
                f"--alluredir={allure_dir}",
                "--browser",
                "chromium",
            ],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            env=env,
            timeout=300,
        )

        run_status[run_id].update(
            {
                "status": "passed" if result.returncode == 0 else "failed",
                "completed_at": datetime.now().isoformat(),
                "stdout": result.stdout[-2000:],
                "stderr": result.stderr[-500:],
                "report_path": str(allure_dir),
            }
        )

        # 5 — Notify via webhook if the caller provided one
        if request.webhook_url:
            import requests as _req

            try:
                _req.post(
                    request.webhook_url,
                    json={"run_id": run_id, "status": run_status[run_id]["status"]},
                    timeout=10,
                )
            except Exception:
                pass  # Webhook failure must not affect the stored result

    except subprocess.TimeoutExpired:
        run_status[run_id]["status"] = "timeout"
    except Exception as exc:
        run_status[run_id]["status"] = "error"
        run_status[run_id]["error"] = str(exc)
    finally:
        # Always clean up the generated test file
        if test_file.exists():
            test_file.unlink()


# ── AI test generation ──────────────────────────────────────────────────────────


def generate_test_from_spec(spec: str) -> str:
    """
    Ask Claude to produce a complete pytest test file from a plain-English spec.
    The prompt includes exact class signatures so Claude cannot hallucinate methods.
    """
    client = get_client()

    prompt = f"""Generate a complete, runnable pytest test file for the following requirement.

Requirement: {spec}

APPLICATION UNDER TEST:
- Login page URL : https://the-internet.herokuapp.com/login
- Valid username  : tomsmith
- Valid password  : SuperSecretPassword!
- Success indicator: page.url contains "/secure" after login

EXACT CLASS SIGNATURES — do not deviate from these:

class BasePage:
    def __init__(self, page): ...
    def navigate(self, url: str): ...    # url is REQUIRED — always pass a full URL string
    def fill(self, locator: str, text: str): ...
    def click(self, locator: str): ...
    def get_title(self) -> str: ...

class LoginPage(BasePage):
    # These three are CLASS ATTRIBUTES (CSS strings) — they are NOT callable:
    username     = "#username"
    password     = "#password"
    login_button = "button[type='submit']"

    def login(self, user: str, pwd: str): ...   # fills both fields then clicks submit

REQUIRED imports (no others):
    import pytest
    from pages.login_page import LoginPage

FIXTURE: `page` is the Playwright page object — injected automatically by pytest via conftest.py.
Do NOT import or instantiate Playwright yourself.

CORRECT usage — option A (use the combined login method):
    import pytest
    from pages.login_page import LoginPage

    @pytest.mark.ai_generated
    def test_login_succeeds_with_valid_credentials(page):
        \"\"\"AI-generated on 2026-05-12.\"\"\"
        login_page = LoginPage(page)
        login_page.navigate("https://the-internet.herokuapp.com/login")
        login_page.login("tomsmith", "SuperSecretPassword!")
        assert "/secure" in page.url

CORRECT usage — option B (fill fields individually using the locator attributes):
    login_page.navigate("https://the-internet.herokuapp.com/login")
    login_page.fill(login_page.username, "tomsmith")
    login_page.fill(login_page.password, "SuperSecretPassword!")
    login_page.click(login_page.login_button)
    assert "/secure" in page.url

NEVER do these (each raises TypeError because the attribute is a plain string):
    login_page.navigate()              # ERROR: url argument required
    login_page.username("tomsmith")    # ERROR: str is not callable
    login_page.password("secret")      # ERROR: str is not callable
    login_page.login_button()          # ERROR: str is not callable

RULES:
- Every test function must have @pytest.mark.ai_generated
- One-line docstring: \"\"\"AI-generated on 2026-05-12.\"\"\"
- Assertions use page.url or login_page.get_title() — never Playwright expect()
- Return ONLY the Python code — no prose, no markdown fences, no backticks
"""

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    code = extract_text(response)
    code = code.replace("```python", "").replace("```", "").strip()
    return code


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # nosec B104
