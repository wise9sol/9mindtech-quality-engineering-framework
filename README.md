![Tests](https://github.com/wise9sol/9mindtech-quality-engineering-framework/actions/workflows/tests.yml/badge.svg)

# 9MindTech Quality Engineering Framework

A modern automation testing framework built with **Python, Pytest, Playwright, and API testing**.

This framework demonstrates a scalable **Quality Engineering architecture** that supports UI automation, API validation, automated reporting, and continuous integration.

---

# Overview

The **9MindTech Quality Engineering Framework** provides an automated testing foundation designed to help software teams deliver reliable applications faster.

The framework validates software across multiple layers:

- User Interface Testing
- API Testing
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

- page loading
- navigation flows
- user interface behavior

Example UI test:
# 9MindTech Quality Engineering Framework

A modern automation testing framework built with **Python, Pytest, Playwright, and API testing**.

This framework demonstrates a scalable **Quality Engineering architecture** that supports UI automation, API validation, automated reporting, and continuous integration.

---

# Overview

The **9MindTech Quality Engineering Framework** provides an automated testing foundation designed to help software teams deliver reliable applications faster.

The framework validates software across multiple layers:

- User Interface Testing
- API Testing
- Continuous Integration Testing

---

# Core Technologies

| Technology | Purpose |
|-----------|--------|
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

# Getting Started

## Clone the Repository

```bash
git clone https://github.com/wise9sol/9mindtech-quality-engineering-framework.git
cd 9mindtech-quality-engineering-framework
```

## Create a Virtual Environment

```bash
python -m venv .venv
```

## Activate the Virtual Environment (Windows PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

## Install Dependencies

```bash
pip install -r requirements.txt
playwright install
```

## Run Tests

```bash
python -m pytest
```

---

# AI-Assisted Test Planning

This framework includes a simple **AI-assisted tool for generating test ideas from feature descriptions**.

Example:

```bash
python tools/test_idea_generator.py
```

This helps accelerate test planning while keeping **human review in the loop**.

---

## Allure Reporting

This framework supports Allure reporting for interactive test result visualization.

Run tests with Allure results:

```bash
python -m pytest --alluredir=allure-results
```

Open the Allure report:

```bash
allure serve allure-results
```

# Framework Capabilities

This framework includes:

- UI automation with Playwright
- API testing
- Parallel test execution
- Automatic screenshots on test failure
- Environment configuration with `.env`
- Structured logging
- Test markers (`smoke`, `regression`, `api`)
- Docker test execution
- GitHub Actions CI pipeline
- AI-assisted test planning
- Allure reporting

---

# License

This project is part of the **9MindTech Quality Engineering initiative**.