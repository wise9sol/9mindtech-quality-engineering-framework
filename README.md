<div align="center">

# QualiOps AI
### Autonomous Quality Engineering Platform

**Convert natural language test specs into production-grade Playwright tests — powered by Claude AI**

[![Tests](https://github.com/wise9sol/9mindtech-quality-engineering-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/wise9sol/9mindtech-quality-engineering-framework/actions/workflows/tests.yml)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)
[![Powered by Claude](https://img.shields.io/badge/AI-Claude%20Sonnet-blueviolet?logo=anthropic)](https://anthropic.com)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

---

[Quick Start](#quick-start) · [API Docs](#api-reference) · [Pricing](#pricing) · [Book a Demo](https://calendly.com/9mindtech_qa-automation-call)

</div>

---

## What is QualiOps AI?

QualiOps AI is an autonomous quality engineering platform that eliminates the gap between writing test requirements and having working automated tests. Describe what you want to test in plain English — QualiOps generates a complete, executable Playwright test suite in seconds.

No manual test scripting. No QA bottleneck. Just describe it, run it, ship it.

```
Input:  "Test that a user can log in with valid credentials and see the dashboard"

Output: 8+ runnable pytest scenarios covering happy path, error states,
        edge cases, and security — ready to drop into CI/CD
```

---

## Key Features

### Natural Language Test Generation
Write test requirements in plain English. QualiOps translates them into production-grade pytest + Playwright test files — complete with markers, docstrings, and assertions that match your coding standards.

### Self-Healing Tests
Locator changes break brittle test suites. QualiOps detects selector drift and automatically patches tests to match updated UI structure, logging every change to a full audit trail.

### REST API with Swagger Docs
Every capability is exposed via a clean REST API with interactive Swagger documentation at `/docs`. Integrate QualiOps into any CI/CD pipeline, internal tooling, or client portal in minutes.

### Docker Ready
Ship a fully containerised QA engine. One `docker run` command gives you a live API server — no Python environment setup, no dependency conflicts.

### 8+ Test Scenarios from One Sentence
A single natural language spec expands into a comprehensive test matrix: happy paths, invalid inputs, boundary values, authentication edge cases, and accessibility checks — all generated automatically.

---

## Quick Start

### Prerequisites

- Python 3.13+
- An Anthropic API key ([get one here](https://console.anthropic.com))
- Chromium (installed automatically by Playwright)

### 1. Clone and install

```bash
git clone https://github.com/wise9sol/9mindtech-quality-engineering-framework.git
cd 9mindtech-quality-engineering-framework
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-...
BASE_URL=https://your-app.com
API_BASE_URL=https://api.your-app.com
TEST_EMAIL=test@example.com
TEST_PASSWORD=your-test-password
```

### 3. Start the API server

```bash
python api_server.py
# Server running at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### 4. Run the existing test suite

```bash
# Smoke tests (fast, critical path)
pytest -m smoke -v

# API tests
pytest -m api -v

# Full regression suite
pytest -m regression -n auto
```

---

## API Reference

The QualiOps API accepts plain-English test specifications and returns test results asynchronously. All endpoints are documented interactively at `http://localhost:8000/docs`.

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Service health and available endpoints |
| `POST` | `/run` | Execute a test suite from a natural language spec |
| `GET` | `/status/{run_id}` | Poll the status of a test run |
| `GET` | `/report/{run_id}` | Retrieve the JSON test report |
| `POST` | `/translate` | Preview generated code without executing |

---

### POST /run — Start a Test Run

Submit a plain-English test specification. The API queues the run and returns a `run_id` immediately — tests execute in the background.

**Request**

```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "acme-corp",
    "test_spec": "Test that a user can log in with valid credentials and reach the secure area",
    "webhook_url": "https://your-app.com/webhooks/test-complete"
  }'
```

**Response**

```json
{
  "run_id": "a3f8c1d2",
  "status": "queued",
  "message": "Test run queued. Poll /status/a3f8c1d2 for results."
}
```

---

### GET /status/{run_id} — Poll Run Status

```bash
curl http://localhost:8000/status/a3f8c1d2
```

**Response (completed)**

```json
{
  "status": "passed",
  "client_id": "acme-corp",
  "started_at": "2026-05-13T10:22:01.443Z",
  "completed_at": "2026-05-13T10:22:34.891Z",
  "stdout": "8 passed in 32.44s",
  "report_path": "reports/allure-results/a3f8c1d2"
}
```

Possible status values: `queued` → `running` → `passed` | `failed` | `error` | `timeout`

---

### POST /translate — Preview Code Generation

See exactly what code QualiOps would generate for each step — without executing anything.

**Request**

```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{
    "steps": [
      {"step": "Navigate to the login page"},
      {"step": "Enter valid username and password"},
      {"step": "Click the login button"}
    ]
  }'
```

**Response**

```json
{
  "translations": [
    {
      "original": "Navigate to the login page",
      "generated_code": "login_page.navigate('https://the-internet.herokuapp.com/login')"
    },
    {
      "original": "Enter valid username and password",
      "generated_code": "login_page.login('tomsmith', 'SuperSecretPassword!')"
    },
    {
      "original": "Click the login button",
      "generated_code": "login_page.click(login_page.login_button)"
    }
  ]
}
```

---

## Deployment

### Option A — Docker (Recommended)

```bash
# Build the image
docker build -t qualiops-ai .

# Run with environment variables
docker run -d \
  -p 8000:8000 \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  -e BASE_URL=https://your-app.com \
  --name qualiops \
  qualiops-ai
```

The API is live at `http://localhost:8000`. Swagger docs at `http://localhost:8000/docs`.

### Option B — Direct Python

```bash
# Production server with Uvicorn (multiple workers)
pip install uvicorn[standard]
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4
```

### Option C — CI/CD Integration (GitHub Actions)

Add QualiOps to your existing pipeline by calling the API from any CI step:

```yaml
- name: Run QualiOps AI Tests
  run: |
    RUN_ID=$(curl -s -X POST $QUALIOPS_URL/run \
      -H "Content-Type: application/json" \
      -d "{\"client_id\": \"$GITHUB_REPOSITORY\", \"test_spec\": \"$TEST_SPEC\"}" \
      | jq -r '.run_id')

    # Poll until complete
    while true; do
      STATUS=$(curl -s $QUALIOPS_URL/status/$RUN_ID | jq -r '.status')
      [ "$STATUS" != "queued" ] && [ "$STATUS" != "running" ] && break
      sleep 10
    done

    [ "$STATUS" = "passed" ] || exit 1
```

---

## What Gets Generated

From a single test spec, QualiOps produces a complete test file covering:

| Scenario Type | Examples |
|---|---|
| **Happy path** | Valid credentials, expected success state |
| **Authentication errors** | Wrong password, locked account, empty fields |
| **Edge cases** | SQL injection strings, Unicode, max-length inputs |
| **Session behaviour** | Login persistence, logout, concurrent sessions |
| **Performance** | Response time assertions (< 2000ms SLA) |
| **Accessibility** | Error message visibility, keyboard navigation |
| **Security** | Auth bypass attempts, credential exposure |
| **State transitions** | Redirect chains, URL verification |

All generated tests include `@pytest.mark.ai_generated`, datestamped docstrings, and conform to the project's naming conventions automatically.

---

## Client Testimonials

> *"QualiOps cut our test authoring time by 80%. We went from writing tests manually to describing features in plain English and having a full suite ready before the sprint ended."*
>
> — **Head of Engineering, SaaS Startup** *(coming soon)*

---

> *"The self-healing feature alone saved us three days of test maintenance after a major UI redesign. The audit log made it easy to review every change."*
>
> — **QA Lead, Scale-up** *(coming soon)*

---

*Are you an early adopter? [Book a demo](https://calendly.com/9mindtech_qa-automation-call) and your testimonial could appear here.*

---

## Pricing

| Plan | Who it's for | Price | Includes |
|------|-------------|-------|----------|
| **Starter** | Small teams, early-stage startups | £499/mo | 500 test runs/mo · API access · Email support |
| **Growth** | Scaling SaaS teams | £1,299/mo | Unlimited runs · Self-healing · Webhook callbacks · Slack support |
| **Enterprise** | Large orgs with compliance needs | Custom | SSO · On-premise · SLA · Dedicated engineer |
| **Audit** | One-time coverage review | £799 flat | Full QA audit + recommendations report |

All plans include a **14-day free trial**. No credit card required to start.

[Book a free 30-minute QA audit](https://calendly.com/9mindtech_qa-automation-call) — we'll review your current test coverage and show you exactly what's missing.

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.13 |
| Test Runner | pytest + pytest-xdist | 8.3.5 |
| Browser Automation | Playwright | 1.51.0 |
| API Framework | FastAPI | latest |
| AI Engine | Anthropic Claude Sonnet | latest |
| Reporting | Allure + pytest-html | latest |
| Containerisation | Docker | latest |
| CI/CD | GitHub Actions | ubuntu-latest |

---

## Contact

**9MindTech** — Elite QA Engineering for Startups and Scaling SaaS Teams

- **Book a demo**: [calendly.com/9mindtech_qa-automation-call](https://calendly.com/9mindtech_qa-automation-call)
- **Email**: [wise9mind.solutions@gmail.com](mailto:wise9mind.solutions@gmail.com)
- **GitHub**: [github.com/wise9sol](https://github.com/wise9sol)

---

<div align="center">

Built with precision by **9MindTech** · © 2026 · MIT License

</div>