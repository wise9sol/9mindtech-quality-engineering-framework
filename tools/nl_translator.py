#!/usr/bin/env python3
# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""Natural language to page object translation — seed of the QualiOps NL-to-code feature."""

import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from ai.client import get_client, CLAUDE_MODEL, extract_text  # noqa: E402
from pages.login_page import LoginPage  # noqa: E402, F401
from pages.home_page import HomePage  # noqa: E402, F401


def translate_step_to_code(step_text: str, available_methods: list[str]) -> Optional[str]:
    """Use Claude to convert a plain English test step into a page object method call."""
    client = get_client()

    prompt = f"""You are a test automation expert. Convert this natural language test step into a Python method call.

Available methods (use only these):
{chr(10).join(f'- {m}' for m in available_methods)}

Step: "{step_text}"

Return ONLY the Python code. No explanations, no markdown, no backticks.
Example output: login_page.click_submit_button()"""

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}],
        )
        code = extract_text(response)
        return code.replace("```python", "").replace("```", "").strip()
    except Exception as e:
        print(f"Translation failed: {e}")
        return None


def main() -> None:
    """Demo: translate a natural language test step into a page object method call."""
    print("=" * 60)
    print("Natural Language Translator")
    print("=" * 60)

    available_methods = [
        "login_page.click_submit_button()",
        "login_page.enter_email('email@example.com')",
        "login_page.enter_password('secret')",
        "login_page.wait_for_login_success()",
        "home_page.verify_dashboard_visible()",
        "home_page.click_navigation_item('Trading')",
    ]

    test_step = "click submit"
    print(f"\nTranslating: '{test_step}'")
    generated_code = translate_step_to_code(test_step, available_methods)
    print(f"Generated:   {generated_code}")

    expected = "login_page.click_submit_button()"
    if generated_code and expected in generated_code:
        print("\nPASS - matched expected pattern")
    else:
        print(f"\nFAIL - expected pattern containing '{expected}'")
        print(f"Got: {generated_code}")


if __name__ == "__main__":
    main()
