"""Tests for the Phase-5 orchestrator: extract_diagrams end-to-end."""

from __future__ import annotations

from cosmos77_ex04.reveng.extract import extract_diagrams


def test_extract_diagrams_renders_and_reports(model, package, tmp_path):
    artifacts = tmp_path / "artifacts"
    reports = tmp_path / "reports"
    result = extract_diagrams(model, package, artifacts, reports)

    assert result["block_png"] == artifacts / "block_diagram.png"
    assert result["oop_png"] == artifacts / "oop_schema.png"
    assert result["architecture"] == reports / "ARCHITECTURE.md"
    assert result["block_png"].stat().st_size > 0
    assert result["oop_png"].stat().st_size > 0

    assert result["classes"] == 2
    assert result["god_nodes"] >= 1
    assert result["hubs"] >= 1

    text = result["architecture"].read_text(encoding="utf-8")
    assert "flowchart" in text and "classDiagram" in text


def test_extract_diagrams_returns_all_keys(model, package, tmp_path):
    result = extract_diagrams(model, package, tmp_path / "a", tmp_path / "r")
    assert set(result) == {
        "block_png",
        "oop_png",
        "architecture",
        "god_nodes",
        "hubs",
        "classes",
    }
