"""The ``reports/ARCHITECTURE.md`` writer — a macro->meso->micro narrative (C3/C4/C14).

The report tells the reverse-engineering story at three zoom levels: **macro**
(communities = the block diagram), **meso** (bridges = the cross-community flow),
and **micro** (god-nodes vs healthy hubs). It embeds the Mermaid ``flowchart``
and ``classDiagram`` as fenced ```mermaid blocks and references the PNG renders.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from cosmos77_ex04.graphify.model import GraphModel
    from cosmos77_ex04.reveng.godnodes import Verdict
    from cosmos77_ex04.reveng.oop_schema import ClassInfo

_BLOCK_PNG = "artifacts/block_diagram.png"
_OOP_PNG = "artifacts/oop_schema.png"


def _macro_section(model: GraphModel, block_md: str) -> list[str]:
    """The macro view: communities as blocks + the embedded flowchart."""
    comms = model.communities()
    lines = [
        "## Macro — Communities (Block Diagram)",
        "",
        f"The graph has **{len(model.nodes)} nodes** in **{len(comms)} communities**. "
        "Each block below is one Community, sized by member count.",
        "",
        f"![Block diagram]({_BLOCK_PNG})",
        "",
        "```mermaid",
        block_md,
        "```",
        "",
    ]
    return lines


def _meso_section(model: GraphModel) -> list[str]:
    """The meso view: the Bridges (cross-community edges) that wire the blocks."""
    from cosmos77_ex04.reveng.block_diagram import bridges

    ranked = sorted(bridges(model).items(), key=lambda kv: kv[1], reverse=True)
    lines = ["## Meso — Bridges (cross-community flow)", ""]
    if not ranked:
        lines += ["No cross-community bridges were found.", ""]
        return lines
    lines += ["| Community A | Community B | Bridge edges |", "| --- | --- | --- |"]
    for (low, high), weight in ranked[:15]:
        lines.append(f"| {low} | {high} | {weight} |")
    lines.append("")
    return lines


def _oop_section(classes: list[ClassInfo], oop_md: str) -> list[str]:
    """The OOP schema view: the class-inheritance diagram."""
    return [
        "## OOP Schema — Class Inheritance",
        "",
        f"AST extraction found **{len(classes)} classes**. Inheritance edges use `<|--`.",
        "",
        f"![OOP schema]({_OOP_PNG})",
        "",
        "```mermaid",
        oop_md,
        "```",
        "",
    ]


def _micro_section(verdicts: list[Verdict]) -> list[str]:
    """The micro view: the God-Node vs healthy-Hub verdict table."""
    gods = sum(1 for v in verdicts if v.kind == "god_node")
    hubs = sum(1 for v in verdicts if v.kind == "hub")
    lines = [
        "## Micro — God Nodes vs healthy Hubs (Centrality)",
        "",
        f"Of the top {len(verdicts)} central nodes: **{gods} God Node(s)**, **{hubs} Hub(s)**.",
        "",
        "| Node | Degree | Betweenness | Verdict | Reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    for verdict in verdicts:
        lines.append(
            f"| {verdict.label} | {verdict.degree} | {verdict.betweenness:.4f} "
            f"| {verdict.kind} | {verdict.reason} |"
        )
    lines.append("")
    return lines


def write_architecture_report(
    model: GraphModel,
    classes: list[ClassInfo],
    verdicts: list[Verdict],
    block_md: str,
    oop_md: str,
    out_path,
) -> Path:
    """Write ``reports/ARCHITECTURE.md`` (macro->meso->micro) and return its path."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Reverse-Engineered Architecture",
        "",
        "A graph-extracted, three-zoom narrative: macro (communities) -> meso "
        "(bridges) -> micro (god-nodes). Diagrams are Extracted from the AST/graph.",
        "",
    ]
    lines += _macro_section(model, block_md)
    lines += _meso_section(model)
    lines += _oop_section(classes, oop_md)
    lines += _micro_section(verdicts)
    out.write_text("\n".join(lines), encoding="utf-8")
    return out
