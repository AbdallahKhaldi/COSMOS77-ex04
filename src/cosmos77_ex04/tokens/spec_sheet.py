"""The Token Spec Sheet (C15) — per-run measured metrics, side by side.

This sheet is the at-a-glance ledger the assignment asks for: for BOTH the naive
baseline and the graph-guided agent, the measured LLM calls, input/output/total
tokens, files read, and iterations. Every number comes from the Gatekeeper, so
the sheet is honest evidence rather than a narrative claim.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _row(label: str, run: dict[str, Any]) -> str:
    """One Spec Sheet row from a measured run's ledger + file/iteration counts."""
    led = run["tokens"]
    return (
        f"| {label} | {led.get('calls', 0)} | {led.get('input_tokens', 0)} | "
        f"{led.get('output_tokens', 0)} | {led.get('total_tokens', 0)} | "
        f"{len(run.get('files_read', []))} | {run.get('iterations', 0)} |"
    )


def write_spec_sheet(
    guided: dict[str, Any], baseline: dict[str, Any], out_path: Path | str
) -> Path:
    """Write reports/SPEC_SHEET.md: the measured per-run metrics table (C15)."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    table = "\n".join(
        [
            "| Run | LLM calls | Input | Output | Total | Files read | Iterations |",
            "| --- | --- | --- | --- | --- | --- | --- |",
            _row("Naive baseline (raw files)", baseline),
            _row("Graph-guided agent", guided),
        ]
    )
    content = (
        "# Token Spec Sheet\n\n"
        "Measured per-run metrics from the Gatekeeper ledger (`usage_metadata`), "
        "both arms on the SAME buggy code and SAME LLM — honest measurement, no "
        "estimates.\n\n"
        f"{table}\n"
    )
    out.write_text(content, encoding="utf-8")
    return out
