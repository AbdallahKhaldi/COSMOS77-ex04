"""Tests for the graph.json parser + queryable model (C1, C14)."""

from __future__ import annotations

import json

from cosmos77_ex04.graphify.model import GraphModel, normalise_tier

FIXTURE = {
    "directed": False,
    "nodes": [
        {
            "id": "m",
            "label": "mod.py",
            "source_file": "mod.py",
            "file_type": "code",
            "community": 0,
        },
        {"id": "a", "label": "A", "source_file": "mod.py", "file_type": "code", "community": 0},
        {"id": "b", "label": "b", "source_file": "mod.py", "file_type": "code", "community": 1},
        {"id": "c", "label": "c", "source_file": "other.py", "file_type": "code", "community": 1},
    ],
    "links": [
        {
            "source": "m",
            "target": "a",
            "relation": "contains",
            "confidence": "EXTRACTED",
            "confidence_score": 1.0,
        },
        {
            "source": "a",
            "target": "b",
            "relation": "calls",
            "confidence": "INFERRED",
            "confidence_score": 0.8,
        },
        {
            "source": "b",
            "target": "c",
            "relation": "calls",
            "confidence": "AMBIGUOUS",
            "confidence_score": 0.2,
        },
        {
            "source": "a",
            "target": "c",
            "relation": "uses",
            "confidence": "EXTRACTED",
            "confidence_score": 1.0,
        },
    ],
}


def _model(tmp_path):
    path = tmp_path / "graph.json"
    path.write_text(json.dumps(FIXTURE), encoding="utf-8")
    return GraphModel.from_json(path)


def test_parses_nodes_and_edges(tmp_path):
    model = _model(tmp_path)
    assert len(model.nodes) == 4
    assert len(model.edges) == 4
    assert model.nodes["a"].label == "A"
    assert model.nodes["m"].file == "mod.py"


def test_evidence_tiers_normalised(tmp_path):
    model = _model(tmp_path)
    assert model.edges_by_tier() == {"extracted": 2, "inferred": 1, "ambiguous": 1}


def test_normalise_tier():
    assert normalise_tier("EXTRACTED") == "extracted"
    assert normalise_tier("weird") == "ambiguous"
    assert normalise_tier("") == "ambiguous"


def test_god_nodes_by_degree(tmp_path):
    model = _model(tmp_path)
    god = model.god_nodes(2)
    assert god[0] == ("a", 3)


def test_betweenness_is_cached(tmp_path):
    model = _model(tmp_path)
    first = model.betweenness()
    assert set(first) == set(model.nodes)
    assert model.betweenness() is first


def test_communities_group_nodes(tmp_path):
    model = _model(tmp_path)
    comms = model.communities()
    assert sorted(comms) == [0, 1]
    assert set(comms[1]) == {"b", "c"}


def test_neighbors_and_label(tmp_path):
    model = _model(tmp_path)
    assert model.neighbors("a") == sorted(["m", "b", "c"])
    assert model.neighbors("missing") == []
    assert model.label_of("a") == "A"
    assert model.label_of("zzz") == "zzz"


def test_edges_key_fallback(tmp_path):
    path = tmp_path / "g.json"
    path.write_text(
        json.dumps({"nodes": [{"id": "x", "label": "x"}], "edges": []}), encoding="utf-8"
    )
    model = GraphModel.from_json(path)
    assert len(model.nodes) == 1
    assert model.edges == []
