![Tests](https://github.com/wise9sol/9mindtech-quality-engineering-framework/actions/workflows/tests.yml/badge.svg)


# 9MindTech Quality Engineering Framework

Designed for modern applications where reliability under real-world conditions is critical.

Built to simulate real user environments and uncover issues traditional automation often misses.

A modern automation testing framework built with Python, Pytest, Playwright, and API testing to ensure application reliability across functional and real-world conditions.

This framework demonstrates a scalable **Quality Engineering architecture** that supports UI automation, API validation, automated reporting, and continuous integration.

---

# Overview

This framework is designed to ensure application reliability across both functional and real-world network conditions.

## Who This Framework Is For

- Startups building web applications
- Teams needing reliable CI/CD test automation
- Products sensitive to network conditions (FinTech, HealthTech, SaaS)

## Value Proposition

This framework helps teams proactively identify real-world reliability issues before they impact users, reducing production failures and improving user experience.

The 9MindTech Quality Engineering Framework provides an automated testing foundation that validates applications across multiple layers:

- UI Automation Testing
- API Testing
- Network Reliability Testing
- Continuous Integration Testing

---

# Core Technologies

| Technology | Purpose |
|-------------|--------|
| Python | Core programming language |
| Pytest | Test execution framework |
| Playwright | Browser automation |
| Requests | API testing |
| Pytest-HTML | Test reporting |
| GitHub Actions | Continuous integration |

---

# Key Features

## UI Automation

Browser automation powered by **Playwright**.

Tests validate:

- Page loading
- Navigation flows
- User interface behavior

### Example UI Test

```python
def test_homepage(page):
    page.goto("https://example.com")
    assert page.title() == "Example Domain"
```

---
## API Testing

API validation using Python requests.

Tests verify:

- Response status codes
- Data integrity
- API reliability


---

## Network Reliability Testing (Advanced)

This framework includes real-world network condition testing, a critical capability for modern applications.

Test scenarios include:

- Normal network baseline
- Slow network simulation (3G conditions)
- Offline behavior testing

Artifacts generated:

- Screenshots
- Playwright trace files
- HTML reports

### Use Case

Validate whether critical user flows (login, checkout, payments) remain reliable under unstable or degraded network conditions that real users experience.

---
# Getting Started

Run the framework locally or integrate it into your CI pipeline to begin identifying reliability issues in your application.

## Clone the Repository

```bash
git clone https://github.com/wise9sol/9mindtech-quality-engineering-framework.git
cd 9mindtech-quality-engineering-framework
```
---
## Create Virtual Environment
```bash
python -m venv .venv
```
---
## Activate (Windows PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```
---
## Install Dependencies

```bash
pip install -r requirements.txt
playwright install
```
---

## Run Tests

```bash
pytest
```
---
## Run Network Tests Only

```bash
pytest -m network --browser chromium
```
---

# Framework Architecture
```
9mindtech-quality-engineering-framework
├── tests
│   ├── ui
│   ├── api
│   └── network
│
├── utils
├── reports
├── artifacts
│
├── conftest.py
├── pytest.ini
├── requirements.txt
```
---
# Reporting
## HTML Report
Generated automatically:
```
reports/report.html
```
---
## Allure Report (Optional)





```bash
pytest --alluredir=allure-results
allure serve allure-results
```
---

## Advanced Capabilities

- UI automation with Playwright
- API testing
- Network condition simulation
- Automatic screenshots on failure
- Playwright trace capture
- Structured logging
- Test markers (smoke, regression, api, network)
- GitHub Actions CI pipeline
- Docker execution support
- Detection of real-world user failure scenarios (slow, unstable, offline networks)
- Scalable test architecture for growing applications


---
## AI-Assisted Test Planning
Generates test ideas from feature descriptions:

```bash
python tools/test_idea_generator.py
```
---
## Why This Framework Matters

Modern applications often fail under real-world conditions such as:

- Slow networks
- Unstable connections
- Offline scenarios

## Real-World Impact

This framework is designed to simulate real user environments, helping teams detect issues that traditional test automation often misses.

---
# Example Output

The framework generates:

- HTML reports (`reports/report.html`)
- Screenshots of failures
- Playwright trace files for debugging
- These outputs provide clear visibility into application behavior under real-world conditions and support faster debugging and issue resolution.

These outputs provide clear visibility into application behavior under real-world conditions.

---
## License

This project is part of the **9MindTech Quality Engineering initiative**.