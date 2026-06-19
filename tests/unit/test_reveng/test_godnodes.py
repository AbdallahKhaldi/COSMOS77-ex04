"""Tests for the God-Node / Centrality diagnosis (C14) and the report writer."""

from __future__ import annotations

from cosmos77_ex04.reveng.block_diagram import block_mermaid
from cosmos77_ex04.reveng.godnodes import classify, write_architecture_report
from cosmos77_ex04.reveng.oop_schema import extract_classes, oop_mermaid


def test_classify_labels_bridge_god_node_and_hub(model):
    verdicts = {v.node_id: v for v in classify(model, top=4)}
    assert verdicts["bridge"].kind == "god_node"
    assert "God Node" in verdicts["bridge"].reason
    assert verdicts["hub"].kind == "hub"
    assert "Healthy Hub" in verdicts["hub"].reason


def test_classify_reports_degree_and_betweenness(model):
    verdicts = classify(model, top=4)
    bridge = next(v for v in verdicts if v.node_id == "bridge")
    assert bridge.degree > 0
    assert bridge.betweenness > 0.0


def test_write_architecture_report_has_both_diagrams(model, package, tmp_path):
    classes = extract_classes(package)
    verdicts = classify(model, top=4)
    out = write_architecture_report(
        model,
        classes,
        verdicts,
        block_mermaid(model),
        oop_mermaid(classes),
        tmp_path / "ARCHITECTURE.md",
    )
    text = out.read_text(encoding="utf-8")
    assert "flowchart" in text
    assert "classDiagram" in text
    assert "God Node" in text
    assert "```mermaid" in text


def test_bridges_communities_unknown_node_is_false(model):
    from cosmos77_ex04.reveng.godnodes import _bridges_communities

    assert _bridges_communities(model, "does-not-exist") is False


def test_report_handles_no_bridges(tmp_path):
    from cosmos77_ex04.graphify.model import GraphModel, Node

    node = Node("solo", "solo", "f.py", "code", 0, "Community 0")
    model = GraphModel([node], [])
    out = write_architecture_report(
        model, [], classify(model), "flowchart TD", "classDiagram", tmp_path / "A.md"
    )
    assert "No cross-community bridges" in out.read_text(encoding="utf-8")
