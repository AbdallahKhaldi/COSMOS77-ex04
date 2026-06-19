"""Tests for the comparison orchestrator (C8/C15 — no live calls, fully mocked)."""

from __future__ import annotations

import json
from pathlib import Path

from cosmos77_ex04.tokens import run as run_mod
from cosmos77_ex04.tokens.run import revert_to_buggy, run_comparison

_FIX = {
    "file": "pkg/mod.py",
    "search": "return foo(a, b)",
    "replace": "return foo(b, a)",
}


class FakeConfig:
    """A minimal stand-in for Config exposing only what run_comparison reads."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root

    def target(self):
        return {
            "project": "pkg",
            "package_subdir": "pkg",
            "workdir": "data/target",
            "failing_test": "pkg/tests::test_x",
        }

    def paths(self):
        return {"obsidian_dir": "obsidian", "reports_dir": "reports", "artifacts_dir": "artifacts"}

    def agent(self):
        return {"top_k": 6, "max_files": 4, "max_llm_calls": 6, "recursion_limit": 12}

    def get(self, dot_path, default=None):
        return _FIX if dot_path == "fix" else default


def _graph_json(path: Path) -> None:
    data = {
        "nodes": [{"id": "n1", "label": "foo", "source_file": "mod.py"}],
        "links": [],
    }
    path.write_text(json.dumps(data), encoding="utf-8")


def _scaffold(tmp_path: Path) -> Path:
    repo = tmp_path
    pkg = repo / "data" / "target" / "pkg" / "pkg"
    pkg.mkdir(parents=True)
    # the fixed (non-buggy) file — run_comparison must revert it to buggy
    (pkg / "mod.py").write_text("def f(a, b):\n    return foo(b, a)\n", encoding="utf-8")
    (repo / "obsidian").mkdir()
    (repo / "obsidian" / "index.md").write_text("# navigation hub", encoding="utf-8")
    artifacts = repo / "artifacts"
    artifacts.mkdir()
    _graph_json(artifacts / "graph.json")
    (repo / "data" / "target" / "_test_output.txt").write_text("Traceback", encoding="utf-8")
    return repo


def test_revert_to_buggy_undoes_a_prior_fix(tmp_path):
    f = tmp_path / "mod.py"
    f.write_text("return foo(b, a)\n", encoding="utf-8")
    assert revert_to_buggy(f, _FIX) is True
    assert f.read_text(encoding="utf-8") == "return foo(a, b)\n"
    # idempotent: already buggy → no change
    assert revert_to_buggy(f, _FIX) is False


def test_revert_to_buggy_guards_missing_file_and_empty_fix(tmp_path):
    missing = tmp_path / "nope.py"
    assert revert_to_buggy(missing, _FIX) is False
    present = tmp_path / "m.py"
    present.write_text("x", encoding="utf-8")
    assert revert_to_buggy(present, {"search": "", "replace": ""}) is False


def test_run_comparison_reverts_and_writes_reports(tmp_path, monkeypatch):
    repo = _scaffold(tmp_path)

    def fake_build_llm(config):
        return object()

    def fake_run_agent(deps, failing_test, *, recursion_limit=12):
        return {
            "diagnosis": "ROOT CAUSE",
            "suspects": ["foo"],
            "files_read": ["mod.py"],
            "iterations": 1,
            "tokens": {"input_tokens": 300, "output_tokens": 50, "total_tokens": 350, "calls": 1},
        }

    def fake_run_baseline(llm, gk, source_root, failing_test, test_output="", **kw):
        return {
            "diagnosis": "ROOT CAUSE",
            "files_read": ["mod.py", "other.py", "third.py"],
            "iterations": 1,
            "tokens": {"input_tokens": 900, "output_tokens": 60, "total_tokens": 960, "calls": 1},
        }

    monkeypatch.setattr(run_mod, "build_llm", fake_build_llm)
    monkeypatch.setattr(run_mod, "run_agent", fake_run_agent)
    monkeypatch.setattr(run_mod, "run_baseline", fake_run_baseline)

    result = run_comparison(FakeConfig(repo), repo)

    # the buggy state was restored for both arms
    buggy = (repo / "data" / "target" / "pkg" / "pkg" / "mod.py").read_text(encoding="utf-8")
    assert "return foo(a, b)" in buggy

    # measured comparison: guided is cheaper + reads fewer files (the C8 claim)
    assert result["comparison"]["tokens_saved"] == 610
    assert result["comparison"]["files_saved"] == 2
    assert result["comparison"]["pct_tokens_saved"] > 0

    # the three deliverables exist
    assert (repo / "reports" / "TOKEN_COMPARISON.md").exists()
    assert (repo / "reports" / "SPEC_SHEET.md").exists()
    assert (repo / "artifacts" / "token_comparison.pdf").exists()
    assert len(result["reports"]) == 3
