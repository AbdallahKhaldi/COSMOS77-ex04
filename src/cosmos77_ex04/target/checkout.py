"""BugsInPy checkout/compile/test harness in an ISOLATED env (C6, C13).

Drives the framework CLI via an injectable ``runner`` (defaults to
``subprocess.run``) so unit tests mock every external call (CLAUDE.md rule 6).
The target builds and tests in BugsInPy's own per-bug virtualenv with an
isolated Python (see :mod:`isolation`) — entirely separate from our ``uv``
project (rule 5). The bug's failing test is run directly in that venv because
``bugsinpy-test`` is broken on macOS bash-3.2.
"""

from __future__ import annotations

import shutil
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cosmos77_ex04.constants import BUGGY_VERSION
from cosmos77_ex04.target import bugsinpy_cli as cli
from cosmos77_ex04.target import isolation
from cosmos77_ex04.target.info import BugInfo, read_bug_info, read_test_command


@dataclass
class BugTestResult:
    """The outcome of one bug-test run."""

    passed: bool
    returncode: int
    output: str


@dataclass
class TargetInfo:
    """Everything the rest of the pipeline needs about the checked-out target."""

    project: str
    bug_id: int
    workdir: Path
    project_dir: Path
    bug: BugInfo
    test_result: BugTestResult


class BugsInPyHarness:
    """Checks out a single buggy version and runs its failing test, isolated."""

    def __init__(
        self,
        project: str,
        bug_id: int,
        workdir: Path | str,
        bugsinpy_dir: Path | str,
        *,
        python_version: str = "3.8.20",
        shim_dir: Path | str | None = None,
        runner: Callable[..., Any] = subprocess.run,
    ) -> None:
        self.project = project
        self.bug_id = int(bug_id)
        self.workdir = Path(workdir)
        self.bugsinpy_dir = Path(bugsinpy_dir)
        self.python_version = python_version
        self.shim_dir = Path(shim_dir) if shim_dir else self.workdir.parent / "pyshim"
        self._run = runner
        self._env: dict[str, str] | None = None

    @property
    def project_dir(self) -> Path:
        """The checked-out project directory (``workdir/project``)."""
        return cli.project_dir(self.workdir, self.project)

    @property
    def venv_python(self) -> Path:
        """The per-bug virtualenv's interpreter (created by ``bugsinpy-compile``)."""
        return self.project_dir / "env" / "bin" / "python"

    def env(self) -> dict[str, str]:
        """Build (once) the PATH env with the pyshim + framework/bin prepended."""
        if self._env is None:
            python_path = isolation.ensure_python(self.python_version, runner=self._run)
            if python_path:
                isolation.ensure_pyshim(self.shim_dir, python_path)
            self._env = isolation.path_env([self.shim_dir, cli.framework_bin(self.bugsinpy_dir)])
        return self._env

    def _exec(self, cmd: list[str], cwd: Path | None = None) -> Any:
        return self._run(
            cmd,
            cwd=str(cwd) if cwd is not None else None,
            env=self.env(),
            capture_output=True,
            text=True,
        )

    def ensure_clone(self) -> Path:
        """Clone the BugsInPy framework once (cached); a no-op if already present."""
        if not self.bugsinpy_dir.exists():
            self._run(cli.clone_cmd(self.bugsinpy_dir), capture_output=True, text=True)
        return self.bugsinpy_dir

    def checkout(self, version: int = BUGGY_VERSION) -> Any:
        """Check out ``version`` (0 = buggy) of the bug into the workdir."""
        self.workdir.mkdir(parents=True, exist_ok=True)
        return self._exec(cli.checkout_cmd(self.project, self.bug_id, version, self.workdir))

    def compile(self) -> Any:
        """Build the per-bug isolated venv and install the target's deps."""
        return self._exec(cli.compile_cmd(), cwd=self.project_dir)

    def _clear_pycache(self) -> None:
        """Delete ``__pycache__`` so a reverted/applied source change isn't masked by stale .pyc."""
        for cache in self.project_dir.rglob("__pycache__"):
            shutil.rmtree(cache, ignore_errors=True)

    def run_test(self) -> BugTestResult:
        """Run the bug's failing test in the venv; ``passed`` is True only on exit 0."""
        self._clear_pycache()
        args = read_test_command(self.project_dir)
        proc = self._exec([str(self.venv_python), "-m", "pytest", *args], cwd=self.project_dir)
        output = (getattr(proc, "stdout", "") or "") + (getattr(proc, "stderr", "") or "")
        return BugTestResult(passed=proc.returncode == 0, returncode=proc.returncode, output=output)

    def prepare(self, *, reuse: bool = True) -> TargetInfo:
        """Full flow (idempotent): clone → checkout buggy → compile → run failing test."""
        self.ensure_clone()
        if not (reuse and (self.project_dir / "bugsinpy_run_test.sh").exists()):
            self.checkout(BUGGY_VERSION)
        if not (reuse and (self.project_dir / "bugsinpy_compile_flag").exists()):
            self.compile()
        result = self.run_test()
        bug = read_bug_info(self.bugsinpy_dir, self.project, self.bug_id)
        return TargetInfo(
            project=self.project,
            bug_id=self.bug_id,
            workdir=self.workdir,
            project_dir=self.project_dir,
            bug=bug,
            test_result=result,
        )
