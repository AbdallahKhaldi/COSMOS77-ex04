"""Discover BugsInPy bugs and read a bug's metadata (no checkout, no network).

Lets us pick the SMALLEST/cleanest bug for a project and record its buggy/fixed
commits, required Python, and failing test — all by reading the cloned framework
tree, so it stays fully mockable with a fixture directory.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class BugInfo:
    """One BugsInPy bug's metadata, parsed from ``bugs/<id>/bug.info``."""

    project: str
    bug_id: int
    python_version: str = ""
    buggy_commit: str = ""
    fixed_commit: str = ""
    test_file: str = ""


def bugs_root(bugsinpy_dir: Path, project: str) -> Path:
    """The ``projects/<project>/bugs`` directory inside the framework clone."""
    return Path(bugsinpy_dir) / "projects" / project / "bugs"


def list_bugs(bugsinpy_dir: Path, project: str) -> list[int]:
    """Return the sorted numeric bug ids available for ``project`` (``[]`` if none)."""
    root = bugs_root(bugsinpy_dir, project)
    if not root.exists():
        return []
    ids = [int(p.name) for p in root.iterdir() if p.is_dir() and p.name.isdigit()]
    return sorted(ids)


def _parse_kv(text: str) -> dict[str, str]:
    """Parse BugsInPy ``key="value"`` lines into a dict."""
    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or "=" not in line:
            continue
        key, _, val = line.partition("=")
        out[key.strip()] = val.strip().strip('"')
    return out


def read_bug_info(bugsinpy_dir: Path, project: str, bug_id: int) -> BugInfo:
    """Read ``bug.info`` for one bug (missing keys default to empty strings)."""
    info_path = bugs_root(bugsinpy_dir, project) / str(bug_id) / "bug.info"
    data = _parse_kv(info_path.read_text(encoding="utf-8")) if info_path.exists() else {}
    return BugInfo(
        project=project,
        bug_id=bug_id,
        python_version=data.get("python_version", ""),
        buggy_commit=data.get("buggy_commit_id", ""),
        fixed_commit=data.get("fixed_commit_id", ""),
        test_file=data.get("test_file", ""),
    )


def read_test_command(project_dir: Path | str) -> list[str]:
    """Extract the pytest target args from the checked-out ``bugsinpy_run_test.sh``.

    `bugsinpy-test` itself is unusable on macOS (bash-3.2 vs the script's bash-4
    ``&>>``), so we read the single failing-test command and run it in the per-bug
    venv ourselves. Returns e.g. ``["tqdm/tests/tests_contrib.py::test_enumerate"]``.
    """
    script = Path(project_dir) / "bugsinpy_run_test.sh"
    if not script.exists():
        return []
    for raw in script.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if "pytest" in line:
            _, _, rest = line.partition("pytest")
            return rest.split()
    return []
