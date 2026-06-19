"""Original extension — find & classify orphan/isolated nodes (C9).

An orphan node has NO in- and NO out-edges: graphify could not connect it. Some
are intentional (adapters, legacy/compat shims, dunder helpers); the rest are
*possible dead code*. We apply a small, stated verification protocol — a label
heuristic — and persist a ``reports/ORPHANS.md`` count + classification table so
a reviewer can confirm each call. Deterministic, no LLM.
"""

from __future__ import annotations

from pathlib import Path

from cosmos77_ex04.graphify.model import GraphModel

#: Label substrings that mark an orphan as an intentional adapter/legacy shim.
_INTENTIONAL_MARKERS = ("test", "adapter", "compat")

_INTENTIONAL = "intentional (adapter/legacy)"
_DEAD_CODE = "possible dead code"


def find_orphans(model: GraphModel) -> list[str]:
    """Node ids with neither predecessors nor successors (truly isolated)."""
    graph = model.graph
    return sorted(
        nid for nid in model.nodes if graph.in_degree(nid) == 0 and graph.out_degree(nid) == 0
    )


def classify_orphan(model: GraphModel, node_id: str) -> str:
    """Heuristic verdict for one orphan (the verification protocol's first pass).

    A ``_``-prefixed label or one naming an adapter/legacy/test concern is judged
    intentional; everything else is flagged as possible dead code for follow-up.
    """
    label = model.label_of(node_id)
    stem = label.lower()
    if label.startswith("_") or any(marker in stem for marker in _INTENTIONAL_MARKERS):
        return _INTENTIONAL
    return _DEAD_CODE


def write_orphans_md(model: GraphModel, out_path: Path | str) -> Path:
    """Write ``reports/ORPHANS.md``: orphan count + classification table."""
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    orphans = find_orphans(model)
    lines = [
        "# ORPHANS.md — orphan / isolated nodes",
        "",
        f"Found **{len(orphans)}** orphan node(s) (no in- and no out-edges). "
        "Each is classified by a label heuristic; verify before deleting.",
        "",
        "| Orphan | File | Classification |",
        "| --- | --- | --- |",
    ]
    for nid in orphans:
        node = model.nodes[nid]
        lines.append(f"| {node.label} | {node.file or '-'} | {classify_orphan(model, nid)} |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
