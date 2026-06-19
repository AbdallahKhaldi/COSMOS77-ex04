"""Tests for build_vault: structure, resolving wikilinks, hot/index content (C2)."""

from __future__ import annotations

from cosmos77_ex04.vault.build import _seed_ids, build_vault

from .fixtures import ReportStub, all_wikilink_targets, make_model, written_stems


def _build(tmp_path):
    model = make_model()
    manifest = build_vault(
        model, ReportStub(), tmp_path, failing_test="tests/test_iter.py::test_enumerate"
    )
    return model, manifest


def test_build_writes_static_pages_and_pages(tmp_path):
    _, manifest = _build(tmp_path)
    for name in ("index", "hot", "suspects", "investigation", "fix-process"):
        assert (tmp_path / f"{name}.md").exists()
    assert (tmp_path / "pages").is_dir()
    assert manifest["files"] == manifest["pages"] + 5
    assert manifest["pages"] > 0
    assert manifest["communities"] == 2
    assert manifest["god_nodes"]


def test_every_wikilink_resolves(tmp_path):
    """The core invariant: no dangling [[link]] anywhere in the vault."""
    _build(tmp_path)
    stems = written_stems(tmp_path)
    targets = all_wikilink_targets(tmp_path)
    assert targets, "expected wikilinks to be emitted"
    dangling = [(str(f), t) for f, t in targets if t not in stems]
    assert not dangling, f"dangling wikilinks: {dangling}"


def test_index_links_hot_suspects_communities_and_god(tmp_path):
    _build(tmp_path)
    text = (tmp_path / "index.md").read_text(encoding="utf-8")
    assert "[[hot" in text
    assert "[[suspects" in text
    assert "Community" in text and "[[Community 0" in text
    assert "[[hub.py" in text  # a god-node page link
    assert "question → index → 2-3 pages → answer" in text


def test_hot_contains_god_nodes_and_enumerate_node(tmp_path):
    _build(tmp_path)
    text = (tmp_path / "hot.md").read_text(encoding="utf-8")
    assert "God Node" in text
    assert "Failing-test neighborhood" in text
    assert "enumerate_items" in text  # seeded from the failing_test token
    assert "[[hub.py" in text  # the top god-node as a wikilink


def test_filenames_sanitized_no_separators(tmp_path):
    _build(tmp_path)
    for md in (tmp_path / "pages").glob("*.md"):
        assert "/" not in md.stem and "\\" not in md.stem
        assert ":" not in md.stem


def test_duplicate_labels_get_unique_stems(tmp_path):
    """Two nodes labelled __init__.py must not collide on disk."""
    model, manifest = _build(tmp_path)
    # both __init__.py nodes are god-nodes (degree-ranked); ensure 2 distinct files.
    init_pages = list((tmp_path / "pages").glob("__init__.py*.md"))
    assert len(init_pages) >= 2
    assert len({p.stem for p in init_pages}) == len(init_pages)


def test_node_page_shows_tiers_community_and_centrality(tmp_path):
    _build(tmp_path)
    hub = (tmp_path / "pages" / "hub.py.md").read_text(encoding="utf-8")
    assert "Extracted" in hub and "Inferred" in hub and "Ambiguous" in hub
    assert "Centrality" in hub
    assert "[[Community 0" in hub
    assert "kind:" in hub  # frontmatter


def test_empty_failing_test_still_builds(tmp_path):
    model = make_model()
    manifest = build_vault(model, ReportStub(), tmp_path, failing_test="")
    assert (tmp_path / "hot.md").exists()
    assert manifest["pages"] > 0


def test_seed_ids_appends_token_match_outside_god_nodes():
    """A node named in the failing test joins the seed set even if not a god-node."""
    model = make_model()
    seeds = _seed_ids(model, god_ids=["hub"], failing_test="iter.py::test enumerate items")
    assert "enum" in seeds  # label 'enumerate_items' matched the 'enumerate' token
    assert seeds[0] == "hub"  # god-nodes lead, token matches follow


def test_capped_top_gods_and_comms_keeps_links_resolving(tmp_path):
    """With tight caps, unregistered nodes/communities fall back to plain text."""
    model = make_model()
    build_vault(model, ReportStub(), tmp_path, top_gods=1, top_comms=1)
    stems = written_stems(tmp_path)
    dangling = [(str(f), t) for f, t in all_wikilink_targets(tmp_path) if t not in stems]
    assert not dangling
    # Only Community 0 has a page; the index lists Community 1 as plain text.
    index = (tmp_path / "index.md").read_text(encoding="utf-8")
    assert "Community 0" in index
