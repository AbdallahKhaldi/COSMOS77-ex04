"""Tests for the SDK pipeline stages — graphify + vault (rule 6, mocked I/O)."""

from __future__ import annotations

import json
from pathlib import Path

from cosmos77_ex04.sdk import sdk as sdkmod

_NODE = {"file_type": "code", "community": 0, "community_name": "Community 0"}


def _graph():
    return {
        "nodes": [
            {"id": "a", "label": "tqdm", "source_file": "std.py", **_NODE},
            {"id": "b", "label": "tenumerate", "source_file": "std.py", **_NODE},
            {
                "id": "c",
                "label": "utils",
                "source_file": "utils.py",
                "file_type": "code",
                "community": 1,
                "community_name": "Community 1",
            },
        ],
        "links": [
            {
                "source": "a",
                "target": "b",
                "relation": "calls",
                "confidence": "EXTRACTED",
                "confidence_score": 1.0,
            },
            {
                "source": "b",
                "target": "c",
                "relation": "uses",
                "confidence": "INFERRED",
                "confidence_score": 0.8,
            },
        ],
    }


def test_build_vault_generates_index_and_hot(config):
    repo_root = config.config_dir.parent
    artifacts = repo_root / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    (artifacts / "graph.json").write_text(json.dumps(_graph()), encoding="utf-8")
    (artifacts / "GRAPH_REPORT.md").write_text("# Graph Report\n", encoding="utf-8")
    summary = sdkmod.SDK(config=config).build_vault()
    assert summary["files"] >= 5
    assert (repo_root / "obsidian" / "index.md").exists()
    assert (repo_root / "obsidian" / "hot.md").exists()


def test_run_graphify_summarises_graph(config, monkeypatch):
    graph = {
        "nodes": [{"id": "a", "label": "a"}, {"id": "b", "label": "b"}],
        "links": [
            {
                "source": "a",
                "target": "b",
                "relation": "calls",
                "confidence": "EXTRACTED",
                "confidence_score": 1.0,
            }
        ],
    }

    def fake_cli(source, work, artifacts, backend=None, force=False):
        Path(artifacts).mkdir(parents=True, exist_ok=True)
        (Path(artifacts) / "graph.json").write_text(json.dumps(graph), encoding="utf-8")
        return {}

    monkeypatch.setattr(sdkmod, "run_graphify_cli", fake_cli)
    out = sdkmod.SDK(config=config).run_graphify()
    assert out["nodes"] == 2
    assert out["edges"] == 1
    assert "extracted" in out["tiers"]


def test_run_graphify_falls_back_when_cli_missing(config, monkeypatch):
    def boom(*args, **kwargs):
        raise FileNotFoundError("graphify not installed")

    def fake_fallback(source, out_path):
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        Path(out_path).write_text(
            json.dumps({"nodes": [{"id": "x", "label": "x"}], "links": []}), encoding="utf-8"
        )
        return Path(out_path)

    def fake_copy(graph_dir, artifacts):
        Path(artifacts).mkdir(parents=True, exist_ok=True)
        (Path(artifacts) / "graph.json").write_text(
            (Path(graph_dir) / "graph.json").read_text(encoding="utf-8"), encoding="utf-8"
        )
        return {"graph.json": Path(artifacts) / "graph.json"}

    monkeypatch.setattr(sdkmod, "run_graphify_cli", boom)
    monkeypatch.setattr(sdkmod, "write_fallback", fake_fallback)
    monkeypatch.setattr(sdkmod, "copy_artifacts", fake_copy)
    out = sdkmod.SDK(config=config).run_graphify()
    assert out["nodes"] == 1
