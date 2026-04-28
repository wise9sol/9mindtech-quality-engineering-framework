"""
ai/test_generator.py — 9MindTech Test Generator
Generates pytest test cases from Page Object classes or API endpoint specs.
All generated tests get @pytest.mark.ai_generated and a docstring with the date.
"""

import re
from datetime import date
from pathlib import Path
from ai.client import get_client, CLAUDE_MODEL, TOKENS

SYSTEM_PROMPT = """You are an elite QA automation engineer working inside the 9MindTech framework.

RULES — follow exactly:
1. Output ONLY valid Python code. No explanation, no markdown fences.
2. Every test function name follows: test_[action]_[expected_outcome]_[condition_if_needed]
3. Every test gets @pytest.mark.ai_generated decorator.
4. Every test gets a one-line docstring: "AI generated: {today}. Tests [what it tests]."
5. Import pytest and any page/fixture needed at the top.
6. Use Playwright expect() for assertions — never assert directly on page state.
7. No time.sleep() — ever.
8. Group tests by logical scenario using pytest classes if >4 tests for one feature.
9. Add @pytest.mark.smoke to critical path tests, @pytest.mark.regression to edge cases.
10. Never hardcode URLs or credentials — use fixtures that read from .env.
"""


def generate_ui_tests(page_object_source: str, feature_name: str) -> str:
    """
    Generate UI test cases from a Page Object class source code.

    Args:
        page_object_source: The full source code of the Page Object class
        feature_name: Human-readable name of the feature (e.g., "Login", "Checkout")

    Returns:
        Generated pytest test file content as a string
    """
    client = get_client()
    today = date.today().isoformat()

    prompt = f"""Generate comprehensive pytest UI tests for the {feature_name} feature.

Page Object source:
```python
{page_object_source}
```

Generate tests covering:
- Happy path (valid inputs, expected success)
- Sad path (invalid inputs, expected errors)
- Edge cases (empty fields, boundary values, special characters)
- Accessibility basics (tab order works, error messages visible)

Today's date for docstrings: {today}
"""

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=TOKENS["test_generation"],
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    return _clean_code_fences(raw)


def generate_api_tests(endpoint_spec: str, feature_name: str) -> str:
    """
    Generate API test cases from an endpoint specification.

    Args:
        endpoint_spec: Description or OpenAPI/JSON spec of the endpoint(s)
        feature_name: Human-readable name (e.g., "User Auth API", "Orders API")

    Returns:
        Generated pytest test file content as a string
    """
    client = get_client()
    today = date.today().isoformat()

    prompt = f"""Generate comprehensive pytest API tests for: {feature_name}

Endpoint specification:
{endpoint_spec}

Generate tests covering:
- All HTTP methods defined in the spec
- Valid payload → assert status code, response schema, response time < 2000ms
- Invalid/missing fields → assert correct 4xx status
- Auth edge cases (missing token, expired token, wrong permissions)
- Boundary values for numeric and string fields

Today's date for docstrings: {today}
"""

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=TOKENS["test_generation"],
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    return _clean_code_fences(raw)


def save_generated_tests(content: str, output_path: str) -> Path:
    """
    Save generated test content to a file.

    Args:
        content: The generated Python test code
        output_path: Relative path inside tests/ (e.g., "ui/test_login_generated.py")

    Returns:
        Path object of the saved file
    """
    path = Path("tests") / output_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"[AI Generator] Saved → {path}")
    return path


def _clean_code_fences(text: str) -> str:
    """Strip markdown code fences if the model included them."""
    return re.sub(r"^```(?:python)?\n?|```$", "", text, flags=re.MULTILINE).strip()


# ── CLI usage ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python -m ai.test_generator <page_object_file> <feature_name>")
        sys.exit(1)

    source_file = Path(sys.argv[1]).read_text()
    feature = sys.argv[2]

    print(f"[AI Generator] Generating UI tests for: {feature}")
    tests = generate_ui_tests(source_file, feature)

    output = f"ui/test_{feature.lower().replace(' ', '_')}_generated.py"
    save_generated_tests(tests, output)
    print("[AI Generator] Done.")
