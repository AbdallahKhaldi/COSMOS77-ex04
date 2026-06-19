"""Tests for the wikilink emit, PageRegistry, and render helpers (C2)."""

from __future__ import annotations

import pytest

from cosmos77_ex04.vault.links import PageRegistry
from cosmos77_ex04.vault.pages import render_hot, render_node_page
from cosmos77_ex04.vault.render import (
    community_link,
    neighbor_links,
    node_role_line,
    tier_breakdown,
)
from cosmos77_ex04.vault.wikilinks import frontmatter, sanitize_filename, wikilink

from .fixtures import make_model


@pytest.mark.parametrize(
    ("raw", "expected_clean"),
    [
        ("pkg/a/b.py", "pkg a b.py"),
        ('weird:name*?"<>|here', "weird name here"),
        ("  spaced   out  ", "spaced out"),
        ("", "untitled"),
        ("...", "untitled"),
    ],
)
def test_sanitize_filename_strips_forbidden(raw, expected_clean):
    out = sanitize_filename(raw)
    for ch in '/\\:*?"<>|':
        assert ch not in out
    assert out == expected_clean
    assert out  # never empty


def test_wikilink_plain_and_alias_forms():
    assert wikilink("stem") == "[[stem]]"
    assert wikilink("stem", "Alias") == "[[stem|Alias]]"
    assert wikilink("stem", "stem") == "[[stem]]"  # alias == stem collapses


def test_frontmatter_is_yaml_fenced():
    block = frontmatter({"kind": "node", "community": "0"})
    lines = block.splitlines()
    assert lines[0] == "---" and lines[-1] == "---"
    assert "kind: node" in lines
    assert "community: 0" in lines


def test_registry_uniqueness_and_has():
    reg = PageRegistry()
    s1 = reg.register("n1", "__init__.py")
    s2 = reg.register("n2", "__init__.py")
    assert s1 != s2  # duplicate label -> unique stems
    assert reg.has("n1") and reg.has("n2")
    assert not reg.has("missing")
    assert reg.register("n1", "__init__.py") == s1  # idempotent


def test_registry_stem_of_raises_for_unknown():
    reg = PageRegistry()
    with pytest.raises(KeyError):
        reg.stem_of("nope")


def test_registry_link_resolves_to_stem():
    reg = PageRegistry()
    stem = reg.register("k", "Some Label")
    assert reg.link("k") == f"[[{stem}]]"
    assert reg.link("k", "Alias") == f"[[{stem}|Alias]]"


def test_community_key_distinct_from_node_id():
    assert PageRegistry.community_key(0) == "community:0"


def test_neighbor_links_falls_back_to_plain_when_no_page():
    model = make_model()
    reg = PageRegistry()
    reg.register("hub", "hub.py")  # only hub has a page; neighbors do not
    out = neighbor_links(model, "hub", reg)
    assert "[[hub.py" not in out  # hub is not its own neighbor
    assert "__init__.py" in out  # neighbor printed plain (no wikilink)
    assert "[[" not in out


def test_neighbor_links_empty_when_isolated():
    model = make_model()
    reg = PageRegistry()
    assert "no neighbors" in neighbor_links(model, "missing", reg)


def test_tier_breakdown_counts_all_three_tiers():
    model = make_model()
    out = tier_breakdown(model, "hub")
    assert "Extracted: 2" in out
    assert "Inferred: 1" in out
    assert "Ambiguous: 1" in out


def test_node_role_line_mentions_centrality_and_bridge():
    model = make_model()
    line = node_role_line(model, "hub")
    assert "Centrality" in line
    assert "betweenness" in line
    assert "Bridge" in line


def test_registry_stems_lists_all_assigned():
    reg = PageRegistry()
    reg.register("k1", "a")
    reg.register("k2", "b")
    assert set(reg.stems()) == {"a", "b"}


def test_community_link_plain_when_unregistered():
    reg = PageRegistry()
    assert community_link(reg, 7) == "Community 7"  # no page -> plain, not a link
    reg.register(PageRegistry.community_key(7), "Community 7")
    assert community_link(reg, 7).startswith("[[")


def test_render_hot_skips_seed_id_absent_from_model():
    model = make_model()
    reg = PageRegistry()
    reg.register("hub", "hub.py")
    text = render_hot(model, reg, "test_x", seed_ids=["hub", "ghost-id"])
    assert "Failing-test neighborhood" in text
    assert "ghost-id" not in text  # absent ids are skipped, never emitted


def test_render_node_page_links_community_when_registered():
    model = make_model()
    reg = PageRegistry()
    reg.register("hub", "hub.py")
    reg.register(PageRegistry.community_key(0), "Community 0")
    page = render_node_page(model, "hub", reg)
    assert "[[Community 0" in page
    assert "Extracted" in page
