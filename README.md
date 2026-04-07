![Tests](https://github.com/wise9sol/9mindtech-quality-engineering-framework/actions/workflows/tests.yml/badge.svg)


# 🚀 9MindTech Quality Engineering Framework

This framework helps teams reduce release bugs by automating critical user flows before production.

QA Automation framework designed to help fast-moving software teams reduce bugs before release.

Built using Python, Pytest, and Playwright to automate critical user flows and improve release confidence.

---

## 🎯 Who This Is For

- SaaS startups shipping frequently  
- Teams relying on manual testing  
- Products where bugs impact users and revenue  
- Teams needing CI-ready automation  

---

## ⚡ What This Solves

Many teams:
- spend too much time on manual testing  
- miss critical bugs before release  
- lack a reliable automation strategy  

This framework provides a **practical automation foundation** to solve those problems quickly.

---

## 📦 What This Framework Does

- UI automation with Playwright  
- API testing support  
- Smoke and regression test suites  
- Automated reporting with artifacts  
- CI integration with GitHub Actions  

---

## 🧪 Example Test Coverage

- Login / Logout  
- Authentication flows  
- Core user journeys  
- Basic regression scenarios  

---

## 🛠 Tech Stack

- Python  
- Pytest  
- Playwright  
- GitHub Actions  

---

## ⚙️ Quick Start

```bash
pip install -r requirements.txt
playwright install
pytest -m smoke
```
---
## 📊 Test Artifacts

- Screenshots on failure  
- Playwright traces  
- HTML reports  

---

## 📸 Sample Test Results

![HTML Test Report](test-report.png)

- Test execution results  
- Failure screenshots  
- HTML reports  
- Playwright traces  

---

## 🔁 CI Integration

Tests run automatically using GitHub Actions to ensure continuous validation.

---

## 💼 Work With 9MindTech

Need QA automation for your product?

I help teams:
- reduce bugs before release  
- automate critical workflows  
- eliminate repetitive testing  
- build scalable QA systems  

📧 wise9mind.solutions@gmail.com  
📅 https://calendly.com/9mindtech_qa-automation-call

---

## 🔥 Why 9MindTech

- Focus on real-world reliability, not just test scripts  
- Built for speed and practical implementation  
- Designed to deliver immediate business value  

---

## 🧭 Mission
Build systems that catch issues before your users do.


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