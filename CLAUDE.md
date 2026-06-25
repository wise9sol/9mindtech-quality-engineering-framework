# CLAUDE.md — 9MindTech Quality Engineering Framework
# Single source of truth for all AI assistants working in this repo.
# Read this before touching any file. Decisions here are FINAL.

---

## 🏢 Company Context

**Company**: 9MindTech
**Framework type**: QA Automation Framework
**Owner**: Principal QA Engineer / Founder
**Mission**: Elite, AI-augmented test automation — production-grade, zero ambiguity.

---

## 🧠 AI Collaboration Rules

This repo is worked on by multiple AI tools. To prevent conflicting suggestions:

| AI Tool        | Responsibility                                      |
|----------------|-----------------------------------------------------|
| Claude Code    | File execution — write, run, fix, refactor code     |
| Claude.ai      | Architecture, strategy, review, design decisions    |
| This CLAUDE.md | Single source of truth — resolves ALL conflicts     |

**Rule #1**: If an AI suggestion conflicts with this file, THIS FILE WINS.
**Rule #2**: Do not introduce new dependencies without updating `requirements.txt` and this file.
**Rule #3**: Do not change folder structure without updating the Structure section below.
**Rule #4**: Always run `pytest --co -q` to validate test collection before committing.

---

## ⚙️ Tech Stack — LOCKED

| Layer              | Technology         | Version       | Notes                              |
|--------------------|--------------------|---------------|------------------------------------|
| Language           | Python             | 3.13          | No upgrade without team sign-off   |
| Test Runner        | pytest             | 8.3.5         | Config in `pytest.ini`             |
| Browser Automation | Playwright         | 1.51.0        | Chromium primary, FF/WebKit CI     |
| HTTP / API Testing | requests           | 2.32.3        | No httpx unless justified          |
| AI Integration     | Anthropic SDK      | 0.49.0        | Claude Sonnet only — see `ai/`     |
| Parallel Execution | pytest-xdist       | 3.6.1         | `-n auto` in CI regression job     |
| Reporting          | Allure + pytest-html | 2.13.5 / 4.1.1 | Allure is primary for clients    |
| Schema Validation  | jsonschema         | 4.26.0        | Schemas live in `utils/schemas/`   |
| Config             | python-dotenv      | 1.0.1         | All secrets via `.env`             |
| Linting            | flake8             | 7.3.0         | Max line length 120                |
| Formatting         | black              | 26.5.1        | Enforced in CI                     |
| Type Checking      | mypy               | 2.1.0         | Checks `ai/ pages/ utils/` in CI   |
| Security Scanning  | bandit             | 1.9.4         | `-ll` severity in CI lint job      |
| API Server         | FastAPI + Uvicorn  | 0.136.1 / 0.46.0 | QualiOps product API — `api_server.py` |
| API Validation     | pydantic           | 2.13.1        | Request/response models in `api_server.py` |
| Pre-commit Hooks   | pre-commit         | 4.6.0         | `.pre-commit-config.yaml` at root  |
| CI/CD              | GitHub Actions     | ubuntu-latest | See `.github/workflows/tests.yml`  |
| Containerization   | Docker             | 1.51.0 image  | Dockerfile at root                 |

---

## 📁 Folder Structure — LOCKED

```
9mindtech-qa/
├── CLAUDE.md                  ← YOU ARE HERE — read first, always
├── README.md
├── pytest.ini
├── requirements.txt
├── Dockerfile
├── .env.example               ← Copy to .env — never commit .env
├── .github/
│   └── workflows/
│       └── tests.yml          ← lint → smoke+api → regression pipeline
│
├── ai/                        ← AI Brain — Anthropic SDK lives here ONLY
│   ├── __init__.py            ← Public API for the ai/ package
│   ├── client.py              ← Singleton Claude client + extract_text() helper
│   ├── test_generator.py      ← Auto-generate test cases from specs
│   ├── self_healer.py         ← Fix broken locators automatically
│   └── failure_analyst.py     ← Root cause analysis from Allure JSON
│
├── pages/                     ← Page Object Models
│   ├── base_page.py
│   ├── home_page.py
│   └── login_page.py
│
├── tests/
│   ├── ui/                    ← Playwright UI tests
│   ├── api/                   ← requests API tests
│   ├── network/               ← Network condition tests (excluded from CI)
│   ├── compliance/            ← NIST 800-53 control tests (AC/AU/IR/SC/IA/SI/...)
│   └── durability/            ← Stability/robustness tests (memory, retries, long-running)
│
├── tools/                     ← Developer CLI tools (not part of test suite)
│   ├── nl_translator.py       ← NL-to-page-object demo (QualiOps seed)
│   └── test_idea_generator.py
│
├── utils/
│   ├── config.py              ← BASE_URL and env config (single source of truth)
│   ├── logger.py              ← Shared logger instance
│   ├── network_config.py      ← Network test constants (import BASE_URL from utils.config)
│   ├── artifacts.py           ← Timestamped artifact path helper
│   └── schemas/               ← jsonschema definitions for API response validation
│       └── post.py
│
├── conftest.py                ← ALL shared fixtures and hooks here, NEVER in test files
│
└── reports/                   ← Auto-generated — never commit this folder
    ├── allure-results/
    ├── ai_analysis/
    ├── screenshots/
    └── report.html
```

---

## 📐 Coding Conventions — NON-NEGOTIABLE

### General
- All code must pass `flake8` and be formatted with `black`
- All code in `ai/ pages/ utils/` must pass `mypy --ignore-missing-imports`
- Type hints required on all function signatures
- Docstrings required on all public classes and methods
- No hardcoded URLs, credentials, or env-specific values — use `.env`

### Test Naming
```python
# Pattern: test_[action]_[expected_outcome]_[condition_if_needed]
def test_login_succeeds_with_valid_credentials(): ...
def test_login_fails_with_invalid_password(): ...
def test_api_returns_404_for_nonexistent_resource(): ...
```

### Pytest Markers — use these, no others without registering in `conftest.py` (`pytest_configure`)
```python
@pytest.mark.smoke        # Fast, critical path — always run in CI
@pytest.mark.regression   # Full suite — run on main branch
@pytest.mark.api          # API-only tests
@pytest.mark.ui           # Browser tests
@pytest.mark.network      # Network condition tests — EXCLUDED from CI
@pytest.mark.ai_generated # Tests created by the AI test generator
@pytest.mark.compliance   # Cross-cutting compliance tests (see tests/compliance/, plus nist_* control markers)
@pytest.mark.durability   # Stability/robustness tests (see tests/durability/)
@pytest.mark.slow         # Tests that take > 5 minutes
```

### Page Object Model Rules
- One class per page/major component
- Locators defined as class attributes at the top
- No assertions inside Page Objects — only in test files
- All waits use `expect()` from Playwright — no `time.sleep()`

```python
class LoginPage(BasePage):
    # Locators — top of class, always
    username = "#username"
    password = "#password"
    login_button = "button[type='submit']"

    def login(self, user: str, pwd: str) -> None:
        """Fill credentials and submit the login form."""
        self.fill(self.username, user)
        self.fill(self.password, pwd)
        self.click(self.login_button)
```

### API Test Rules
- Every API test must assert: status code, response time < 2000ms
- Use `response.elapsed.total_seconds() * 1000` — never `time.time()`
- Success responses must validate schema with `jsonschema.validate()`
- Use `conftest.py` fixtures for base URLs — never hardcode
- Schema definitions live in `utils/schemas/`

---

## 🤖 AI Module Rules (`ai/`)

- Claude model: **claude-sonnet-4-6** only — never change without approval
- All Claude calls go through `ai/client.py` — never instantiate `Anthropic()` elsewhere
- Use `extract_text(response)` from `ai/client.py` to read response text — never access `response.content[0].text` directly (fails mypy)
- AI-generated tests get `@pytest.mark.ai_generated` and a docstring noting generation date
- Self-healer logs every locator change to `reports/healer.log`
- Failure analyst output saved to `reports/ai_analysis/` — never printed only to console
- Max tokens per call: 2000 for generation, 1000 for analysis

---

## 🚦 CI/CD Behavior — LOCKED

```yaml
# Execution order — do not change
1. Lint:          flake8 + black --check + mypy (ai/ pages/ utils/) + bandit -r ai/ pages/ utils/ -ll
2. Smoke (UI):    pytest -m "smoke and ui" --tb=short  [Chromium]
3. API tests:     pytest -m api --tb=short
4. Cross-browser: pytest -m "smoke and ui" --browser {firefox,webkit} (matrix, parallel with smoke+api)
5. Regression:    pytest -m regression -n auto --tb=short --save-traces  (main branch only)
6. Network tests: EXCLUDED from CI — run locally only
```

**`--save-traces`**: Enables Playwright tracing in the regression job. Pass it locally when debugging a flaky test. Without it, no trace overhead.

**Never add `time.sleep()` to fix flaky CI tests — fix the root cause.**
**Never use `--ignore` to skip failing tests without opening a tracking issue.**

---

## 🔐 Environment Variables

```bash
# Copy .env.example to .env — never commit .env
ANTHROPIC_API_KEY=          # Required for ai/ module
BASE_URL=https://the-internet.herokuapp.com
API_BASE_URL=https://jsonplaceholder.typicode.com
TEST_EMAIL=test@example.com
TEST_PASSWORD=
ALLURE_RESULTS_DIR=reports/allure-results
```

---

## ❌ What NOT To Do — Common AI Mistakes to Avoid

- Do NOT use `driver` — this is Playwright, not Selenium
- Do NOT use `sleep()` — use Playwright `expect()` or `wait_for_*`
- Do NOT put fixtures in test files — they go in `conftest.py`
- Do NOT create a second Anthropic client — use `ai/client.py`
- Do NOT access `response.content[0].text` directly — use `extract_text(response)`
- Do NOT use `gpt-*` models — this framework uses Claude only
- Do NOT add `xfail` markers without a linked issue number
- Do NOT modify `reports/` — it is auto-generated
- Do NOT commit `.env` — use `.env.example` as the template
- Do NOT use `time.time()` for response timing — use `response.elapsed`

---

## ✅ Definition of Done (every PR)

- [ ] Tests pass locally: `pytest -m "smoke or api"`
- [ ] No new flake8 or mypy warnings
- [ ] New tests follow naming conventions above
- [ ] CLAUDE.md updated if stack/structure/rules changed
- [ ] Allure report reviewed before merge

---

*Last updated: 2026-05-18 · Maintained by 9MindTech*
