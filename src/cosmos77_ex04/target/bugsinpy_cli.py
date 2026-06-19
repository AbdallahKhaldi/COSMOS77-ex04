"""Pure command builders for the BugsInPy framework CLI (no execution).

Kept side-effect-free so the exact command lines are unit-testable without ever
touching git/subprocess (CLAUDE.md rule 6). The orchestration that actually runs
these lives in :mod:`cosmos77_ex04.target.checkout`.
"""

from __future__ import annotations

import os
from pathlib import Path

#: The upstream BugsInPy framework repository (cloned once, cached under data/).
CLONE_URL = "https://github.com/soarsmu/BugsInPy.git"


def clone_cmd(dest: Path) -> list[str]:
    """A shallow clone of the BugsInPy framework into ``dest``."""
    return ["git", "clone", "--depth", "1", CLONE_URL, str(dest)]


def checkout_cmd(project: str, bug_id: int, version: int, workdir: Path) -> list[str]:
    """``bugsinpy-checkout`` for one bug (version 0 = buggy, 1 = fixed)."""
    return [
        "bugsinpy-checkout",
        "-p",
        project,
        "-v",
        str(version),
        "-i",
        str(bug_id),
        "-w",
        str(workdir),
    ]


def compile_cmd() -> list[str]:
    """``bugsinpy-compile`` — builds the per-bug isolated venv + installs deps."""
    return ["bugsinpy-compile"]


def test_cmd() -> list[str]:
    """``bugsinpy-test`` — runs the bug-specific test (expected to FAIL on buggy)."""
    return ["bugsinpy-test"]


def info_cmd(project: str, bug_id: int) -> list[str]:
    """``bugsinpy-info`` — prints a bug's metadata."""
    return ["bugsinpy-info", "-p", project, "-i", str(bug_id)]


def framework_bin(bugsinpy_dir: Path) -> Path:
    """The ``framework/bin`` directory holding the ``bugsinpy-*`` executables."""
    return Path(bugsinpy_dir) / "framework" / "bin"


def env_with_bin(bugsinpy_dir: Path, base_env: dict[str, str] | None = None) -> dict[str, str]:
    """Return an env with the BugsInPy ``framework/bin`` prepended to ``PATH``."""
    env = dict(base_env if base_env is not None else os.environ)
    binp = str(framework_bin(bugsinpy_dir))
    env["PATH"] = binp + os.pathsep + env.get("PATH", "")
    return env


def project_dir(workdir: Path, project: str) -> Path:
    """The checked-out project directory inside ``workdir``."""
    return Path(workdir) / project
