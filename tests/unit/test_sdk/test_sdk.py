"""Tests for the SDK surface — prepare_target delegates, stubs raise (rule 2)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cosmos77_ex04.sdk import sdk as sdkmod
from cosmos77_ex04.target.checkout import BugTestResult, TargetInfo
from cosmos77_ex04.target.info import BugInfo


def test_prepare_target_delegates_to_harness(config, monkeypatch):
    captured: dict = {}
    fake = TargetInfo(
        "tqdm",
        1,
        Path("/w"),
        Path("/w/tqdm"),
        BugInfo("tqdm", 1, "3.6.9", "a", "b", "t"),
        BugTestResult(False, 1, "1 failed"),
    )

    class FakeHarness:
        def __init__(self, project, bug_id, workdir, bugsinpy_dir, **kwargs):
            captured["init"] = (project, bug_id, kwargs)
            self.bug_id = bug_id

        def ensure_clone(self):
            captured["clone"] = True

        def prepare(self):
            captured["prepare"] = True
            return fake

    monkeypatch.setattr(sdkmod, "BugsInPyHarness", FakeHarness)
    out = sdkmod.SDK(config=config).prepare_target()
    assert out is fake
    assert captured["clone"] and captured["prepare"]
    assert captured["init"][0] == "tqdm"
    assert captured["init"][2]["python_version"] == "3.8.20"


def test_prepare_target_bug_id_fallback(config_dir, monkeypatch):
    setup = json.loads((config_dir / "setup.json").read_text(encoding="utf-8"))
    setup["target"]["bug_id"] = None
    (config_dir / "setup.json").write_text(json.dumps(setup), encoding="utf-8")
    from cosmos77_ex04.shared.config import Config

    captured: dict = {}

    class FakeHarness:
        def __init__(self, *args, **kwargs):
            self.bug_id = args[1]
            captured["inst"] = self

        def ensure_clone(self):
            pass

        def prepare(self):
            return "OK"

    monkeypatch.setattr(sdkmod, "BugsInPyHarness", FakeHarness)
    monkeypatch.setattr(sdkmod, "list_bugs", lambda d, p: [3, 5])
    assert sdkmod.SDK(config=Config(config_dir)).prepare_target() == "OK"
    assert captured["inst"].bug_id == 3


def test_spec_sheet_returns_ledger(config):
    sdk = sdkmod.SDK(config=config)
    sdk.gatekeeper.record({"input_tokens": 4, "output_tokens": 6, "total_tokens": 10})
    sheet = sdk.spec_sheet()
    assert sheet["total_tokens"] == 10
    assert sheet["calls"] == 1


def test_repo_root_is_config_parent(config, config_dir):
    assert sdkmod.SDK(config=config).repo_root == config_dir.parent


@pytest.mark.parametrize(
    "method",
    [
        "build_vault",
        "extract_diagrams",
        "run_agent",
        "apply_fix",
        "compare_tokens",
        "run_extensions",
    ],
)
def test_unimplemented_stages_raise(config, method):
    with pytest.raises(NotImplementedError):
        getattr(sdkmod.SDK(config=config), method)()


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
