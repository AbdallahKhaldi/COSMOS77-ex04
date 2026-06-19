"""Tests for orphan/isolated-node discovery and classification (C9)."""

from __future__ import annotations

from cosmos77_ex04.extensions.orphans import classify_orphan, find_orphans, write_orphans_md


def test_find_orphans_finds_isolated_nodes(model):
    orphans = find_orphans(model)
    assert "orph" in orphans  # no in/out edges
    assert "_helper" in orphans  # also isolated
    assert "a" not in orphans  # connected hub is not an orphan


def test_classify_underscore_is_intentional(model):
    assert classify_orphan(model, "_helper") == "intentional (adapter/legacy)"


def test_classify_plain_orphan_is_dead_code(model):
    assert classify_orphan(model, "orph") == "possible dead code"


def test_classify_marker_label_is_intentional(model):
    # 'compat' substring in the label flags it as a legacy shim.
    model.nodes["orph"].label = "compat_shim"
    assert classify_orphan(model, "orph") == "intentional (adapter/legacy)"


def test_write_orphans_md_is_non_empty(tmp_path, model):
    out = write_orphans_md(model, tmp_path / "ORPHANS.md")
    text = out.read_text(encoding="utf-8")
    assert "ORPHANS.md" in text
    assert "| Orphan | File | Classification |" in text
    assert "lonely" in text
    assert text.strip()
