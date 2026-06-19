"""Render the graph-guided investigation into reports/BUG_ANALYSIS.md (C5)."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def write_bug_analysis(result: dict[str, Any], failing_test: str, out_path: Path | str) -> Path:
    """Write the BUG_ANALYSIS report (problem, suspects, root cause, token ledger)."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    suspects = "\n".join(f"- {s}" for s in result["suspects"]) or "- (none)"
    files = "\n".join(f"- `{f}`" for f in result["files_read"]) or "- (none)"
    ledger = result["tokens"]
    content = (
        "# Bug Analysis — Graph-Guided Investigation\n\n"
        f"**Failing test:** `{failing_test}`\n\n"
        "## How the graph led us here (guided retrieval)\n"
        "The agent consulted `index.md`, `hot.md`, and the graph summary FIRST, then\n"
        "ranked suspects by Centrality + proximity to the failing test, and read ONLY\n"
        "the top suspect files — never the whole repository. This is the "
        "context-reduction mechanism the token comparison (C8) measures.\n\n"
        f"## Suspects considered (ranked by Centrality)\n{suspects}\n\n"
        f"## Files read (targeted — {len(result['files_read'])} file(s))\n{files}\n\n"
        f"## Root cause (LLM diagnosis on focused context)\n\n{result['diagnosis']}\n\n"
        "## Token ledger (measured — the deliverable's evidence)\n"
        f"- LLM calls: {ledger['calls']}\n"
        f"- Input tokens: {ledger['input_tokens']}\n"
        f"- Output tokens: {ledger['output_tokens']}\n"
        f"- Total tokens: {ledger['total_tokens']}\n"
        f"- Iterations: {result['iterations']}\n"
    )
    out.write_text(content, encoding="utf-8")
    return out
