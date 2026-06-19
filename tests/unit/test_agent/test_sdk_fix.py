"""SDK-level test for apply_fix → FAIL→PASS + knowledge artifacts (C6, C7)."""

from __future__ import annotations

from cosmos77_ex04.agent import fix as fixmod
from cosmos77_ex04.sdk.sdk import SDK
from cosmos77_ex04.target.checkout import BugTestResult


class _FakeHarness:
    def __init__(self):
        self.calls = 0

    def run_test(self):
        passed = self.calls > 0  # first call FAIL, second PASS
        self.calls += 1
        return BugTestResult(passed=passed, returncode=0 if passed else 1, output="")


def test_apply_fix_verifies_and_writes_artifacts(config, monkeypatch):
    repo_root = config.config_dir.parent
    # config fix block points at pkg/mod.py with foo(a, b) -> foo(b, a)
    target_file = repo_root / "data" / "target" / "tqdm" / "pkg" / "mod.py"
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text("def g():\n    return foo(a, b)\n", encoding="utf-8")
    (repo_root / "reports").mkdir(parents=True, exist_ok=True)
    (repo_root / "reports" / "BUG_ANALYSIS.md").write_text("# Bug Analysis\n", encoding="utf-8")

    monkeypatch.setattr(fixmod, "harness_from_config", lambda c, r: _FakeHarness())
    out = SDK(config=config).apply_fix()

    assert out["before_passed"] is False
    assert out["after_passed"] is True
    assert "return foo(b, a)" in target_file.read_text(encoding="utf-8")
    assert (repo_root / "obsidian" / "investigation.md").exists()
    assert (repo_root / "obsidian" / "fix-process.md").exists()
