"""Tests for the BugsInPy harness (rule 6 — subprocess fully mocked)."""

from __future__ import annotations

from types import SimpleNamespace

from cosmos77_ex04.target.checkout import BugsInPyHarness, BugTestResult, TargetInfo


def make_runner(returncode=1, stdout="FAILED", record=None):
    """A fake ``subprocess.run`` that answers uv-python probes and records cmds."""

    def runner(cmd, **kwargs):
        if record is not None:
            record.append((cmd, kwargs))
        if cmd[:3] == ["uv", "python", "find"]:
            return SimpleNamespace(stdout="/fake/python\n", stderr="", returncode=0)
        if cmd[:3] == ["uv", "python", "install"]:
            return SimpleNamespace(stdout="", stderr="", returncode=0)
        return SimpleNamespace(stdout=stdout, stderr="", returncode=returncode)

    return runner


def _harness(tmp_path, **kwargs):
    return BugsInPyHarness(
        "tqdm",
        1,
        tmp_path / "target",
        tmp_path / "BugsInPy",
        shim_dir=tmp_path / "shim",
        **kwargs,
    )


def test_checkout_builds_command(tmp_path):
    rec: list = []
    _harness(tmp_path, runner=make_runner(record=rec)).checkout(0)
    cmds = [c for c, _ in rec]
    assert [
        "bugsinpy-checkout",
        "-p",
        "tqdm",
        "-v",
        "0",
        "-i",
        "1",
        "-w",
        str(tmp_path / "target"),
    ] in cmds


def test_compile_builds_command(tmp_path):
    rec: list = []
    _harness(tmp_path, runner=make_runner(record=rec)).compile()
    assert ["bugsinpy-compile"] in [c for c, _ in rec]


def test_env_has_shim_then_framework_bin(tmp_path):
    env = _harness(tmp_path, runner=make_runner()).env()
    parts = env["PATH"].split(":")
    assert str(tmp_path / "shim") == parts[0]
    assert str(tmp_path / "BugsInPy" / "framework" / "bin") == parts[1]


def test_env_without_python_still_builds(tmp_path):
    def runner(cmd, **kwargs):
        return SimpleNamespace(stdout="", stderr="", returncode=0)

    env = _harness(tmp_path, runner=runner).env()
    assert "PATH" in env
    assert not (tmp_path / "shim" / "python").exists()


def test_run_test_reports_failure(tmp_path):
    project_dir = tmp_path / "target" / "tqdm"
    project_dir.mkdir(parents=True)
    (project_dir / "bugsinpy_run_test.sh").write_text(
        "python3 -m pytest tqdm/tests/x.py::t\n", encoding="utf-8"
    )
    rec: list = []
    result = _harness(tmp_path, runner=make_runner(1, "1 failed", rec)).run_test()
    assert isinstance(result, BugTestResult)
    assert result.passed is False
    assert result.returncode == 1
    pytest_cmds = [c for c, _ in rec if "-m" in c and "pytest" in c]
    assert pytest_cmds and pytest_cmds[0][-1] == "tqdm/tests/x.py::t"


def test_run_test_clears_stale_pycache(tmp_path):
    project_dir = tmp_path / "target" / "tqdm"
    cache = project_dir / "tqdm" / "__pycache__"
    cache.mkdir(parents=True)
    (cache / "contrib.pyc").write_text("stale", encoding="utf-8")
    (project_dir / "bugsinpy_run_test.sh").write_text("python3 -m pytest a::b\n", encoding="utf-8")
    _harness(tmp_path, runner=make_runner(1, "1 failed")).run_test()
    assert not cache.exists()  # cleared before the run so the .pyc can't mask source edits


def test_ensure_clone_skips_when_present(tmp_path):
    (tmp_path / "BugsInPy").mkdir()
    rec: list = []
    _harness(tmp_path, runner=make_runner(record=rec)).ensure_clone()
    assert not any(c[:2] == ["git", "clone"] for c, _ in rec)


def test_ensure_clone_clones_when_absent(tmp_path):
    rec: list = []
    _harness(tmp_path, runner=make_runner(record=rec)).ensure_clone()
    assert any(c[:2] == ["git", "clone"] for c, _ in rec)


def test_prepare_reuses_existing_checkout(tmp_path):
    bug_dir = tmp_path / "BugsInPy" / "projects" / "tqdm" / "bugs" / "1"
    bug_dir.mkdir(parents=True)
    (bug_dir / "bug.info").write_text('python_version="3.6.9"\n', encoding="utf-8")
    project_dir = tmp_path / "target" / "tqdm"
    project_dir.mkdir(parents=True)
    (project_dir / "bugsinpy_run_test.sh").write_text("python3 -m pytest a::b\n", encoding="utf-8")
    (project_dir / "bugsinpy_compile_flag").write_text("1", encoding="utf-8")
    rec: list = []
    info_obj = _harness(tmp_path, runner=make_runner(1, "1 failed", rec)).prepare()
    assert isinstance(info_obj, TargetInfo)
    assert info_obj.test_result.passed is False
    assert info_obj.bug.python_version == "3.6.9"
    cmds = [c for c, _ in rec]
    assert not any(c[:1] == ["bugsinpy-checkout"] for c in cmds)
    assert ["bugsinpy-compile"] not in cmds


def test_prepare_runs_checkout_and_compile_when_forced(tmp_path):
    bug_dir = tmp_path / "BugsInPy" / "projects" / "tqdm" / "bugs" / "1"
    bug_dir.mkdir(parents=True)
    (bug_dir / "bug.info").write_text("", encoding="utf-8")
    project_dir = tmp_path / "target" / "tqdm"
    project_dir.mkdir(parents=True)
    (project_dir / "bugsinpy_run_test.sh").write_text("python3 -m pytest a::b\n", encoding="utf-8")
    rec: list = []
    _harness(tmp_path, runner=make_runner(1, "x", rec)).prepare(reuse=False)
    cmds = [c for c, _ in rec]
    assert any(c[:1] == ["bugsinpy-checkout"] for c in cmds)
    assert ["bugsinpy-compile"] in cmds
