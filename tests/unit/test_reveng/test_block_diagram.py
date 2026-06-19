"""Tests for the BLOCK diagram (C3): bridges, Mermaid flowchart, PNG render."""

from __future__ import annotations

from cosmos77_ex04.reveng.block_diagram import (
    block_mermaid,
    bridges,
    render_block_png,
)


def test_bridges_count_cross_community_edges(model):
    counts = bridges(model)
    # The single ``l0 -> bridge`` stays in community 0; the five ``bridge -> rK``
    # edges all cross from community 0 into community 1.
    assert counts == {(0, 1): 5}


def test_bridges_ignores_unknown_endpoints(model):
    from cosmos77_ex04.graphify.model import Edge

    model.edges.append(Edge("ghost", "bridge", "calls", "extracted", 1.0))
    assert bridges(model) == {(0, 1): 5}


def test_block_mermaid_contains_flowchart_and_bridge(model):
    text = block_mermaid(model)
    assert text.startswith("flowchart")
    assert "bridge edges" in text
    assert "C0" in text and "C1" in text


def test_render_block_png_writes_nonempty(model, tmp_path):
    out = render_block_png(model, tmp_path / "block.png")
    assert out.exists()
    assert out.suffix == ".png"
    assert out.stat().st_size > 0


def test_block_mermaid_falls_back_to_generic_name():
    from cosmos77_ex04.graphify.model import GraphModel, Node

    node = Node("x", "x", "f.py", "code", 9, "")  # blank community_name
    text = block_mermaid(GraphModel([node], []))
    assert "Community 9" in text
