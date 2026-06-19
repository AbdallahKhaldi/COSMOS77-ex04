"""Tests for the honest token comparison + report (C8 — the central invariant)."""

from __future__ import annotations

from cosmos77_ex04.tokens.compare import compare, write_comparison_md


def _run(total, inp, out, files):
    return {
        "tokens": {"input_tokens": inp, "output_tokens": out, "total_tokens": total, "calls": 1},
        "files_read": files,
        "iterations": 1,
    }


def test_compare_reports_savings_when_guided_is_cheaper():
    baseline = _run(1000, 900, 100, ["a.py", "b.py", "c.py", "d.py"])
    guided = _run(400, 350, 50, ["a.py", "b.py"])
    c = compare(baseline, guided)

    assert c["tokens_saved"] == 600
    assert c["pct_tokens_saved"] == 60.0
    # the central invariant: guided reads fewer files
    assert c["files_baseline"] == 4
    assert c["files_guided"] == 2
    assert c["files_saved"] == 2


def test_compare_is_honest_when_runs_are_equal():
    same = _run(500, 450, 50, ["a.py", "b.py"])
    c = compare(same, dict(same))
    assert c["tokens_saved"] == 0
    assert c["pct_tokens_saved"] == 0.0
    assert c["files_saved"] == 0


def test_compare_guards_divide_by_zero():
    baseline = _run(0, 0, 0, [])
    guided = _run(0, 0, 0, [])
    c = compare(baseline, guided)
    assert c["pct_tokens_saved"] == 0.0


def test_write_comparison_md_has_table_and_narrative(tmp_path):
    baseline = _run(1000, 900, 100, ["a.py", "b.py", "c.py"])
    guided = _run(400, 350, 50, ["a.py"])
    out = write_comparison_md(compare(baseline, guided), tmp_path / "reports" / "TC.md")
    text = out.read_text(encoding="utf-8")
    assert "| Metric | Baseline | Guided | Delta | % |" in text
    assert "Total tokens" in text
    assert "Guided retrieval" in text
    assert "token_comparison.pdf" in text
    assert "signal-to-noise" in text


def test_write_comparison_md_modest_savings_is_honest(tmp_path):
    baseline = _run(120, 100, 20, ["a.py", "b.py"])
    guided = _run(110, 90, 20, ["a.py"])
    out = write_comparison_md(compare(baseline, guided), tmp_path / "TC.md")
    text = out.read_text(encoding="utf-8")
    assert "modest" in text


def test_write_comparison_md_baseline_wins_is_honest(tmp_path):
    baseline = _run(300, 250, 50, ["a.py", "b.py", "c.py"])
    guided = _run(350, 300, 50, ["a.py"])
    out = write_comparison_md(compare(baseline, guided), tmp_path / "TC.md")
    text = out.read_text(encoding="utf-8")
    assert "honestly" in text
    assert "file count" in text
