"""Tests for the GRAPH_REPORT.md parser (C1)."""

from __future__ import annotations

from cosmos77_ex04.graphify.report import ReportSummary, parse_report

REPORT = """# Graph Report

## Summary
500 nodes · 1071 edges · 28 communities
Extraction: 76% EXTRACTED · 24% INFERRED

## God Nodes (most connected - your core abstractions)
1. `tqdm` - 106 edges
2. `closing()` - 74 edges
3. `TMonitor` - 21 edges

## Surprising Connections (you probably didn't know these)
- `test_manpath()` --calls--> `main()`  [INFERRED]
  src.py → dst.py

## Suggested Questions
- Why does `tqdm` connect Community 10 to Community 3?
- Are the 58 inferred relationships correct?
"""


def test_parse_report_extracts_sections(tmp_path):
    path = tmp_path / "GRAPH_REPORT.md"
    path.write_text(REPORT, encoding="utf-8")
    summary = parse_report(path)
    assert isinstance(summary, ReportSummary)
    assert ("tqdm", 106) in summary.god_nodes
    assert len(summary.god_nodes) == 3
    assert any("test_manpath" in line for line in summary.surprising)
    assert len(summary.surprising) == 1
    assert any("Community 10" in q for q in summary.questions)
    assert "500 nodes" in summary.summary_line


def test_parse_missing_report_is_empty(tmp_path):
    summary = parse_report(tmp_path / "nope.md")
    assert summary.god_nodes == []
    assert summary.summary_line == ""
