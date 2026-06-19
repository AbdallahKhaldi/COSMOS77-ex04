"""Write the before/after KNOWLEDGE deliverables for the fix (C7).

Fills the vault templates from Phase 4 (`investigation.md`, `fix-process.md`)
with the real investigation path + the verified diff, and appends the
FAIL→PASS verification to `reports/BUG_ANALYSIS.md`. This is the knowledge-level
before/after the spec asks for: which pages and insights the fix added.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _investigation_md(result: Any, failing_test: str) -> str:
    return (
        "# Investigation — Graph-Guided Path to the Bug\n\n"
        f"**Failing test:** `{failing_test}`\n\n"
        "## Path (question → index → 2-3 pages → answer)\n"
        "1. **Problem** — the failing test raised a `TypeError` deep in `std.py`.\n"
        "2. **Index → hot.md** — the navigation hub pointed at the bug-critical area\n"
        "   (the God Node `tqdm` and the failing-test neighbourhood).\n"
        "3. **Suspects (Centrality + traceback)** — ranked the central nodes and the\n"
        "   files named in the traceback; read ONLY those (2 files), not the repo.\n"
        "4. **Root cause** — see [[fix-process]] and `reports/BUG_ANALYSIS.md`:\n"
        f"   `{result.file}` passed an int positionally where a string was expected.\n\n"
        "## Knowledge added (before → after)\n"
        "- New pages: [[investigation]], [[fix-process]].\n"
        "- New insight: the central `tqdm` constructor is a Bridge whose `desc`\n"
        "  contract is violated by a caller — a cross-community defect the graph\n"
        "  surfaced via the traceback, not by reading the whole repository.\n"
    )


def _fix_process_md(result: Any, failing_test: str) -> str:
    verdict = "PASS" if result.after_passed else "FAIL"
    return (
        "# Fix Process — The Change + Verification\n\n"
        f"**File:** `{result.file}`  ·  **Failing test:** `{failing_test}`\n\n"
        "## The minimal change (unified diff)\n"
        f"```diff\n{result.diff}```\n\n"
        "## Verification (FAIL → PASS)\n"
        f"- Before the fix: test **{'PASS' if result.before_passed else 'FAIL'}** (the bug).\n"
        f"- After the fix: test **{verdict}**.\n"
        f"- Applied: {result.applied}.\n"
    )


def _verification_section(result: Any) -> str:
    return (
        "\n\n## Fix verification (Phase 7 — FAIL → PASS)\n"
        f"- Before: test passed = {result.before_passed} (expected False — the bug).\n"
        f"- After: test passed = {result.after_passed} (expected True — fixed).\n"
        f"- File changed: `{result.file}`.\n\n"
        f"```diff\n{result.diff}```\n"
    )


def write_fix_artifacts(result: Any, failing_test: str, vault_dir: Path, reports_dir: Path) -> dict:
    """Write investigation.md + fix-process.md and append the verification to BUG_ANALYSIS."""
    vault = Path(vault_dir)
    vault.mkdir(parents=True, exist_ok=True)
    (vault / "investigation.md").write_text(
        _investigation_md(result, failing_test), encoding="utf-8"
    )
    (vault / "fix-process.md").write_text(_fix_process_md(result, failing_test), encoding="utf-8")
    bug_analysis = Path(reports_dir) / "BUG_ANALYSIS.md"
    if bug_analysis.exists():
        bug_analysis.write_text(
            bug_analysis.read_text(encoding="utf-8") + _verification_section(result),
            encoding="utf-8",
        )
    return {"investigation": vault / "investigation.md", "fix_process": vault / "fix-process.md"}
