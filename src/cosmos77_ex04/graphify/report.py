"""Parse graphify's GRAPH_REPORT.md into a structured summary (C1).

The report's God Nodes, Surprising Connections, and Suggested Questions seed the
Obsidian vault (index.md / hot.md) and the agent's first read. This is pure text
parsing — no graph needed — so it is trivially testable with a fixture report.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

_GOD_RE = re.compile(r"`([^`]+)`\s*[-–—]\s*(\d+)\s*edges")


@dataclass
class ReportSummary:
    """The structured slice of GRAPH_REPORT.md the rest of the pipeline reuses."""

    summary_line: str = ""
    god_nodes: list[tuple[str, int]] = field(default_factory=list)
    surprising: list[str] = field(default_factory=list)
    questions: list[str] = field(default_factory=list)


def _sections(text: str) -> dict[str, list[str]]:
    """Split a Markdown document into ``{lowercased ## heading: [lines]}``."""
    sections: dict[str, list[str]] = {}
    current = ""
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip().lower()
            sections[current] = []
        elif current:
            sections[current].append(line)
    return sections


def _find(sections: dict[str, list[str]], keyword: str) -> list[str]:
    """Return the lines of the first section whose heading contains ``keyword``."""
    for heading, lines in sections.items():
        if keyword in heading:
            return lines
    return []


def _is_item(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and stripped[0] in "-*0123456789"


def _clean(line: str) -> str:
    return line.strip().lstrip("-*0123456789. ").strip()


def parse_report(path: Path | str) -> ReportSummary:
    """Parse a GRAPH_REPORT.md into a :class:`ReportSummary` (empty if absent)."""
    file = Path(path)
    text = file.read_text(encoding="utf-8") if file.exists() else ""
    sections = _sections(text)
    god_nodes: list[tuple[str, int]] = []
    for line in _find(sections, "god nodes"):
        match = _GOD_RE.search(line)
        if match:
            god_nodes.append((match.group(1), int(match.group(2))))
    surprising = [
        line.strip()
        for line in _find(sections, "surprising")
        if "`" in line and ("-->" in line or "→" in line)
    ]
    questions = [_clean(line) for line in _find(sections, "suggested questions") if _is_item(line)]
    summary_line = next(
        (
            line.strip()
            for line in _find(sections, "summary")
            if "nodes" in line and "edges" in line
        ),
        "",
    )
    return ReportSummary(summary_line, god_nodes, surprising, questions)
