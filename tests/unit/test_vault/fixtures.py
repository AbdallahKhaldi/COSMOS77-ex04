"""Shared in-memory GraphModel + report stub for the vault tests."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from cosmos77_ex04.graphify.model import Edge, GraphModel, Node

#: Matches every ``[[target`` (target = up to ``]`` or ``|``) in a vault file.
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)")


@dataclass
class ReportStub:
    """Minimal stand-in for graphify's ReportSummary (only what index.md reads)."""

    summary_line: str = "4 nodes · 5 edges · 2 communities"
    god_nodes: list[tuple[str, int]] = field(default_factory=list)
    surprising: list[str] = field(default_factory=list)
    questions: list[str] = field(default_factory=list)


def make_model() -> GraphModel:
    """A 2-community graph with god-nodes, a duplicate label, and an enumerate node."""
    nodes = [
        Node("hub", "hub.py", "hub.py", "module", 0, "Core"),
        Node("a", "__init__.py", "pkg/a/__init__.py", "module", 0, "Core"),
        Node("b", "__init__.py", "pkg/b/__init__.py", "module", 1, "Plugins"),
        Node("enum", "enumerate_items", "iter.py", "function", 1, "Plugins"),
        Node("util", "util/helper", "u.py", "function", 1, "Plugins"),
    ]
    edges = [
        Edge("hub", "a", "contains", "extracted", 1.0),
        Edge("hub", "b", "imports", "inferred", 0.8),
        Edge("hub", "enum", "calls", "ambiguous", 0.2),
        Edge("hub", "util", "calls", "extracted", 1.0),
        Edge("enum", "util", "calls", "inferred", 0.7),
    ]
    return GraphModel(nodes, edges)


def all_wikilink_targets(out_dir: Path) -> list[tuple[Path, str]]:
    """Every ``(file, target_stem)`` wikilink across all .md files under out_dir."""
    found: list[tuple[Path, str]] = []
    for md in sorted(out_dir.rglob("*.md")):
        for match in WIKILINK_RE.finditer(md.read_text(encoding="utf-8")):
            found.append((md, match.group(1).strip()))
    return found


def written_stems(out_dir: Path) -> set[str]:
    """The set of stems actually written (top-level + pages/)."""
    return {md.stem for md in out_dir.rglob("*.md")}
