"""
ai/self_healer.py — 9MindTech Self-Healing Locator Agent
When a Playwright locator fails, this agent analyzes the page HTML
and suggests 3 alternative locators ranked by reliability.
All changes are logged to reports/healer.log.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from ai.client import get_client, CLAUDE_MODEL, TOKENS

# ── Logging setup ──────────────────────────────────────────────────────────────
LOG_PATH = Path("reports/healer.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format="%(asctime)s [HEALER] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
healer_log = logging.getLogger("self_healer")


@dataclass
class HealedLocator:
    """Result from the self-healing agent."""
    original: str
    suggested: list[str]          # Ranked best → worst
    confidence: str               # "high" | "medium" | "low"
    reasoning: str
    timestamp: str = ""

    def __post_init__(self):
        self.timestamp = datetime.now().isoformat()

    def best(self) -> str:
        """Return the top-ranked locator suggestion."""
        return self.suggested[0] if self.suggested else self.original


SYSTEM_PROMPT = """You are a Playwright locator expert for the 9MindTech QA framework.

Your job: given a broken locator and the current page HTML snapshot, suggest 3 replacement 
locators ranked best to worst by reliability.

Locator reliability ranking (prefer in this order):
1. data-testid attributes — most stable, purpose-built for testing
2. ARIA roles + accessible name — semantic, resistant to UI changes
3. Unique text content — readable but brittle to copy changes
4. CSS class — only if unique and not utility/generated class
5. XPath — last resort only

NEVER suggest:
- Position-based locators (nth-child, first-of-type for non-list items)
- Locators containing generated hash classes (e.g., "css-a8j2k")
- Locators with hardcoded indices unless the element is in a known list

Respond ONLY with valid JSON in this exact shape:
{
  "suggested": ["locator1", "locator2", "locator3"],
  "confidence": "high|medium|low",
  "reasoning": "One sentence explaining why the original failed and why locator1 is best."
}
"""


def heal_locator(
    broken_locator: str,
    page_html_snapshot: str,
    element_description: str = "",
) -> HealedLocator:
    """
    Analyze a broken Playwright locator and return healed alternatives.

    Args:
        broken_locator: The locator string that failed (e.g., "[data-testid='old-btn']")
        page_html_snapshot: Relevant HTML section from the page (trim to ~500 lines)
        element_description: Human description of the element (e.g., "Submit button on login form")

    Returns:
        HealedLocator dataclass with ranked suggestions
    """
    client = get_client()

    context = f"Element description: {element_description}\n" if element_description else ""

    prompt = f"""{context}Broken locator: {broken_locator}

Page HTML snapshot:
```html
{page_html_snapshot[:8000]}
```

Suggest 3 replacement locators."""

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=TOKENS["self_healing"],
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = response.content[0].text.strip()
        data = json.loads(raw)

        result = HealedLocator(
            original=broken_locator,
            suggested=data.get("suggested", []),
            confidence=data.get("confidence", "low"),
            reasoning=data.get("reasoning", ""),
        )

        healer_log.info(
            f"HEALED | original={broken_locator!r} | "
            f"best={result.best()!r} | confidence={result.confidence} | "
            f"reason={result.reasoning}"
        )
        return result

    except (json.JSONDecodeError, KeyError) as e:
        healer_log.error(f"FAILED | original={broken_locator!r} | error={e}")
        return HealedLocator(
            original=broken_locator,
            suggested=[broken_locator],
            confidence="low",
            reasoning=f"Healing failed: {e}",
        )


def heal_and_apply(page, broken_locator: str, element_description: str = "") -> str:
    """
    Playwright-integrated healing. Gets the page HTML, heals the locator,
    tries each suggestion, and returns the first one that resolves successfully.

    Args:
        page: Playwright Page object
        broken_locator: The locator that failed
        element_description: Human description of the element

    Returns:
        Working locator string, or original if all suggestions fail
    """
    html_snapshot = page.content()
    result = heal_locator(broken_locator, html_snapshot, element_description)

    for locator in result.suggested:
        try:
            count = page.locator(locator).count()
            if count == 1:
                healer_log.info(f"APPLIED | {broken_locator!r} → {locator!r}")
                print(f"[Self-Healer] Fixed: {broken_locator!r} → {locator!r} (confidence: {result.confidence})")
                return locator
            elif count > 1:
                healer_log.warning(f"AMBIGUOUS | {locator!r} matched {count} elements, skipping")
        except Exception as e:
            healer_log.warning(f"UNUSABLE | {locator!r} | error={e}")

    healer_log.error(f"NO_FIX | all suggestions failed for {broken_locator!r}")
    print(f"[Self-Healer] Could not heal: {broken_locator!r} — check reports/healer.log")
    return broken_locator


# ── Pytest plugin hook — auto-heal on locator failure ─────────────────────────
class SelfHealingPlugin:
    """
    Pytest plugin that intercepts Playwright TimeoutErrors and attempts healing.

    Usage in conftest.py:
        from ai.self_healer import SelfHealingPlugin
        pytest_plugins = [SelfHealingPlugin()]
    """

    def pytest_runtest_logreport(self, report):
        if report.failed and "TimeoutError" in str(report.longrepr):
            healer_log.warning(
                f"TEST FAILED with TimeoutError: {report.nodeid} — "
                "Consider using heal_and_apply() around flaky locators."
            )
