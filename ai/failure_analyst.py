"""
ai/failure_analyst.py — 9MindTech Failure Analyst
Reads Allure JSON results, identifies failing tests, and produces
a plain-English root cause analysis report saved to reports/ai_analysis/.
"""

import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from ai.client import get_client, CLAUDE_MODEL, TOKENS

OUTPUT_DIR = Path("reports/ai_analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_PROMPT = """You are a senior QA engineer performing root cause analysis for 9MindTech.

Given a list of failing test results from an Allure JSON report, produce a clear, 
actionable analysis. Be direct and specific — no fluff.

Structure your response EXACTLY like this (use these headers):

## Summary
One paragraph: how many tests failed, what areas are affected, overall severity.

## Root Causes
For each distinct root cause group:
- **[Root Cause Name]**: What is broken and why. Which tests are affected.

## Priority Fixes
Numbered list of specific actions the engineer should take, most critical first.
Each item: what to fix, which file/function, estimated effort (low/medium/high).

## Patterns to Watch
Any trends suggesting systemic issues (e.g., all API tests failing = env issue,
all login tests failing = auth regression, flaky timing = missing waits).
"""


@dataclass
class FailureReport:
    """Structured output from the failure analyst."""
    total_tests: int
    failed_count: int
    ai_analysis: str
    generated_at: str = ""
    report_path: str = ""

    def __post_init__(self):
        self.generated_at = datetime.now().isoformat()


@dataclass
class FailedTest:
    """Extracted data from a single failing Allure result."""
    name: str
    status: str
    error_message: str
    stack_trace: str
    labels: list[str] = field(default_factory=list)


def load_allure_results(results_dir: str = "reports/allure-results") -> list[FailedTest]:
    """
    Parse Allure JSON result files and extract failing tests.

    Args:
        results_dir: Path to Allure results directory

    Returns:
        List of FailedTest objects for failed/broken tests only
    """
    results_path = Path(results_dir)
    if not results_path.exists():
        raise FileNotFoundError(f"Allure results not found at: {results_dir}")

    failed = []
    for json_file in results_path.glob("*-result.json"):
        try:
            data = json.loads(json_file.read_text())
            if data.get("status") not in ("failed", "broken"):
                continue

            status_detail = data.get("statusDetails", {})
            labels = [label.get("value", "") for label in data.get("labels", [])]

            failed.append(FailedTest(
                name=data.get("fullName", data.get("name", "Unknown")),
                status=data.get("status", "unknown"),
                error_message=status_detail.get("message", "No error message"),
                stack_trace=status_detail.get("trace", "No stack trace")[:500],
                labels=labels,
            ))
        except (json.JSONDecodeError, KeyError):
            continue

    return failed


def analyze_failures(
    failed_tests: list[FailedTest],
    total_tests: int | None = None,
) -> FailureReport:
    """
    Run AI analysis on failing tests and generate a structured report.

    Args:
        failed_tests: List of FailedTest objects from load_allure_results()
        total_tests: Total test count for context (optional)

    Returns:
        FailureReport with AI analysis and saved report path
    """
    if not failed_tests:
        return FailureReport(
            total_tests=total_tests or 0,
            failed_count=0,
            ai_analysis="No failing tests found. All tests passed.",
        )

    client = get_client()
    total = total_tests or len(failed_tests)

    # Build a compact summary for the prompt
    failures_text = ""
    for i, test in enumerate(failed_tests[:20], 1):  # Cap at 20 to stay in token budget
        failures_text += f"""
--- Test {i} ---
Name: {test.name}
Status: {test.status}
Labels: {', '.join(test.labels)}
Error: {test.error_message[:300]}
Trace (excerpt): {test.stack_trace[:200]}
"""

    if len(failed_tests) > 20:
        failures_text += f"\n... and {len(failed_tests) - 20} more failures (truncated for analysis)"

    prompt = f"""Analyze these test failures from the 9MindTech QA suite.

Run stats: {len(failed_tests)} failed out of {total} total tests.

Failing tests:
{failures_text}

Provide root cause analysis following the required format.
"""

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=TOKENS["failure_analysis"],
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    analysis = response.content[0].text.strip()
    report = FailureReport(
        total_tests=total,
        failed_count=len(failed_tests),
        ai_analysis=analysis,
    )

    report.report_path = _save_report(report, failed_tests)
    return report


def _save_report(report: FailureReport, failed_tests: list[FailedTest]) -> str:
    """Save the analysis report to reports/ai_analysis/."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUTPUT_DIR / f"analysis_{timestamp}.md"

    content = f"""# 9MindTech — AI Failure Analysis
Generated: {report.generated_at}
Run: {report.failed_count} failed / {report.total_tests} total

---

{report.ai_analysis}

---

## Raw Failure List
| # | Test | Status | Error |
|---|------|--------|-------|
"""
    for i, t in enumerate(failed_tests, 1):
        error_short = t.error_message[:80].replace("|", "/")
        content += f"| {i} | `{t.name}` | {t.status} | {error_short} |\n"

    filename.write_text(content, encoding="utf-8")
    print(f"[Failure Analyst] Report saved → {filename}")
    return str(filename)


def run_analysis(results_dir: str = "reports/allure-results") -> FailureReport:
    """
    Full pipeline: load Allure results → analyze → save report.
    Call this after a test run to get an instant AI analysis.

    Args:
        results_dir: Path to Allure results directory

    Returns:
        FailureReport with analysis and file path
    """
    print("[Failure Analyst] Loading Allure results...")
    failed = load_allure_results(results_dir)
    print(f"[Failure Analyst] Found {len(failed)} failing tests")

    print("[Failure Analyst] Running AI analysis...")
    report = analyze_failures(failed)

    print("\n" + "="*60)
    print(report.ai_analysis)
    print("="*60 + "\n")

    return report


# ── CLI usage ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    results_dir = sys.argv[1] if len(sys.argv) > 1 else "reports/allure-results"
    run_analysis(results_dir)
