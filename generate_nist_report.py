# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""Generate a NIST 800-53 control-coverage report (HTML + PDF).

The framework registers one ``nist_<control>`` marker per NIST 800-53 control
in ``conftest.py`` and exercises each control with one or more tests in
``tests/compliance/``. This tool reconciles the two -- the registered markers
(what the framework *claims* to cover) against the markers actually used by
tests (what it *does* cover) -- and renders the result as a standalone HTML
page and a PDF suitable for client delivery.

Usage:
    python generate_nist_report.py --out-dir reports/nist-coverage
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
CONFTEST = ROOT / "conftest.py"
COMPLIANCE_DIR = ROOT / "tests" / "compliance"

# "nist_ac2: NIST 800-53 AC-2 Account Management"
_MARKER_RE = re.compile(r'"(nist_[a-z0-9]+):\s*NIST 800-53\s+([A-Z]+)-(\d+)\s+(.+?)"')
_USAGE_RE = re.compile(r"pytest\.mark\.(nist_[a-z0-9]+)")


@dataclass
class Control:
    """A single NIST 800-53 control and its test coverage."""

    marker: str
    family: str
    number: int
    title: str
    test_count: int = 0
    files: List[str] = field(default_factory=list)

    @property
    def control_id(self) -> str:
        """Return the canonical control identifier, e.g. ``AC-2``."""
        return f"{self.family}-{self.number}"

    @property
    def covered(self) -> bool:
        """Return True when at least one test exercises this control."""
        return self.test_count > 0


def parse_registered_controls(conftest: Path) -> Dict[str, Control]:
    """Parse ``nist_*`` marker registrations from conftest.py."""
    text = conftest.read_text(encoding="utf-8")
    controls: Dict[str, Control] = {}
    for marker, family, number, title in _MARKER_RE.findall(text):
        controls[marker] = Control(
            marker=marker,
            family=family,
            number=int(number),
            title=title.strip(),
        )
    return controls


def scan_test_usage(compliance_dir: Path) -> Dict[str, List[str]]:
    """Map each ``nist_*`` marker to the test files that use it."""
    usage: Dict[str, List[str]] = defaultdict(list)
    for path in sorted(compliance_dir.glob("test_*.py")):
        text = path.read_text(encoding="utf-8")
        for marker in _USAGE_RE.findall(text):
            usage[marker].append(path.name)
    return usage


def build_coverage(controls: Dict[str, Control], usage: Dict[str, List[str]]) -> List[Control]:
    """Fold test usage into the registered controls and return them sorted."""
    for marker, files in usage.items():
        control = controls.get(marker)
        if control is None:
            # Marker used by a test but never registered in conftest.py.
            controls[marker] = Control(
                marker=marker,
                family="UNREGISTERED",
                number=0,
                title=f"{marker} -- used by tests but not registered",
                test_count=len(files),
                files=sorted(set(files)),
            )
            continue
        control.test_count = len(files)
        control.files = sorted(set(files))
    return sorted(controls.values(), key=lambda c: (c.family, c.number, c.marker))


@dataclass
class Summary:
    """Top-line coverage figures for the report header."""

    total_controls: int
    covered_controls: int
    total_tests: int
    families: int

    @property
    def coverage_pct(self) -> float:
        """Percentage of registered controls with at least one test."""
        if self.total_controls == 0:
            return 0.0
        return 100.0 * self.covered_controls / self.total_controls


def summarize(controls: List[Control]) -> Summary:
    """Compute top-line figures across all controls."""
    return Summary(
        total_controls=len(controls),
        covered_controls=sum(1 for c in controls if c.covered),
        total_tests=sum(c.test_count for c in controls),
        families=len({c.family for c in controls}),
    )


def _group_by_family(controls: List[Control]) -> Dict[str, List[Control]]:
    grouped: Dict[str, List[Control]] = defaultdict(list)
    for control in controls:
        grouped[control.family].append(control)
    return grouped


# ── HTML rendering ──────────────────────────────────────────────────────────

_HTML_STYLE = """
  body { font-family: -apple-system, Segoe UI, Roboto, sans-serif;
         margin: 2rem auto; max-width: 980px; color: #1a1a2e; }
  h1 { margin-bottom: 0.25rem; }
  .sub { color: #555; margin-top: 0; }
  .cards { display: flex; gap: 1rem; margin: 1.5rem 0; flex-wrap: wrap; }
  .card { flex: 1; min-width: 150px; background: #f4f6fb;
          border: 1px solid #e0e4ee; border-radius: 10px; padding: 1rem; }
  .card .n { font-size: 2rem; font-weight: 700; color: #2d3a8c; }
  .card .l { color: #555; font-size: 0.85rem; text-transform: uppercase;
             letter-spacing: 0.05em; }
  h2 { margin-top: 2rem; border-bottom: 2px solid #2d3a8c;
       padding-bottom: 0.25rem; }
  table { border-collapse: collapse; width: 100%; margin-top: 0.5rem; }
  th, td { text-align: left; padding: 0.5rem 0.75rem;
           border-bottom: 1px solid #e6e6ee; font-size: 0.9rem; }
  th { background: #2d3a8c; color: #fff; }
  .covered { color: #1a7f37; font-weight: 600; }
  .gap { color: #b30000; font-weight: 600; }
  footer { margin-top: 2.5rem; color: #888; font-size: 0.8rem; }
"""


def render_html(controls: List[Control], summary: Summary, ts: str) -> str:
    """Render the coverage report as a standalone HTML document."""
    rows = []
    for family, items in _group_by_family(controls).items():
        rows.append(f"<h2>{family} &mdash; {len(items)} control(s)</h2>")
        rows.append("<table><thead><tr>")
        rows.append(
            "<th>Control</th><th>Title</th><th>Tests</th>" "<th>Status</th><th>Test files</th></tr></thead><tbody>"
        )
        for c in items:
            status = '<span class="covered">COVERED</span>' if c.covered else '<span class="gap">NO COVERAGE</span>'
            files = ", ".join(c.files) if c.files else "&mdash;"
            rows.append(
                f"<tr><td><b>{c.control_id}</b></td><td>{c.title}</td>"
                f"<td>{c.test_count}</td><td>{status}</td>"
                f"<td>{files}</td></tr>"
            )
        rows.append("</tbody></table>")

    cards = (
        f'<div class="card"><div class="n">{summary.total_controls}</div>'
        '<div class="l">Controls</div></div>'
        f'<div class="card"><div class="n">{summary.covered_controls}</div>'
        '<div class="l">Covered</div></div>'
        f'<div class="card"><div class="n">{summary.coverage_pct:.0f}%</div>'
        '<div class="l">Coverage</div></div>'
        f'<div class="card"><div class="n">{summary.total_tests}</div>'
        '<div class="l">Tests</div></div>'
        f'<div class="card"><div class="n">{summary.families}</div>'
        '<div class="l">Families</div></div>'
    )

    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>NIST 800-53 Coverage Report</title>"
        f"<style>{_HTML_STYLE}</style></head><body>"
        "<h1>NIST 800-53 Control Coverage</h1>"
        "<p class='sub'>9MindTech Quality Engineering Framework"
        f" &middot; generated {ts}</p>"
        f'<div class="cards">{cards}</div>'
        f"{''.join(rows)}"
        "<footer>&copy; 2026 Wise 9 Mind Solutions LLC. "
        "Generated by generate_nist_report.py.</footer>"
        "</body></html>"
    )


# ── PDF rendering ───────────────────────────────────────────────────────────


def render_pdf(path: Path, controls: List[Control], summary: Summary, ts: str) -> None:
    """Render the coverage report as a PDF using reportlab."""
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    h2_style = ParagraphStyle(
        "FamilyHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#2d3a8c"),
        spaceBefore=14,
        alignment=TA_LEFT,
    )
    cell = ParagraphStyle("Cell", parent=styles["BodyText"], fontSize=8, leading=10)

    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="NIST 800-53 Coverage Report",
    )

    story: List[object] = [
        Paragraph("NIST 800-53 Control Coverage", title_style),
        Paragraph(
            "9MindTech Quality Engineering Framework &middot; " f"generated {ts}",
            styles["Normal"],
        ),
        Spacer(1, 6 * mm),
        Paragraph(
            f"<b>{summary.covered_controls}/{summary.total_controls}</b> "
            f"controls covered ({summary.coverage_pct:.0f}%) across "
            f"<b>{summary.families}</b> families, exercised by "
            f"<b>{summary.total_tests}</b> tests.",
            styles["Normal"],
        ),
        Spacer(1, 4 * mm),
    ]

    for family, items in _group_by_family(controls).items():
        story.append(Paragraph(f"{family} &mdash; {len(items)} control(s)", h2_style))
        data = [["Control", "Title", "Tests", "Status"]]
        for c in items:
            data.append(
                [
                    Paragraph(f"<b>{c.control_id}</b>", cell),
                    Paragraph(c.title, cell),
                    str(c.test_count),
                    "COVERED" if c.covered else "NO COVERAGE",
                ]
            )
        table = Table(
            data,
            colWidths=[24 * mm, 92 * mm, 16 * mm, 42 * mm],
            repeatRows=1,
        )
        style = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d3a8c")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f6fb")]),
                ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#e6e6ee")),
            ]
        )
        for idx, c in enumerate(items, start=1):
            colour = colors.HexColor("#1a7f37") if c.covered else colors.HexColor("#b30000")
            style.add("TEXTCOLOR", (3, idx), (3, idx), colour)
        table.setStyle(style)
        story.append(table)

    doc.build(story)


# ── CLI ─────────────────────────────────────────────────────────────────────


def generate(out_dir: Path) -> tuple[Path, Path, Summary]:
    """Build coverage data and write the HTML and PDF reports."""
    controls = build_coverage(
        parse_registered_controls(CONFTEST),
        scan_test_usage(COMPLIANCE_DIR),
    )
    summary = summarize(controls)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    out_dir.mkdir(parents=True, exist_ok=True)
    html_path = out_dir / "nist_coverage_report.html"
    pdf_path = out_dir / "nist_coverage_report.pdf"

    html_path.write_text(render_html(controls, summary, ts), encoding="utf-8")
    render_pdf(pdf_path, controls, summary, ts)
    return html_path, pdf_path, summary


def main() -> None:
    """Parse CLI arguments and generate the coverage report."""
    parser = argparse.ArgumentParser(description="Generate a NIST 800-53 coverage report (HTML + PDF).")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("reports/nist-coverage"),
        help="Directory to write the HTML and PDF reports into.",
    )
    args = parser.parse_args()

    html_path, pdf_path, summary = generate(args.out_dir)
    print(
        f"NIST coverage: {summary.covered_controls}/{summary.total_controls} "
        f"controls ({summary.coverage_pct:.0f}%), "
        f"{summary.total_tests} tests."
    )
    print(f"HTML report: {html_path}")
    print(f"PDF report:  {pdf_path}")


if __name__ == "__main__":
    main()
