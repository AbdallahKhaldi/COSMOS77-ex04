"""The LangGraph nodes: graph-guided-FIRST, then targeted snippets, then diagnose (C5).

Order is enforced by the graph edges (graph.py): ``load_context`` (no source) →
``rank_suspects`` → ``request_snippets`` (ONLY the ranked suspects) → ``diagnose``
(one bounded LLM call). ``should_continue`` halts on diagnosis or the call cap.
"""

from __future__ import annotations

from cosmos77_ex04.agent.llm import invoke_diagnose
from cosmos77_ex04.agent.retrieval import fetch_snippets, graph_summary, rank_suspects, read_vault
from cosmos77_ex04.agent.state import AgentDeps, AgentState

_PROMPT = """You are a senior Python debugger investigating a FAILING test in the tqdm project.
Failing test: {failing_test}

You are given FOCUSED context from a knowledge graph — NOT the whole repository
(that would dilute signal and bury the bug in the middle). Use it to find the bug.

# Focused graph context (navigation hub + bug-critical area + graph summary)
{context}

# Suspect sources the graph pointed to (the ONLY files read)
{snippets}

Identify the ROOT CAUSE. Answer with exactly these sections:
ROOT CAUSE: <one sentence>
FILE: <the faulty file>
FAULTY CODE: <the faulty line or expression>
MINIMAL FIX: <the smallest change that fixes it>
"""


def load_context(state: AgentState, deps: AgentDeps) -> dict:
    """Read the navigation hub + hot.md + graph summary + the failing-test traceback."""
    vault = read_vault(deps.vault_dir)
    trace = (
        f"\n\n## Failing-test output (traceback)\n{deps.test_output}" if deps.test_output else ""
    )
    return {"context": f"{graph_summary(deps.model)}\n\n{vault}{trace}"}


def rank_suspects_node(state: AgentState, deps: AgentDeps) -> dict:
    """Rank suspects by Centrality + proximity to the failing test + traceback files."""
    suspects = rank_suspects(deps.model, state["failing_test"], deps.top_k, deps.test_output)
    return {"suspects": suspects}


def request_snippets(state: AgentState, deps: AgentDeps) -> dict:
    """Fetch ONLY the top suspects' source files (targeted; never the whole repo)."""
    snippets, files_read = fetch_snippets(
        deps.model, state["suspects"], deps.source_root, deps.max_files
    )
    return {"snippets": snippets, "files_read": files_read}


def diagnose(state: AgentState, deps: AgentDeps) -> dict:
    """The single bounded LLM call: focused context + targeted snippets → root cause."""
    snippet_text = "\n\n".join(
        f"### {name}\n```python\n{code}\n```" for name, code in state["snippets"].items()
    )
    prompt = _PROMPT.format(
        failing_test=state["failing_test"], context=state["context"], snippets=snippet_text
    )
    diagnosis = invoke_diagnose(deps.llm, prompt, deps.gatekeeper)
    return {"diagnosis": diagnosis, "step_count": state["step_count"] + 1, "done": True}


def should_continue(state: AgentState, deps: AgentDeps) -> str:
    """Stop when diagnosed or the call cap is reached (the token-provable bound)."""
    if state.get("done") or state["step_count"] >= deps.max_calls:
        return "end"
    return "continue"
