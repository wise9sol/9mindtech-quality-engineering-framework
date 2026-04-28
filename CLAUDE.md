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

| Layer              | Technology         | Version       | Notes                          |
|--------------------|--------------------|---------------|--------------------------------|
| Language           | Python             | 3.13          | No upgrade without team sign-off|
| Test Runner        | pytest             | 8.3.5         | Config in `pytest.ini`         |
| Browser Automation | Playwright         | 1.51.0        | Chromium primary, FF/WebKit CI |
| HTTP / API Testing | requests           | 2.32.3        | No httpx unless justified      |
| AI Integration     | Anthropic SDK      | 0.49.0        | Claude Sonnet only — see ai/   |
| Parallel Execution | pytest-xdist       | latest        | `-n auto` in CI                |
| Reporting          | Allure + pytest-html | latest      | Allure is primary for clients  |
| Config             | python-dotenv      | latest        | All secrets via .env           |
| CI/CD              | GitHub Actions     | ubuntu-latest | See .github/workflows/         |
| Containerization   | Docker             | latest        | Dockerfile at root             |

---

## 📁 Folder Structure — LOCKED

```
9mindtech-qa/
├── CLAUDE.md                  ← YOU ARE HERE — read first, always
├── README.md
├── pytest.ini
├── requirements.txt
├── Dockerfile
├── .env.example
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── ai/                        ← AI Brain — Anthropic SDK lives here ONLY
│   ├── __init__.py
│   ├── client.py              ← Single Claude client instance
│   ├── test_generator.py      ← Auto-generate test cases from specs
│   ├── self_healer.py         ← Fix broken locators automatically
│   └── failure_analyst.py     ← Root cause analysis from Allure JSON
│
├── pages/                     ← Page Object Models
│   ├── base_page.py
│   └── [feature]_page.py
│
├── tests/
│   ├── ui/                    ← Playwright UI tests
│   ├── api/                   ← requests API tests
│   └── network/               ← Network condition tests (excluded from CI)
│
├── utils/
│   ├── api_client.py
│   ├── data_factory.py
│   └── helpers.py
│
├── fixtures/
│   └── conftest.py            ← All shared fixtures here, NEVER in test files
│
└── reports/                   ← Auto-generated — never commit this folder
    ├── allure-results/
    └── report.html
```

---

## 📐 Coding Conventions — NON-NEGOTIABLE

### General
- All code must pass `flake8` and be formatted with `black`
- Type hints required on all function signatures
- Docstrings required on all public classes and methods
- No hardcoded URLs, credentials, or env-specific values — use `.env`

### Test Naming
```python
# Pattern: test_[action]_[expected_outcome]_[condition_if_needed]
def test_login_succeeds_with_valid_credentials(): ...
def test_login_fails_with_invalid_password(): ...
def test_api_returns_400_when_payload_missing_required_field(): ...
```

### Pytest Markers — use these, no others without adding to pytest.ini
```python
@pytest.mark.smoke        # Fast, critical path — always run in CI
@pytest.mark.regression   # Full suite — run on release branches
@pytest.mark.api          # API-only tests
@pytest.mark.ui           # Browser tests
@pytest.mark.network      # Network condition tests — EXCLUDED from CI
@pytest.mark.ai_generated # Tests created by the AI test generator
```

### Page Object Model Rules
- One class per page/major component
- Locators defined as class attributes at the top
- No assertions inside Page Objects — only in test files
- All waits use `expect()` from Playwright — no `time.sleep()`

```python
class LoginPage(BasePage):
    # Locators — top of class, always
    EMAIL_INPUT = "[data-testid='email']"
    PASSWORD_INPUT = "[data-testid='password']"
    SUBMIT_BUTTON = "[data-testid='login-btn']"

    def login(self, email: str, password: str) -> None:
        self.page.fill(self.EMAIL_INPUT, email)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.SUBMIT_BUTTON)
```

### API Test Rules
- Every API test must assert: status code, response schema, response time < 2000ms
- Use `conftest.py` fixtures for base URLs and auth headers
- Schema validation uses `jsonschema` — define schemas in `utils/schemas/`

---

## 🤖 AI Module Rules (`ai/`)

- Claude model: **claude-sonnet-4-20250514** only — never change without approval
- All Claude calls go through `ai/client.py` — never instantiate Anthropic() elsewhere
- AI-generated tests get `@pytest.mark.ai_generated` and a docstring noting generation date
- Self-healer logs every locator change to `reports/healer.log`
- Failure analyst output saved to `reports/ai_analysis/` — never printed only to console
- Max tokens per call: 2000 for generation, 1000 for analysis

---

## 🚦 CI/CD Behavior — LOCKED

```yaml
# Execution order — do not change
1. Lint (flake8 + black --check)
2. Smoke tests: pytest -m smoke --tb=short
3. API tests: pytest -m api --tb=short
4. Regression: pytest -m regression -n auto (only on main branch)
5. Network tests: EXCLUDED from CI — run locally only
```

**Never add `time.sleep()` to fix flaky CI tests — fix the root cause.**
**Never use `--ignore` to skip failing tests without opening a tracking issue.**

---

## 🔐 Environment Variables

```bash
# .env.example — copy to .env, never commit .env
BASE_URL=https://your-app.com
API_BASE_URL=https://api.your-app.com
TEST_EMAIL=test@example.com
TEST_PASSWORD=
ANTHROPIC_API_KEY=          # Required for ai/ module
ALLURE_RESULTS_DIR=reports/allure-results
```

---

## ❌ What NOT To Do — Common AI Mistakes to Avoid

- Do NOT use `driver` — this is Playwright, not Selenium
- Do NOT use `sleep()` — use Playwright `expect()` or `wait_for_*`
- Do NOT put fixtures in test files — they go in `fixtures/conftest.py`
- Do NOT create a second Anthropic client — use `ai/client.py`
- Do NOT use `gpt-*` models — this framework uses Claude only
- Do NOT add `xfail` markers without a linked issue number
- Do NOT modify `reports/` — it is auto-generated
- Do NOT commit `.env` — use `.env.example` as the template

---

## ✅ Definition of Done (every PR)

- [ ] Tests pass locally: `pytest -m smoke -m api`
- [ ] No new flake8 warnings
- [ ] New tests follow naming conventions above
- [ ] CLAUDE.md updated if stack/structure changed
- [ ] Allure report reviewed before merge

---

*Last updated: 2026 · Maintained by 9MindTech*
