"""Tests for the fix application + FAIL→PASS verification guard (C6)."""

from __future__ import annotations

import pytest

from cosmos77_ex04.agent.fix import FixNotVerifiedError, verify_fail_to_pass
from cosmos77_ex04.target.checkout import BugTestResult


class FakeHarness:
    """Returns the queued verdicts for successive run_test() calls."""

    def __init__(self, verdicts):
        self.verdicts = list(verdicts)
        self.calls = 0

    def run_test(self):
        passed = self.verdicts[self.calls]
        self.calls += 1
        return BugTestResult(passed=passed, returncode=0 if passed else 1, output="")


def test_verify_fail_to_pass_applies_and_diffs(tmp_path):
    target = tmp_path / "mod.py"
    target.write_text("x = 1\nreturn foo(a, b)\ny = 2\n", encoding="utf-8")
    result = verify_fail_to_pass(
        FakeHarness([False, True]), target, "return foo(a, b)", "return foo(b, a)", "mod.py"
    )
    assert result.before_passed is False
    assert result.after_passed is True
    assert result.applied is True
    assert "return foo(b, a)" in target.read_text(encoding="utf-8")
    assert "-return foo(a, b)" in result.diff
    assert "+return foo(b, a)" in result.diff


def test_verify_raises_when_after_still_fails(tmp_path):
    target = tmp_path / "mod.py"
    target.write_text("return foo(a, b)\n", encoding="utf-8")
    with pytest.raises(FixNotVerifiedError):
        verify_fail_to_pass(
            FakeHarness([False, False]), target, "return foo(a, b)", "return foo(b, a)", "mod.py"
        )


def test_verify_raises_when_before_already_passes(tmp_path):
    target = tmp_path / "mod.py"
    target.write_text("return foo(a, b)\n", encoding="utf-8")
    with pytest.raises(FixNotVerifiedError):
        verify_fail_to_pass(
            FakeHarness([True, True]), target, "return foo(a, b)", "return foo(b, a)", "mod.py"
        )


def test_verify_reverts_a_prior_fix(tmp_path):
    target = tmp_path / "mod.py"
    target.write_text("return foo(b, a)\n", encoding="utf-8")  # already fixed
    harness = FakeHarness([False, True])
    result = verify_fail_to_pass(harness, target, "return foo(a, b)", "return foo(b, a)", "mod.py")
    assert result.after_passed is True
    assert harness.calls == 2  # restored buggy, ran FAIL, re-applied, ran PASS
