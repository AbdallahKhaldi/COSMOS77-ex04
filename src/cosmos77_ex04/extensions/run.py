"""Orchestrator for the original extensions (C9) — wires all four together.

Loads the real ``artifacts/graph.json`` once, then runs: the explicit suspect
ranking (-> obsidian/suspects.md), the dynamic hot.md (-> obsidian/hot.md), the
orphan finder (-> reports/ORPHANS.md), and the change-impact report (->
reports/IMPACT.md). The git runner is injected so tests stay offline (rule 6).
"""

from __future__ import annotations

import subprocess
from collections.abc import Callable
from pathlib import Path

from cosmos77_ex04.extensions.centrality_rank import rank_suspects_scored, write_suspects_md
from cosmos77_ex04.extensions.dynamic_hot import changed_files_from_git, rebuild_hot
from cosmos77_ex04.extensions.impact_report import write_impact_md
from cosmos77_ex04.extensions.orphans import find_orphans, write_orphans_md
from cosmos77_ex04.graphify.model import GraphModel


def _impact_label(model: GraphModel, config: dict) -> str:
    """The most central node — 'what breaks if we change the God Node' (the real blast radius)."""
    gods = model.god_nodes(1)
    return model.label_of(gods[0][0]) if gods else ""


def run_extensions(
    config: dict, repo_root: Path | str, runner: Callable[..., object] = subprocess.run
) -> dict:
    """Run all four extensions, writing into ``obsidian/`` and ``reports/``.

    Returns the output paths plus a couple of head-line stats (orphan count, top
    suspect) so the caller can report without re-reading the files.
    """
    root = Path(repo_root)
    paths = config.get("paths") or {}
    obsidian = root / paths.get("obsidian_dir", "obsidian")
    reports = root / paths.get("reports_dir", "reports")
    artifacts = root / paths.get("artifacts_dir", "artifacts")
    model = GraphModel.from_json(artifacts / "graph.json")

    target = config.get("target") or {}
    fix = config.get("fix") or {}
    failing_test = target.get("failing_test", "")

    ranking = rank_suspects_scored(model, failing_test)
    suspects = write_suspects_md(ranking, obsidian / "suspects.md")

    workdir = root / target.get("workdir", "data/target") / target.get("project", "")
    changed = changed_files_from_git(workdir, runner=runner)
    if not changed and fix.get("file"):
        changed = [fix["file"]]
    hot = rebuild_hot(model, changed, obsidian / "hot.md")

    orphans = write_orphans_md(model, reports / "ORPHANS.md")
    impact = write_impact_md(model, _impact_label(model, config), reports / "IMPACT.md")

    return {
        "suspects": suspects,
        "hot": hot,
        "orphans": orphans,
        "impact": impact,
        "orphan_count": len(find_orphans(model)),
        "top_suspect": ranking[0]["label"] if ranking else "",
    }
