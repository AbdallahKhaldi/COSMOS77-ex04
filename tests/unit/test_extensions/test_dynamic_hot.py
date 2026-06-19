"""Tests for the dynamic hot.md (git diff mocked — no live git, rule 6)."""

from __future__ import annotations

from types import SimpleNamespace

from cosmos77_ex04.extensions.dynamic_hot import changed_files_from_git, rebuild_hot


def _runner(stdout: str):
    """A subprocess.run stand-in returning a fixed stdout."""
    return lambda *a, **k: SimpleNamespace(stdout=stdout, returncode=0)


def test_changed_files_parses_git_output():
    runner = _runner("tqdm/contrib/__init__.py\ntqdm/std.py\n\n")
    changed = changed_files_from_git("/repo", runner=runner)
    assert changed == ["tqdm/contrib/__init__.py", "tqdm/std.py"]


def test_changed_files_empty_when_clean():
    assert changed_files_from_git("/repo", runner=_runner("")) == []


def test_rebuild_hot_from_changed_files(tmp_path, model):
    out = rebuild_hot(model, ["pkg/contrib_init.py"], tmp_path / "hot.md")
    text = out.read_text(encoding="utf-8")
    assert "kind: hot" in text
    assert "tenumerate (changed)" in text  # matched node
    assert "1-hop neighbours" in text  # its neighbourhood is reported


def test_rebuild_hot_falls_back_to_god_nodes_when_empty(tmp_path, model):
    out = rebuild_hot(model, [], tmp_path / "hot.md")
    text = out.read_text(encoding="utf-8")
    assert "God Nodes" in text
    assert "tqdm" in text  # the top God Node, never empty


def test_rebuild_hot_orphan_changed_has_no_neighbours(tmp_path, model):
    out = rebuild_hot(model, ["dead.py"], tmp_path / "hot.md")
    assert "orphan/isolated node" in out.read_text(encoding="utf-8")
