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
```

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

Activate the virtual environment (Windows PowerShell):

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

## AI-Assisted Test Planning

This framework includes a simple AI-assisted tool for generating test ideas from feature descriptions.

Example:

```bash
python tools/test_idea_generator.py
```

This helps accelerate test planning while keeping human review in the loop.