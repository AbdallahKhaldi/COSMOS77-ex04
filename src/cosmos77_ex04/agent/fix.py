"""Apply the diagnosed fix and VERIFY the failing test goes FAIL→PASS (C6, C7).

The fix is recorded in config (file + search → replace) — the exact change the
graph-guided agent diagnosed. We restore the buggy state, run the test (must
FAIL), apply the fix, run again (must PASS), and capture the unified diff. The
guard refuses to claim success unless the transition is genuine FAIL→PASS — no
fabricated wins (the honesty rule).
"""

from __future__ import annotations

import difflib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cosmos77_ex04.agent.fix_report import write_fix_artifacts
from cosmos77_ex04.target.factory import harness_from_config


class FixNotVerifiedError(RuntimeError):
    """Raised when the (re)run does not demonstrate a real FAIL→PASS transition."""


@dataclass
class FixResult:
    """The applied fix + the before/after test verdicts (the C6 evidence)."""

    file: str
    diff: str
    before_passed: bool
    after_passed: bool
    applied: bool


def _unified_diff(before: str, after: str, name: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=f"a/{name}",
            tofile=f"b/{name}",
        )
    )


def verify_fail_to_pass(
    harness: Any, file_path: Path, search: str, replace: str, name: str
) -> FixResult:
    """Restore buggy → run (FAIL) → apply fix → run (PASS); raise unless genuine."""
    path = Path(file_path)
    text = path.read_text(encoding="utf-8")
    if replace in text and search not in text:  # idempotent: undo a prior fix first
        path.write_text(text.replace(replace, search, 1), encoding="utf-8")
    before_text = path.read_text(encoding="utf-8")
    before = harness.run_test()
    after_text = before_text.replace(search, replace, 1)
    applied = after_text != before_text
    path.write_text(after_text, encoding="utf-8")
    after = harness.run_test()
    result = FixResult(
        name, _unified_diff(before_text, after_text, name), before.passed, after.passed, applied
    )
    if before.passed or not after.passed:
        raise FixNotVerifiedError(
            f"expected FAIL→PASS, got before_passed={before.passed}, after_passed={after.passed}"
        )
    return result


def run_fix(config: Any, repo_root: Path) -> dict[str, Any]:
    """Apply + verify the fix, then write the before/after knowledge deliverables."""
    target = config.target()
    fix = config.get("fix", default={})
    project = target.get("project", "tqdm")
    file_path = repo_root / target.get("workdir", "data/target") / project / fix["file"]
    harness = harness_from_config(config, repo_root)
    result = verify_fail_to_pass(harness, file_path, fix["search"], fix["replace"], fix["file"])
    paths = config.paths()
    write_fix_artifacts(
        result,
        target.get("failing_test", ""),
        repo_root / paths.get("obsidian_dir", "obsidian"),
        repo_root / paths.get("reports_dir", "reports"),
    )
    return {
        "file": result.file,
        "before_passed": result.before_passed,
        "after_passed": result.after_passed,
        "applied": result.applied,
    }
