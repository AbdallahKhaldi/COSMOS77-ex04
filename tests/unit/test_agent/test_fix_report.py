"""Tests for the before/after knowledge deliverables (C7)."""

from __future__ import annotations

from cosmos77_ex04.agent.fix import FixResult
from cosmos77_ex04.agent.fix_report import write_fix_artifacts


def test_write_fix_artifacts(tmp_path):
    vault = tmp_path / "obsidian"
    vault.mkdir()
    reports = tmp_path / "reports"
    reports.mkdir()
    (reports / "BUG_ANALYSIS.md").write_text("# Bug Analysis\n", encoding="utf-8")
    result = FixResult(
        "tqdm/contrib/__init__.py", "--- a\n+++ b\n-foo(a, b)\n+foo(b, a)\n", False, True, True
    )
    out = write_fix_artifacts(result, "tests_contrib.py::test_enumerate", vault, reports)
    assert (vault / "investigation.md").exists()
    assert out["fix_process"].exists()
    fix_process = (vault / "fix-process.md").read_text(encoding="utf-8")
    assert "FAIL" in fix_process and "PASS" in fix_process
    assert "```diff" in fix_process
    bug_analysis = (reports / "BUG_ANALYSIS.md").read_text(encoding="utf-8")
    assert "Phase 7" in bug_analysis
    assert "foo(b, a)" in bug_analysis


def test_write_fix_artifacts_without_bug_analysis(tmp_path):
    vault = tmp_path / "obsidian"
    reports = tmp_path / "reports"
    result = FixResult("x.py", "diff", False, True, True)
    write_fix_artifacts(result, "t", vault, reports)  # BUG_ANALYSIS absent — must not raise
    assert (vault / "investigation.md").exists()
