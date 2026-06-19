"""Build a BugsInPyHarness from config (shared by the SDK and the fix step)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cosmos77_ex04.target.checkout import BugsInPyHarness


def harness_from_config(config: Any, repo_root: Path) -> BugsInPyHarness:
    """Construct the harness for the configured target (no checkout performed)."""
    target = config.target()
    project = target.get("project", "tqdm")
    return BugsInPyHarness(
        project,
        target.get("bug_id") or 1,
        repo_root / target.get("workdir", "data/target"),
        repo_root / "data" / "BugsInPy",
        python_version=target.get("python_version", "3.8.20"),
        shim_dir=repo_root / "data" / "pyshim",
    )
