"""Run the Graphify CLI on the target and persist artifacts (C1).

graphify 0.8.42's headless build is ``graphify extract <src> --backend <b>
--out <dir>``, which writes ``<dir>/graphify-out/{graph.json, GRAPH_REPORT.md,
graph.html, ...}`` — AST extraction is near-free; only the semantic pass spends
LLM tokens. We copy the three core artifacts into ``artifacts/``. The call is
injectable so unit tests mock it (rule 6); it is idempotent (an existing
graph.json is reused unless ``force``). If the CLI is unavailable/fails, the SDK
falls back to the DIY ast+networkx builder (ADR-003) so graph.json always exists.
"""

from __future__ import annotations

import shutil
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

#: The core artifacts copied from graphify-out/ into artifacts/.
ARTIFACT_FILES = ("graph.json", "GRAPH_REPORT.md", "graph.html")


def extract_cmd(source: Path, out_dir: Path, backend: str = "gemini") -> list[str]:
    """Build the ``graphify extract`` command line (AST + optional semantic pass)."""
    return ["graphify", "extract", str(source), "--backend", backend, "--out", str(out_dir)]


def cluster_cmd(out_dir: Path) -> list[str]:
    """Build the ``graphify cluster-only`` command (writes GRAPH_REPORT.md + graph.html)."""
    return ["graphify", "cluster-only", str(out_dir)]


def out_graph_dir(out_dir: Path) -> Path:
    """The ``graphify-out`` directory graphify writes inside ``out_dir``."""
    return Path(out_dir) / "graphify-out"


def copy_artifacts(graph_dir: Path, artifacts_dir: Path) -> dict[str, Path]:
    """Copy the core artifacts that exist from ``graph_dir`` into ``artifacts_dir``."""
    graph_dir = Path(graph_dir)
    artifacts_dir = Path(artifacts_dir)
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    copied: dict[str, Path] = {}
    for name in ARTIFACT_FILES:
        src = graph_dir / name
        if src.exists():
            dst = artifacts_dir / name
            shutil.copy2(src, dst)
            copied[name] = dst
    return copied


def run_graphify(
    source: Path | str,
    out_dir: Path | str,
    artifacts_dir: Path | str,
    *,
    backend: str = "gemini",
    force: bool = False,
    runner: Callable[..., Any] = subprocess.run,
) -> dict[str, Path]:
    """Run graphify (unless cached) and copy the artifacts; returns copied paths."""
    out_dir = Path(out_dir)
    graph_dir = out_graph_dir(out_dir)
    graph_json = graph_dir / "graph.json"
    report = graph_dir / "GRAPH_REPORT.md"
    if force or not graph_json.exists():
        out_dir.mkdir(parents=True, exist_ok=True)
        runner(extract_cmd(Path(source), out_dir, backend), capture_output=True, text=True)
    if force or not report.exists():
        runner(cluster_cmd(out_dir), capture_output=True, text=True)
    if not graph_json.exists():
        raise FileNotFoundError(f"graphify produced no graph.json at {graph_json}")
    return copy_artifacts(graph_dir, artifacts_dir)
