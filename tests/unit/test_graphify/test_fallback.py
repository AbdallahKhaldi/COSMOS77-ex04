"""Tests for the DIY ast+networkx fallback graph builder (ADR-003)."""

from __future__ import annotations

from cosmos77_ex04.graphify.fallback import build_graph, write_fallback
from cosmos77_ex04.graphify.model import GraphModel


def test_build_graph_extracts_symbols_and_relations(tmp_path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "a.py").write_text(
        "import os\nclass Base:\n    pass\nclass Child(Base):\n    def m(self):\n        return 1\n",
        encoding="utf-8",
    )
    (pkg / "b.py").write_text("def helper():\n    return 2\n", encoding="utf-8")
    graph = build_graph(pkg)
    labels = {n["label"] for n in graph["nodes"]}
    assert {"Base", "Child", "helper"} <= labels
    relations = {link["relation"] for link in graph["links"]}
    assert {"inherits", "contains", "imports"} <= relations
    assert all(link["confidence"] == "EXTRACTED" for link in graph["links"])


def test_build_graph_skips_unparseable_files(tmp_path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "bad.py").write_text("def (:\n", encoding="utf-8")
    (pkg / "ok.py").write_text("def f():\n    pass\n", encoding="utf-8")
    labels = {n["label"] for n in build_graph(pkg)["nodes"]}
    assert "f" in labels


def test_write_fallback_is_model_parseable(tmp_path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "m.py").write_text("def f():\n    return 1\n", encoding="utf-8")
    out = write_fallback(pkg, tmp_path / "out" / "graph.json")
    assert out.exists()
    model = GraphModel.from_json(out)
    assert len(model.nodes) >= 2
    assert model.edges_by_tier()["extracted"] >= 1
