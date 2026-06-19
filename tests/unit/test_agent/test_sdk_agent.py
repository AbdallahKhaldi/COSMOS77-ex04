"""SDK-level test for run_agent → BUG_ANALYSIS.md (C5, real Gemini mocked)."""

from __future__ import annotations

import json

from langchain_core.messages import AIMessage

from cosmos77_ex04.agent import graph as agentgraph
from cosmos77_ex04.sdk import sdk as sdkmod

_GRAPH = {
    "nodes": [
        {
            "id": "a",
            "label": "tqdm",
            "source_file": "std.py",
            "file_type": "code",
            "community": 0,
            "community_name": "Community 0",
        },
        {
            "id": "b",
            "label": "tenumerate",
            "source_file": "std.py",
            "file_type": "code",
            "community": 0,
            "community_name": "Community 0",
        },
    ],
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


class _FakeLLM:
    def invoke(self, prompt):
        return AIMessage(
            content="ROOT CAUSE: x\nFILE: std.py",
            usage_metadata={"input_tokens": 50, "output_tokens": 10, "total_tokens": 60},
        )


def test_run_agent_writes_bug_analysis(config, monkeypatch):
    monkeypatch.setattr(agentgraph, "build_llm", lambda config: _FakeLLM())
    repo_root = config.config_dir.parent
    artifacts = repo_root / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    (artifacts / "graph.json").write_text(json.dumps(_GRAPH), encoding="utf-8")
    vault = repo_root / "obsidian"
    vault.mkdir(parents=True, exist_ok=True)
    (vault / "index.md").write_text("# Index", encoding="utf-8")
    (vault / "hot.md").write_text("# hot", encoding="utf-8")
    src = repo_root / "data" / "target" / "tqdm" / "tqdm"
    src.mkdir(parents=True, exist_ok=True)
    (src / "std.py").write_text("def f():\n    return 1\n", encoding="utf-8")
    result = sdkmod.SDK(config=config).run_agent()
    assert "ROOT CAUSE" in result["diagnosis"]
    assert (repo_root / "reports" / "BUG_ANALYSIS.md").exists()
    assert result["tokens"]["calls"] == 1
