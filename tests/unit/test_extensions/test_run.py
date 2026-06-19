"""Tests for the extensions orchestrator (fixture graph.json, mocked git)."""

from __future__ import annotations

import json
from types import SimpleNamespace

from cosmos77_ex04.extensions.run import run_extensions

_GRAPH = {
    "directed": True,
    "nodes": [
        {"id": "a", "label": "tqdm", "source_file": "std.py", "community": 0},
        {"id": "b", "label": "tenumerate", "source_file": "contrib_init.py", "community": 0},
        {"id": "c", "label": "helper", "source_file": "utils.py", "community": 1},
        {"id": "orph", "label": "lonely", "source_file": "dead.py", "community": 2},
    ],
    "links": [
        {"source": "a", "target": "b", "relation": "calls", "confidence": "EXTRACTED"},
        {"source": "a", "target": "c", "relation": "calls", "confidence": "EXTRACTED"},
    ],
}


def _config():
    return {
        "target": {"failing_test": "test_enumerate", "workdir": "data/target", "project": "tqdm"},
        "fix": {"file": "tqdm/contrib/__init__.py"},
        "paths": {
            "obsidian_dir": "obsidian",
            "reports_dir": "reports",
            "artifacts_dir": "artifacts",
        },
    }


def _make_repo(tmp_path):
    (tmp_path / "artifacts").mkdir()
    (tmp_path / "artifacts" / "graph.json").write_text(json.dumps(_GRAPH), encoding="utf-8")
    return tmp_path


def _runner(stdout: str = ""):
    """A subprocess.run stand-in returning a fixed git diff stdout."""

    def run(*_a, **_k):
        return SimpleNamespace(stdout=stdout, returncode=0)

    return run


def test_run_extensions_writes_all_four(tmp_path):
    repo = _make_repo(tmp_path)
    result = run_extensions(_config(), repo, runner=_runner(""))  # clean tree

    for key in ("suspects", "hot", "orphans", "impact"):
        assert result[key].exists(), key
        assert result[key].read_text(encoding="utf-8").strip()
    assert result["orphan_count"] == 1  # 'orph'
    assert result["top_suspect"] == "tqdm"


def test_run_extensions_uses_git_changed_files(tmp_path):
    repo = _make_repo(tmp_path)
    result = run_extensions(_config(), repo, runner=_runner("contrib_init.py\n"))
    hot = result["hot"].read_text(encoding="utf-8")
    assert "tenumerate (changed)" in hot  # tracked the git-changed node


def test_run_extensions_returns_expected_keys(tmp_path):
    repo = _make_repo(tmp_path)
    result = run_extensions(_config(), repo, runner=_runner(""))
    assert set(result) == {"suspects", "hot", "orphans", "impact", "orphan_count", "top_suspect"}


def test_run_extensions_falls_back_to_god_node_without_fix(tmp_path):
    # No 'fix' config + clean tree -> impact targets the top God Node, hot uses gods.
    repo = _make_repo(tmp_path)
    config = _config()
    del config["fix"]
    result = run_extensions(config, repo, runner=_runner(""))
    impact = result["impact"].read_text(encoding="utf-8")
    assert "tqdm" in impact  # the top God Node became the changed component
    assert "God Nodes" in result["hot"].read_text(encoding="utf-8")
