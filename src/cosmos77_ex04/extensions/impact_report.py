"""Original extension — "what breaks if we change X" (C9).

Before touching a component we ask the graph for its blast radius: who depends on
it (the reverse-reachable callers) and which Bridges — the high-betweenness God
Nodes — sit on the most paths and are thus most affected by change. Persisted as
``reports/IMPACT.md``. Deterministic, no LLM.
"""

from __future__ import annotations

from pathlib import Path

import networkx as nx

from cosmos77_ex04.graphify.model import GraphModel


def _resolve(model: GraphModel, target: str) -> str | None:
    """Map an id or a label to a node id (id wins; else first label match)."""
    if target in model.nodes:
        return target
    for nid, node in model.nodes.items():
        if node.label == target:
            return nid
    return None


def impacted_nodes(model: GraphModel, node_id: str, depth: int = 2) -> list[str]:
    """Reverse-reachable callers of ``node_id`` within ``depth`` hops (the blast radius).

    We walk the *reversed* graph: an edge ``a -> b`` means a depends on b, so b's
    callers are b's predecessors — exactly who breaks if b changes.
    """
    resolved = _resolve(model, node_id)
    if resolved is None or resolved not in model.graph:
        return []
    reverse = model.graph.reverse(copy=False)
    reached = nx.single_source_shortest_path_length(reverse, resolved, cutoff=depth)
    return sorted(nid for nid in reached if nid != resolved)


def god_node_betweenness(model: GraphModel, top: int = 5) -> list[tuple[str, float]]:
    """The ``top`` highest-betweenness nodes — the Bridges most affected by change."""
    betweenness = model.betweenness()
    ranked = sorted(betweenness.items(), key=lambda kv: kv[1], reverse=True)
    return [(nid, round(score, 4)) for nid, score in ranked[:top]]


def write_impact_md(model: GraphModel, target_label: str, out_path: Path | str) -> Path:
    """Write ``reports/IMPACT.md``: the blast radius of ``target_label`` + Bridge table."""
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    callers = impacted_nodes(model, target_label)
    lines = [
        "# IMPACT.md — what breaks if we change X",
        "",
        f"**Changed component:** `{target_label}`",
        "",
        f"## Blast radius — {len(callers)} dependent caller(s) (reverse-reachable)",
        "",
    ]
    if callers:
        lines.extend(f"- {model.label_of(nid)}" for nid in callers)
    else:
        lines.append("- none (orphan/isolated or unresolved target)")
    lines.extend(
        [
            "",
            "## God-Node betweenness — the Bridges most affected by change",
            "",
            "| Bridge | Betweenness |",
            "| --- | ---: |",
        ]
    )
    for nid, score in god_node_betweenness(model):
        lines.append(f"| {model.label_of(nid)} | {score} |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
