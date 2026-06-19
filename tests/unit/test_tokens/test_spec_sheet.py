"""Tests for the Token Spec Sheet (C15 — measured per-run metrics table)."""

from __future__ import annotations

from cosmos77_ex04.tokens.spec_sheet import write_spec_sheet


def _run(calls, total, files, iterations):
    return {
        "tokens": {
            "calls": calls,
            "input_tokens": total - 10,
            "output_tokens": 10,
            "total_tokens": total,
        },
        "files_read": files,
        "iterations": iterations,
    }


def test_write_spec_sheet_has_both_rows(tmp_path):
    guided = _run(1, 400, ["a.py"], 1)
    baseline = _run(1, 1000, ["a.py", "b.py", "c.py"], 1)
    out = write_spec_sheet(guided, baseline, tmp_path / "reports" / "SPEC_SHEET.md")
    text = out.read_text(encoding="utf-8")

    assert "Token Spec Sheet" in text
    assert "| Run | LLM calls | Input | Output | Total | Files read | Iterations |" in text
    assert "Naive baseline (raw files)" in text
    assert "Graph-guided agent" in text
    assert "1000" in text and "400" in text
