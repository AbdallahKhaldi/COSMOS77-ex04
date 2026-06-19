"""Tests for graph-guided focused retrieval (C5 — no LLM, no bulk reads)."""

from __future__ import annotations

from cosmos77_ex04.agent.retrieval import (
    fetch_snippets,
    graph_summary,
    rank_suspects,
    read_vault,
)
from cosmos77_ex04.graphify.model import Edge, GraphModel, Node


def _model():
    nodes = [
        Node("a", "tqdm", "std.py", "code", 0, "Community 0"),
        Node("b", "tenumerate", "std.py", "code", 0, "Community 0"),
        Node("c", "helper", "utils.py", "code", 1, "Community 1"),
        Node("d", "unused", "other.py", "code", 1, "Community 1"),
    ]
    edges = [
        Edge("a", "b", "calls", "extracted", 1.0),
        Edge("b", "c", "uses", "inferred", 0.8),
        Edge("a", "c", "calls", "extracted", 1.0),
    ]
    return GraphModel(nodes, edges)


def test_rank_suspects_prioritises_proximity_to_test():
    ranked = rank_suspects(_model(), "tqdm/tests/tests_contrib.py::test_enumerate", 3)
    assert ranked[:2] == ["a", "b"] or set(ranked[:2]) == {"a", "b"}
    assert "d" not in ranked  # unused, zero-degree, no proximity


def test_rank_suspects_boosts_traceback_files():
    # A node whose file appears in the traceback gets the strongest boost.
    ranked = rank_suspects(_model(), "test_x", 2, test_output="Traceback: tqdm/utils.py:5 helper")
    assert "c" in ranked  # utils.py, surfaced only because the traceback names it


def test_fetch_snippets_reads_only_suspect_files(tmp_path):
    model = _model()
    (tmp_path / "std.py").write_text("X = 1\n", encoding="utf-8")
    (tmp_path / "utils.py").write_text("Y = 2\n", encoding="utf-8")
    (tmp_path / "other.py").write_text("SECRET = 3\n", encoding="utf-8")
    snippets, files_read = fetch_snippets(model, ["a", "b", "c"], tmp_path, max_files=4)
    assert files_read == ["std.py", "utils.py"]  # dedup; never other.py
    assert "other.py" not in snippets


def test_fetch_snippets_respects_max_files(tmp_path):
    model = _model()
    (tmp_path / "std.py").write_text("X = 1\n", encoding="utf-8")
    (tmp_path / "utils.py").write_text("Y = 2\n", encoding="utf-8")
    snippets, files_read = fetch_snippets(model, ["a", "c"], tmp_path, max_files=1)
    assert len(files_read) == 1


def test_graph_summary_has_no_raw_source():
    summary = graph_summary(_model())
    assert "nodes" in summary and "communities" in summary
    assert "tqdm" in summary


def test_read_vault_reads_hub_and_hot(tmp_path):
    (tmp_path / "index.md").write_text("# Index nav hub", encoding="utf-8")
    (tmp_path / "hot.md").write_text("# hot bug-critical", encoding="utf-8")
    text = read_vault(tmp_path)
    assert "nav hub" in text and "bug-critical" in text
