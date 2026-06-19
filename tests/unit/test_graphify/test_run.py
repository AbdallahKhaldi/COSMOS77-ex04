"""Tests for the Graphify CLI runner + artifact copy (rule 6 — CLI mocked)."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from cosmos77_ex04.graphify import run


def _ok(**_kwargs):
    return SimpleNamespace(returncode=0, stdout="", stderr="")


def test_extract_cmd_flags():
    assert run.extract_cmd(Path("/src"), Path("/out"), "gemini") == [
        "graphify",
        "extract",
        "/src",
        "--backend",
        "gemini",
        "--out",
        "/out",
    ]


def test_cluster_cmd():
    assert run.cluster_cmd(Path("/out")) == ["graphify", "cluster-only", "/out"]


def test_out_graph_dir():
    assert run.out_graph_dir(Path("/out")) == Path("/out/graphify-out")


def test_copy_artifacts_copies_present_only(tmp_path):
    graph_dir = tmp_path / "graphify-out"
    graph_dir.mkdir()
    (graph_dir / "graph.json").write_text("{}", encoding="utf-8")
    (graph_dir / "GRAPH_REPORT.md").write_text("# r", encoding="utf-8")
    copied = run.copy_artifacts(graph_dir, tmp_path / "artifacts")
    assert set(copied) == {"graph.json", "GRAPH_REPORT.md"}
    assert (tmp_path / "artifacts" / "graph.json").exists()


def test_run_graphify_reuses_existing(tmp_path):
    graph_dir = tmp_path / "work" / "graphify-out"
    graph_dir.mkdir(parents=True)
    (graph_dir / "graph.json").write_text('{"nodes": []}', encoding="utf-8")
    (graph_dir / "GRAPH_REPORT.md").write_text("# report", encoding="utf-8")
    called: list = []

    def runner(cmd, **_kwargs):
        called.append(cmd)
        return _ok()

    copied = run.run_graphify(
        tmp_path / "src", tmp_path / "work", tmp_path / "artifacts", runner=runner
    )
    assert called == []
    assert {"graph.json", "GRAPH_REPORT.md"} <= set(copied)


def test_run_graphify_clusters_when_report_missing(tmp_path):
    graph_dir = tmp_path / "work" / "graphify-out"
    graph_dir.mkdir(parents=True)
    (graph_dir / "graph.json").write_text('{"nodes": []}', encoding="utf-8")
    called: list = []

    def runner(cmd, **_kwargs):
        called.append(cmd)
        return _ok()

    run.run_graphify(tmp_path / "src", tmp_path / "work", tmp_path / "artifacts", runner=runner)
    assert called == [run.cluster_cmd(tmp_path / "work")]


def test_run_graphify_invokes_when_absent(tmp_path):
    out = tmp_path / "work"

    def runner(cmd, **_kwargs):
        graph_dir = out / "graphify-out"
        graph_dir.mkdir(parents=True, exist_ok=True)
        (graph_dir / "graph.json").write_text('{"nodes": []}', encoding="utf-8")
        return _ok()

    copied = run.run_graphify(tmp_path / "src", out, tmp_path / "artifacts", runner=runner)
    assert "graph.json" in copied


def test_run_graphify_raises_without_output(tmp_path):
    def runner(cmd, **_kwargs):
        return SimpleNamespace(returncode=1, stdout="", stderr="boom")

    with pytest.raises(FileNotFoundError):
        run.run_graphify(tmp_path / "src", tmp_path / "work", tmp_path / "artifacts", runner=runner)


def test_run_graphify_force_reinvokes(tmp_path):
    graph_dir = tmp_path / "work" / "graphify-out"
    graph_dir.mkdir(parents=True)
    (graph_dir / "graph.json").write_text('{"nodes": []}', encoding="utf-8")
    called: list = []

    def runner(cmd, **_kwargs):
        called.append(cmd)
        return _ok()

    run.run_graphify(
        tmp_path / "src", tmp_path / "work", tmp_path / "artifacts", force=True, runner=runner
    )
    assert called
