"""Agent state + dependency bundle for the graph-guided LangGraph agent (C5)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypedDict

from cosmos77_ex04.graphify.model import GraphModel
from cosmos77_ex04.shared.gatekeeper import Gatekeeper


class AgentState(TypedDict):
    """The LangGraph state threaded through the investigation."""

    failing_test: str
    context: str
    suspects: list[str]
    files_read: list[str]
    snippets: dict[str, str]
    diagnosis: str
    step_count: int
    done: bool


@dataclass
class AgentDeps:
    """Everything the nodes need — injected so unit tests pass a fake LLM (rule 6)."""

    model: GraphModel
    llm: Any
    gatekeeper: Gatekeeper
    vault_dir: Path
    source_root: Path
    test_output: str = ""
    top_k: int = 5
    max_files: int = 4
    max_calls: int = 6
