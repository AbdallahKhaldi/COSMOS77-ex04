"""The single business-logic entry point (CLAUDE.md rule 2).

The CLI, the LangGraph agent, the token harness, and the tests all go through
``class SDK`` — one audited surface. Each pipeline stage is one method; stages
land in their phase (a ``NotImplementedError`` until then). The Gatekeeper token
ledger is created once and shared so the comparison rests on ONE measured ledger.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cosmos77_ex04.shared.config import Config
from cosmos77_ex04.shared.gatekeeper import Gatekeeper
from cosmos77_ex04.target.checkout import BugsInPyHarness, TargetInfo
from cosmos77_ex04.target.info import list_bugs


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

    def run_graphify(self) -> Any:
        """Run Graphify + parse graph.json (Phase 3)."""
        raise NotImplementedError("run_graphify lands in Phase 3")

    def build_vault(self) -> Any:
        """Generate the Obsidian vault (Phase 4)."""
        raise NotImplementedError("build_vault lands in Phase 4")

    def extract_diagrams(self) -> Any:
        """Extract the block diagram + OOP schema (Phase 5)."""
        raise NotImplementedError("extract_diagrams lands in Phase 5")

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
