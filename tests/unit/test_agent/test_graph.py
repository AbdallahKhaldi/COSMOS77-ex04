"""Tests for the graph-guided agent run (C5 — LLM mocked, invariants asserted)."""

from __future__ import annotations

from langchain_core.messages import AIMessage

from cosmos77_ex04.agent.graph import run_agent
from cosmos77_ex04.agent.state import AgentDeps
from cosmos77_ex04.graphify.model import Edge, GraphModel, Node
from cosmos77_ex04.shared.gatekeeper import Gatekeeper


class FakeLLM:
    """Records prompts and returns a canned diagnosis with usage_metadata."""

    def __init__(self):
        self.prompts: list[str] = []

    def invoke(self, prompt):
        self.prompts.append(prompt)
        return AIMessage(
            content="ROOT CAUSE: prefix is an int\nFILE: std.py\nFAULTY CODE: prefix[-2:]",
            usage_metadata={"input_tokens": 120, "output_tokens": 30, "total_tokens": 150},
        )


def _model():
    nodes = [
        Node("a", "tqdm", "std.py", "code", 0, "Community 0"),
        Node("b", "tenumerate", "std.py", "code", 0, "Community 0"),
        Node("c", "helper", "utils.py", "code", 1, "Community 1"),
        Node("d", "unused", "other.py", "code", 1, "Community 1"),
    ]
    edges = [
        Edge("a", "b", "calls", "extracted", 1.0),
        Edge("b", "c", "uses", "inferred", 0.8),
        Edge("a", "c", "calls", "extracted", 1.0),
    ]
    return GraphModel(nodes, edges)


def _env(tmp_path):
    vault = tmp_path / "obsidian"
    vault.mkdir()
    (vault / "index.md").write_text("# Index — navigation hub", encoding="utf-8")
    (vault / "hot.md").write_text("# hot — bug-critical area", encoding="utf-8")
    src = tmp_path / "src"
    src.mkdir()
    (src / "std.py").write_text(
        "def f():\n    prefix = 1\n    return prefix[-2:]\n", encoding="utf-8"
    )
    (src / "utils.py").write_text("def helper():\n    return 2\n", encoding="utf-8")
    (src / "other.py").write_text("SECRET_DO_NOT_READ = 'x'\n", encoding="utf-8")
    return vault, src


def test_agent_is_graph_first_targeted_and_metered(tmp_path):
    vault, src = _env(tmp_path)
    llm = FakeLLM()
    gk = Gatekeeper()
    deps = AgentDeps(_model(), llm, gk, vault, src, top_k=3, max_files=4, max_calls=6)
    result = run_agent(deps, "tqdm/tests/tests_contrib.py::test_enumerate")

    assert "ROOT CAUSE" in result["diagnosis"]
    assert result["iterations"] == 1
    assert len(llm.prompts) == 1
    # graph-FIRST: the prompt carries the vault hub + graph summary
    assert "navigation hub" in llm.prompts[0]
    assert "communities" in llm.prompts[0]
    # targeted: only suspect files; NEVER the non-suspect other.py
    assert "other.py" not in result["files_read"]
    assert "std.py" in result["files_read"]
    assert "SECRET_DO_NOT_READ" not in llm.prompts[0]
    # metered: the ledger recorded the call (the evidence behind C8)
    assert gk.ledger()["total_tokens"] == 150
    assert gk.ledger()["calls"] == 1


def test_step_cap_bounds_the_run(tmp_path):
    vault, src = _env(tmp_path)
    deps = AgentDeps(_model(), FakeLLM(), Gatekeeper(), vault, src, max_calls=1)
    result = run_agent(deps, "test_enumerate")
    assert result["iterations"] <= 1
