"""Tests for the grouped bar chart renderer (C8 — writes a non-empty PDF)."""

from __future__ import annotations

from cosmos77_ex04.tokens.chart import render_chart


def _run(total, files):
    return {
        "tokens": {"total_tokens": total, "input_tokens": total, "output_tokens": 0},
        "files_read": files,
    }


def test_render_chart_writes_non_empty_pdf(tmp_path):
    baseline = _run(1000, ["a.py", "b.py", "c.py"])
    guided = _run(400, ["a.py"])
    out = render_chart(baseline, guided, tmp_path / "art" / "token_comparison.pdf")

    assert out.exists()
    data = out.read_bytes()
    assert len(data) > 0
    assert data[:4] == b"%PDF"


def test_render_chart_handles_zero_runs(tmp_path):
    baseline = _run(0, [])
    guided = _run(0, [])
    out = render_chart(baseline, guided, tmp_path / "tc.pdf")
    assert out.read_bytes()[:4] == b"%PDF"
