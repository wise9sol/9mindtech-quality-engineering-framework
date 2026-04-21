
![CI](https://github.com/wise9sol/9mindtech-quality-engineering-framework/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Playwright](https://img.shields.io/badge/playwright-latest-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

# 9MindTech Quality Engineering Framework

A production-ready test automation framework for teams that ship fast and break nothing. Built and maintained by [9MindTech](https://github.com/wise9sol) — QA consulting for startups and scaling SaaS teams.

---

## Who This Is For

- SaaS startups shipping frequently
- Teams relying on manual testing
- Products where bugs impact users and revenue
- Teams needing CI-ready automation fast

---

## What This Solves

Most teams catch bugs too late — after they've already hit production. This framework shifts testing left, automating critical user flows so bugs are caught before release, not after.

---

## What's in the Box

| Layer | Technology | Coverage |
|---|---|---|
| UI / Browser | Playwright + Page Object Model | Login, auth flows, core user journeys |
| API | pytest + requests | Status, schema, CRUD, data integrity |
| Network | Playwright | Offline and slow network scenarios |
| CI/CD | GitHub Actions | Runs on every push |
| Reporting | pytest-html + Allure | HTML report uploaded as artifact |

---

## Get Running in 5 Minutes

**1. Clone and install**

```bash
git clone https://github.com/wise9sol/9mindtech-quality-engineering-framework.git
cd 9mindtech-quality-engineering-framework
pip install -r requirements.txt
playwright install chromium
```

**2. Run the full suite**

```bash
pytest
```

**3. Run just API tests (no browser needed)**

```bash
pytest tests/api/ -v
```

**4. Run just UI tests**

```bash
pytest tests/ui/ -v
```

**5. View the HTML report**

After any test run, open `reports/report.html` in your browser.

---

## Project Structure

```
├── conftest.py                  # Shared fixtures: browser, API session, test data
├── pytest.ini                   # Test runner config, markers, reporting
├── requirements.txt             # Pinned dependencies for reproducible CI
│
├── pages/                       # Page Object Model
│   ├── base_page.py             # Base class: wait strategies, screenshot on failure
│   └── playwright_docs_page.py  # Example page object (swap for your app)
│
├── tests/
│   ├── ui/
│   │   ├── test_login.py            # Smoke: homepage load, core UI elements
│   │   ├── test_page_load.py        # Page title, navbar, heading, content
│   │   ├── test_navigation.py       # Search, links, broken images
│   │   └── test_responsive.py       # Mobile, tablet, desktop viewports
│   ├── api/
│   │   ├── test_api_status.py       # API health check
│   │   ├── test_get_requests.py     # GET: status, schema, performance SLA
│   │   ├── test_write_operations.py # POST/PUT/PATCH/DELETE: full CRUD
│   │   └── test_data_integrity.py   # FK integrity, uniqueness, edge cases
│   └── network/
│       ├── test_normal_login.py     # Standard network conditions
│       ├── test_offline_login.py    # Offline behaviour
│       └── test_slow_login.py       # Throttled network conditions
│
└── .github/
    └── workflows/tests.yml      # CI pipeline: test, report, artifact upload
```

---

## Tech Stack

- Python 3.11
- pytest
- Playwright
- requests
- GitHub Actions
- pytest-html / Allure

---

## Adapting to Your Application

This framework is designed to be dropped onto any web app or API in under an hour.

**To test your own UI:** Copy `pages/playwright_docs_page.py`, rename it, and replace the selectors and URL. The `BasePage` class handles all wait logic — you just define locators.

**To test your own API:** Update `BASE_URL` in `conftest.py` to your staging environment. The API test structure works against any REST API.

**Environment variables for CI:**

```bash
export BASE_URL=https://staging.yourapp.com/api
export UI_BASE_URL=https://staging.yourapp.com
pytest
```

---

## Work With Us

This framework is open source and free to use. If you want it set up, customised, and integrated into your pipeline by the team that built it:

Book a free 30-minute QA audit — we'll review your current test coverage and show you exactly what's missing.

- - Calendly: https://calendly.com/9mindtech_qa-automation-call
- Email: wise9mind.solutions@gmail.com

> 9MindTech specialises in building quality engineering systems for startups and scaling SaaS teams. We set up frameworks like this, integrate them into your pipeline, and train your team to maintain them.