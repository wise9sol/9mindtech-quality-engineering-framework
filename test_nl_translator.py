#!/usr/bin/env python3
"""
Test the natural language to page object translation.
This is the seed of your business.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from ai.client import get_client

# Import your actual page objects
from pages.login_page import LoginPage
from pages.home_page import HomePage


def translate_step_to_code(step_text: str, available_methods: list[str]) -> str:
    """
    Use Claude to convert plain English to a method call.

    Args:
        step_text: e.g., "click submit"
        available_methods: e.g., ["login_page.click_submit_button()",
                                   "login_page.enter_email('x')"]

    Returns:
        Python code string, e.g., "login_page.click_submit_button()"
    """
    client = get_client()

    prompt = f"""You are a test automation expert. Convert this natural language test step into a Python method call.

Available methods (use only these):
{chr(10).join(f'- {m}' for m in available_methods)}

Step: "{step_text}"

Return ONLY the Python code. No explanations, no markdown, no backticks.
Example output: login_page.click_submit_button()"""

    try:
        response = client.messages.create(
            model="claude-3-sonnet-20241022",
            max_tokens=100,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        code = response.content[0].text.strip()
        # Remove any markdown formatting if present
        code = code.replace("```python", "").replace("```", "").strip()
        return code
    except Exception as e:
        print(f"Translation failed: {e}")
        return None


def main():
    print("=" * 60)
    print("Testing Natural Language Translator")
    print("=" * 60)

    # Step 1: Define what methods actually exist in your page objects
    # Check your actual LoginPage class for real method names
    print("\n1. Checking available page object methods...")

    # Be honest about what methods you have. Examples:
    available_methods = [
        "login_page.click_submit_button()",
        "login_page.enter_email('email@example.com')",
        "login_page.enter_password('secret')",
        "login_page.wait_for_login_success()",
        "home_page.verify_dashboard_visible()",
        "home_page.click_navigation_item('Trading')"
    ]

    print(f"   Available: {', '.join(available_methods[:3])}...")

    # Step 2: Test simple translation
    test_step = "click submit"
    print(f"\n2. Translating: '{test_step}'")

    generated_code = translate_step_to_code(test_step, available_methods)
    print(f"   Generated: {generated_code}")

    # Step 3: Verify it matches something in your available methods
    print("\n3. Verification:")
    expected = "login_page.click_submit_button()"
    if generated_code and expected in generated_code:
        print(f"   ✅ PASS - Generated '{generated_code}' matches expected pattern")
    else:
        print(f"   ❌ FAIL - Expected pattern containing '{expected}'")
        print(f"   Got: {generated_code}")

    # Step 4: Show how this would execute in a real test
    print("\n" + "=" * 60)
    print("HOW THIS INTEGRATES WITH YOUR EXISTING TESTS")
    print("=" * 60)

    print("""
    # In your actual test file (e.g., tests/ui/test_ai_generated.py):

    import pytest
    from pages.login_page import LoginPage

    @pytest.mark.ai_generated
    def test_ai_translated_login(page):
        login_page = LoginPage(page)

        # Instead of writing this manually:
        # login_page.enter_email("user@example.com")
        # login_page.enter_password("pass123")
        # login_page.click_submit_button()

        # Your AI translator would generate it:
        steps = [
            ("fill email: user@example.com", "login_page.enter_email('user@example.com')"),
            ("fill password: pass123", "login_page.enter_password('pass123')"),
            ("click submit", "login_page.click_submit_button()"),
        ]

        for step_text, generated_code in steps:
            print(f"Step: {step_text}")
            print(f"Code: {generated_code}")
            exec(generated_code)  # Only if you trust the source!
    """)

    print("\n✅ Translation test complete.")
    print("\nNext step: Integrate this with your AI test generator at:")
    print("   ai/test_generator.py")


if __name__ == "__main__":
    main()