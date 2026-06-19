"""Tests for the "what breaks if we change X" impact report (C9)."""

from __future__ import annotations

from cosmos77_ex04.extensions.impact_report import (
    god_node_betweenness,
    impacted_nodes,
    write_impact_md,
)


def test_impacted_nodes_returns_reverse_callers(model):
    # c is called by a and b -> both break if c changes.
    callers = impacted_nodes(model, "c")
    assert set(callers) == {"a", "b"}


def test_impacted_nodes_resolves_by_label(model):
    assert set(impacted_nodes(model, "helper")) == {"a", "b"}


def test_impacted_nodes_orphan_has_empty_blast_radius(model):
    assert impacted_nodes(model, "orph") == []


def test_impacted_nodes_unknown_target(model):
    assert impacted_nodes(model, "does-not-exist") == []


def test_god_node_betweenness_ranked(model):
    ranked = god_node_betweenness(model, top=3)
    scores = [s for _, s in ranked]
    assert scores == sorted(scores, reverse=True)
    assert len(ranked) <= 3


def test_write_impact_md_is_non_empty(tmp_path, model):
    out = write_impact_md(model, "helper", tmp_path / "IMPACT.md")
    text = out.read_text(encoding="utf-8")
    assert "what breaks if we change X" in text
    assert "Blast radius" in text
    assert "Betweenness" in text
    assert text.strip()
