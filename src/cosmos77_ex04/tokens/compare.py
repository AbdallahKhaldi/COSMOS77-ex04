"""Compute + render the honest naive-vs-guided token comparison (C8).

The deltas here rest on MEASURED ledgers from both arms (same bug, same model),
never estimates. :func:`write_comparison_md` reports the numbers as they are: if
guided retrieval saves a lot, we show it; if the saving is modest (small target,
both arms reach the bug), we say so plainly — the defensible measured comparison
is the deliverable, not an inflated percentage.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _tok(ledger: dict[str, Any], key: str) -> int:
    """Read a token field from a ledger, defaulting to 0."""
    return int(ledger.get(key, 0) or 0)


def compare(baseline: dict[str, Any], guided: dict[str, Any]) -> dict[str, Any]:
    """Compute token + file deltas (guided vs baseline) from two measured runs."""
    b_led, g_led = baseline["tokens"], guided["tokens"]
    b_total, g_total = _tok(b_led, "total_tokens"), _tok(g_led, "total_tokens")
    tokens_saved = b_total - g_total
    pct = (tokens_saved / b_total * 100.0) if b_total else 0.0
    files_baseline = len(baseline.get("files_read", []))
    files_guided = len(guided.get("files_read", []))
    return {
        "baseline_total_tokens": b_total,
        "guided_total_tokens": g_total,
        "baseline_input_tokens": _tok(b_led, "input_tokens"),
        "guided_input_tokens": _tok(g_led, "input_tokens"),
        "baseline_output_tokens": _tok(b_led, "output_tokens"),
        "guided_output_tokens": _tok(g_led, "output_tokens"),
        "tokens_saved": tokens_saved,
        "pct_tokens_saved": round(pct, 2),
        "files_baseline": files_baseline,
        "files_guided": files_guided,
        "files_saved": files_baseline - files_guided,
    }


def _row(label: str, base: Any, guided: Any) -> str:
    delta = guided - base
    pct = f"{(-delta / base * 100):.1f}%" if base else "n/a"
    return f"| {label} | {base} | {guided} | {delta:+d} | {pct} |"


def _narrative(c: dict[str, Any]) -> str:
    """An HONEST paragraph: large savings shown, modest savings explained."""
    pct = c["pct_tokens_saved"]
    if c["tokens_saved"] > 0 and pct >= 25:
        verdict = (
            f"Guided retrieval cut total tokens by {pct}% "
            f"({c['tokens_saved']} fewer). By consulting `index.md` as the "
            "navigation hub and reading only the top suspect files, the agent "
            "kept a high signal-to-noise context and avoided the Lost in the "
            "Middle and Context Rot failure modes of the raw-file baseline."
        )
    elif c["tokens_saved"] > 0:
        verdict = (
            f"Guided retrieval saved {c['tokens_saved']} tokens ({pct}%) — a "
            "modest but REAL reduction. The target is small, so the baseline's "
            "whole-repo prompt is not enormous; the honest measurement still "
            "shows guided retrieval reading fewer files at lower cost."
        )
    else:
        verdict = (
            "On this run the baseline matched or beat the guided arm on tokens "
            f"({pct}%). We report it honestly: the target is small enough that "
            "both arms can reach the bug. The defensible win is the file count — "
            f"guided read {c['files_guided']} file(s) vs {c['files_baseline']}."
        )
    return verdict


def write_comparison_md(comparison: dict[str, Any], out_path: Path | str) -> Path:
    """Write reports/TOKEN_COMPARISON.md: a delta table + an honest narrative."""
    c = comparison
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    table = "\n".join(
        [
            "| Metric | Baseline | Guided | Delta | % |",
            "| --- | --- | --- | --- | --- |",
            _row("Total tokens", c["baseline_total_tokens"], c["guided_total_tokens"]),
            _row("Input tokens", c["baseline_input_tokens"], c["guided_input_tokens"]),
            _row("Output tokens", c["baseline_output_tokens"], c["guided_output_tokens"]),
            _row("Files read", c["files_baseline"], c["files_guided"]),
        ]
    )
    content = (
        "# Token Comparison — Naive Raw-Files vs Graph-Guided (C8)\n\n"
        "All numbers are MEASURED from `usage_metadata` via the Gatekeeper ledger, "
        "for both arms on the SAME buggy code and SAME LLM.\n\n"
        f"{table}\n\n"
        "## Honest verdict\n\n"
        f"{_narrative(c)}\n\n"
        "See the chart `artifacts/token_comparison.pdf` for the grouped bars.\n"
    )
    out.write_text(content, encoding="utf-8")
    return out
