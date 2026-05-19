"""
ai/client.py — 9MindTech AI Brain
Single Claude client instance for the entire framework.
NEVER instantiate Anthropic() anywhere else in this codebase.
"""

import os
import threading
from anthropic import Anthropic
from anthropic.types import Message, TextBlock
from dotenv import load_dotenv

load_dotenv()

_client: Anthropic | None = None
_client_lock = threading.Lock()


def get_client() -> Anthropic:
    """
    Returns the singleton Anthropic client.
    Lazily initialized on first call; double-checked locking for thread safety.
    """
    global _client
    if _client is None:
        with _client_lock:
            if _client is None:
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    raise EnvironmentError("ANTHROPIC_API_KEY not set. Add it to your .env file.")
                _client = Anthropic(api_key=api_key)
    return _client


def extract_text(response: Message) -> str:
    """Extract the text from the first content block of a Claude response."""
    content = response.content[0]
    assert isinstance(content, TextBlock), f"Expected TextBlock, got {type(content).__name__}"
    return content.text.strip()


# Model — change only with team approval and CLAUDE.md update
CLAUDE_MODEL = "claude-sonnet-4-6"

# Token budgets per use case
TOKENS = {
    "test_generation": 2000,
    "self_healing": 1000,
    "failure_analysis": 1000,
    "code_review": 2000,
}
