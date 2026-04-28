"""
ai/ — 9MindTech AI Brain
Single Anthropic SDK integration point for the entire framework.

Quick reference:
    from ai.test_generator import generate_ui_tests, generate_api_tests
    from ai.self_healer import heal_and_apply, heal_locator
    from ai.failure_analyst import run_analysis
"""

from ai.client import get_client, CLAUDE_MODEL, TOKENS
from ai.test_generator import generate_ui_tests, generate_api_tests, save_generated_tests
from ai.self_healer import heal_locator, heal_and_apply
from ai.failure_analyst import run_analysis, load_allure_results, analyze_failures

__all__ = [
    "get_client",
    "CLAUDE_MODEL",
    "TOKENS",
    "generate_ui_tests",
    "generate_api_tests",
    "save_generated_tests",
    "heal_locator",
    "heal_and_apply",
    "run_analysis",
    "load_allure_results",
    "analyze_failures",
]
