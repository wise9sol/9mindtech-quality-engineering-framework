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

```python
def test_homepage(page):
    page.goto("https://example.com")
    assert page.title() == "Example Domain"

## Getting Started

Clone the repository:

```bash
git clone https://github.com/wise9sol/9mindtech-quality-engineering-framework.git
cd 9mindtech-quality-engineering-framework
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```

Run tests:

```bash
python -m pytest
```