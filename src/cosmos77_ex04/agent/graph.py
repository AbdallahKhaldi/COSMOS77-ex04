"""Assemble + run the graph-guided StateGraph with bounded LLM calls (C5).

The flow is load_context → rank_suspects → request_snippets → diagnose →
(loop or END). Calls are bounded two ways: ``should_continue`` (a step counter)
and LangGraph's compiled ``recursion_limit`` — so the token cost is provable.
"""

from __future__ import annotations

from functools import partial
from pathlib import Path
from typing import Any

from langgraph.graph import END, START, StateGraph

from cosmos77_ex04.agent import nodes
from cosmos77_ex04.agent.analysis import write_bug_analysis
from cosmos77_ex04.agent.llm import build_llm
from cosmos77_ex04.agent.retrieval import read_text_file
from cosmos77_ex04.agent.state import AgentDeps, AgentState
from cosmos77_ex04.graphify.model import GraphModel


def build_graph(deps: AgentDeps) -> Any:
    """Compile the StateGraph with each node bound to the injected dependencies."""
    sg: StateGraph = StateGraph(AgentState)
    sg.add_node("load_context", partial(nodes.load_context, deps=deps))
    sg.add_node("rank_suspects", partial(nodes.rank_suspects_node, deps=deps))
    sg.add_node("request_snippets", partial(nodes.request_snippets, deps=deps))
    sg.add_node("diagnose", partial(nodes.diagnose, deps=deps))
    sg.add_edge(START, "load_context")
    sg.add_edge("load_context", "rank_suspects")
    sg.add_edge("rank_suspects", "request_snippets")
    sg.add_edge("request_snippets", "diagnose")
    sg.add_conditional_edges(
        "diagnose",
        partial(nodes.should_continue, deps=deps),
        {"continue": "request_snippets", "end": END},
    )
    return sg.compile()


def run_agent(deps: AgentDeps, failing_test: str, *, recursion_limit: int = 12) -> dict[str, Any]:
    """Run the bounded investigation and return diagnosis + ledger + files_read."""
    initial: AgentState = {
        "failing_test": failing_test,
        "context": "",
        "suspects": [],
        "files_read": [],
        "snippets": {},
        "diagnosis": "",
        "step_count": 0,
        "done": False,
    }
    final = build_graph(deps).invoke(initial, config={"recursion_limit": recursion_limit})
    return {
        "diagnosis": final["diagnosis"],
        "suspects": [deps.model.label_of(s) for s in final["suspects"]],
        "files_read": final["files_read"],
        "iterations": final["step_count"],
        "tokens": deps.gatekeeper.ledger(),
    }


def investigate(config: Any, gatekeeper: Any, model: GraphModel, repo_root: Path) -> dict[str, Any]:
    """High-level entry: build deps from config, run the agent, write BUG_ANALYSIS.md."""
    paths = config.paths()
    target = config.target()
    agent_cfg = config.agent()
    project = target.get("project", "tqdm")
    source = (
        repo_root
        / target.get("workdir", "data/target")
        / project
        / target.get("package_subdir", project)
    )
    test_output = read_text_file(
        repo_root / target.get("workdir", "data/target") / "_test_output.txt"
    )
    deps = AgentDeps(
        model=model,
        llm=build_llm(config),
        gatekeeper=gatekeeper,
        vault_dir=repo_root / paths.get("obsidian_dir", "obsidian"),
        source_root=source,
        test_output=test_output,
        top_k=int(agent_cfg.get("top_k", 5)),
        max_files=int(agent_cfg.get("max_files", 4)),
        max_calls=int(agent_cfg.get("max_llm_calls", 6)),
    )
    failing_test = target.get("failing_test", "")
    result = run_agent(
        deps, failing_test, recursion_limit=int(agent_cfg.get("recursion_limit", 12))
    )
    write_bug_analysis(
        result, failing_test, repo_root / paths.get("reports_dir", "reports") / "BUG_ANALYSIS.md"
    )
    return result
