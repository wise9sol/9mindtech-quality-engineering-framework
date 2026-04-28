"""
ai/client.py — 9MindTech AI Brain
Single Claude client instance for the entire framework.
NEVER instantiate Anthropic() anywhere else in this codebase.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

_client: Anthropic | None = None


def get_client() -> Anthropic:
    """
    Returns the singleton Anthropic client.
    Lazily initialized on first call.
    """
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY not set. Add it to your .env file."
            )
        _client = Anthropic(api_key=api_key)
    return _client


# Model — change only with team approval and CLAUDE.md update
CLAUDE_MODEL = "claude-sonnet-4-5"

# Token budgets per use case
TOKENS = {
    "test_generation": 2000,
    "self_healing": 1000,
    "failure_analysis": 1500,
    "code_review": 2000,
}
