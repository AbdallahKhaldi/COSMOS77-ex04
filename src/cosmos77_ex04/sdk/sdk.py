"""The single business-logic entry point (CLAUDE.md rule 2).

The CLI, the LangGraph agent, the token harness, and the tests all go through
``class SDK`` — one audited surface. Each pipeline stage is one method; stages
land in their phase (a ``NotImplementedError`` until then). The Gatekeeper token
ledger is created once and shared so the comparison rests on ONE measured ledger.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from cosmos77_ex04.graphify.fallback import write_fallback
from cosmos77_ex04.graphify.model import GraphModel
from cosmos77_ex04.graphify.report import parse_report
from cosmos77_ex04.graphify.run import copy_artifacts, out_graph_dir
from cosmos77_ex04.graphify.run import run_graphify as run_graphify_cli
from cosmos77_ex04.reveng.extract import extract_diagrams as extract_diagrams_fn
from cosmos77_ex04.shared.config import Config
from cosmos77_ex04.shared.gatekeeper import Gatekeeper
from cosmos77_ex04.target.checkout import BugsInPyHarness, TargetInfo
from cosmos77_ex04.target.info import list_bugs
from cosmos77_ex04.vault.build import build_vault as build_vault_fn


class SDK:
    """All business logic for the reverse-engineering + debugging pipeline."""

    def __init__(self, config: Config | None = None, gatekeeper: Gatekeeper | None = None) -> None:
        self.config = config or Config()
        self.gatekeeper = gatekeeper or Gatekeeper()

    @property
    def repo_root(self) -> Path:
        """The repository root (the parent of the ``config/`` directory)."""
        return self.config.config_dir.parent

    def prepare_target(self) -> TargetInfo:
        """Check out one BugsInPy bug into an isolated env and run its failing test."""
        target = self.config.target()
        project = target.get("project", "tqdm")
        workdir = self.repo_root / target.get("workdir", "data/target")
        bugsinpy_dir = self.repo_root / "data" / "BugsInPy"
        harness = BugsInPyHarness(
            project,
            target.get("bug_id") or 1,
            workdir,
            bugsinpy_dir,
            python_version=target.get("python_version", "3.8.20"),
            shim_dir=self.repo_root / "data" / "pyshim",
        )
        harness.ensure_clone()
        if target.get("bug_id") is None:
            bugs = list_bugs(bugsinpy_dir, project)
            if bugs:
                harness.bug_id = bugs[0]
        return harness.prepare()

    def run_graphify(self, *, force: bool = False) -> dict[str, Any]:
        """Run Graphify on the target source (DIY fallback) and summarise the graph."""
        target = self.config.target()
        project = target.get("project", "tqdm")
        project_dir = self.repo_root / target.get("workdir", "data/target") / project
        source = project_dir / target.get("package_subdir", project)
        work_dir = self.repo_root / "data" / "graphify"
        artifacts_dir = self.repo_root / self.config.paths().get("artifacts_dir", "artifacts")
        try:
            run_graphify_cli(
                source, work_dir, artifacts_dir, backend=self.config.active_provider(), force=force
            )
        except (OSError, subprocess.SubprocessError):
            write_fallback(source, out_graph_dir(work_dir) / "graph.json")
            copy_artifacts(out_graph_dir(work_dir), artifacts_dir)
        model = GraphModel.from_json(artifacts_dir / "graph.json")
        return {
            "nodes": len(model.nodes),
            "edges": len(model.edges),
            "communities": len(model.communities()),
            "tiers": model.edges_by_tier(),
            "god_nodes": [model.label_of(nid) for nid, _ in model.god_nodes(5)],
        }

    def build_vault(self) -> dict[str, Any]:
        """Generate the Obsidian knowledge vault (index.md / hot.md / pages) from the graph."""
        artifacts_dir = self.repo_root / self.config.paths().get("artifacts_dir", "artifacts")
        obsidian_dir = self.repo_root / self.config.paths().get("obsidian_dir", "obsidian")
        model = GraphModel.from_json(artifacts_dir / "graph.json")
        report = parse_report(artifacts_dir / "GRAPH_REPORT.md")
        failing_test = self.config.target().get("failing_test", "")
        return build_vault_fn(model, report, obsidian_dir, failing_test=failing_test)

    def extract_diagrams(self) -> dict[str, Any]:
        """Extract the architectural block diagram + OOP schema + God-Node report."""
        artifacts_dir = self.repo_root / self.config.paths().get("artifacts_dir", "artifacts")
        reports_dir = self.repo_root / self.config.paths().get("reports_dir", "reports")
        target = self.config.target()
        project = target.get("project", "tqdm")
        source = (
            self.repo_root
            / target.get("workdir", "data/target")
            / project
            / target.get("package_subdir", project)
        )
        model = GraphModel.from_json(artifacts_dir / "graph.json")
        return extract_diagrams_fn(model, source, artifacts_dir, reports_dir)

    def run_agent(self) -> Any:
        """Run the graph-guided LangGraph debug agent (Phase 6)."""
        raise NotImplementedError("run_agent lands in Phase 6")

    def apply_fix(self) -> Any:
        """Apply + verify the fix, FAIL→PASS (Phase 7)."""
        raise NotImplementedError("apply_fix lands in Phase 7")

    def compare_tokens(self) -> Any:
        """Run the naive baseline vs graph-guided token comparison (Phase 8)."""
        raise NotImplementedError("compare_tokens lands in Phase 8")

    def run_extensions(self) -> Any:
        """Run the original extensions (Phase 9)."""
        raise NotImplementedError("run_extensions lands in Phase 9")

    def spec_sheet(self) -> dict[str, Any]:
        """Return the measured token ledger (the Spec Sheet aggregate, C15)."""
        return self.gatekeeper.ledger()
