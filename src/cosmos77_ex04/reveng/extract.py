"""Phase-5 orchestrator (C3/C4/C14) — extract every reverse-engineering diagram.

One call renders both PNGs (block + OOP), classifies the god-nodes, and writes
the ``ARCHITECTURE.md`` report. Keeps the SDK/CLI un-wired (the orchestrator that
sits above this module does that); this is the pure, deterministic extraction.
"""

from __future__ import annotations

from pathlib import Path

from cosmos77_ex04.graphify.model import GraphModel
from cosmos77_ex04.reveng.block_diagram import block_mermaid, render_block_png
from cosmos77_ex04.reveng.godnodes import classify, write_architecture_report
from cosmos77_ex04.reveng.oop_schema import extract_classes, oop_mermaid, render_oop_png


def extract_diagrams(
    model: GraphModel,
    source,
    artifacts_dir,
    reports_dir,
) -> dict:
    """Render PNGs, classify god-nodes, write ARCHITECTURE.md; return a summary.

    ``model`` is the parsed graph, ``source`` is the package to AST-walk for the
    OOP schema, and the two dirs receive the PNGs / the report respectively.
    """
    artifacts = Path(artifacts_dir)
    reports = Path(reports_dir)

    block_png = render_block_png(model, artifacts / "block_diagram.png")
    classes = extract_classes(source)
    oop_png = render_oop_png(classes, artifacts / "oop_schema.png")

    block_md = block_mermaid(model)
    oop_md = oop_mermaid(classes)
    verdicts = classify(model)
    architecture = write_architecture_report(
        model, classes, verdicts, block_md, oop_md, reports / "ARCHITECTURE.md"
    )

    return {
        "block_png": block_png,
        "oop_png": oop_png,
        "architecture": architecture,
        "god_nodes": sum(1 for v in verdicts if v.kind == "god_node"),
        "hubs": sum(1 for v in verdicts if v.kind == "hub"),
        "classes": len(classes),
    }
