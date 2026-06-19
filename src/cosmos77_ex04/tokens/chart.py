"""Render the naive-vs-guided comparison as a grouped bar chart (C8).

The chart visualises the two measured axes — total tokens and files read — side
by side so the honest comparison is legible at a glance. We force the headless
``Agg`` backend BEFORE importing pyplot so it renders a PDF without a display.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")  # headless: must precede the pyplot import

import matplotlib.pyplot as plt  # noqa: E402


def _totals(run: dict[str, Any]) -> tuple[int, int]:
    """Return (total_tokens, files_read) for one measured run."""
    tokens = int(run["tokens"].get("total_tokens", 0) or 0)
    return tokens, len(run.get("files_read", []))


def render_chart(baseline: dict[str, Any], guided: dict[str, Any], out_path: Path | str) -> Path:
    """Write a grouped bar chart (tokens + files: baseline vs guided) to a PDF."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    b_tokens, b_files = _totals(baseline)
    g_tokens, g_files = _totals(guided)

    fig, (ax_tok, ax_files) = plt.subplots(1, 2, figsize=(9, 4))
    arms = ["Naive (raw files)", "Graph-guided"]
    colours = ["#b3261e", "#1a73e8"]
    ax_tok.bar(arms, [b_tokens, g_tokens], color=colours)
    ax_tok.set_title("Total tokens (measured)")
    ax_tok.set_ylabel("tokens")
    ax_files.bar(arms, [b_files, g_files], color=colours)
    ax_files.set_title("Files read")
    ax_files.set_ylabel("files")
    for ax in (ax_tok, ax_files):
        ax.tick_params(axis="x", rotation=15)
    fig.suptitle("Naive raw-file reading vs graph-guided retrieval")
    fig.tight_layout()
    fig.savefig(out, format="pdf")
    plt.close(fig)
    return out
