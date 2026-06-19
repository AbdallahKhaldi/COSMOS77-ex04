"""Tests for BugsInPy bug discovery + metadata reading (rule 6 — fixture dirs)."""

from __future__ import annotations

from pathlib import Path

from cosmos77_ex04.target import info


def _make_bug(root: Path, project: str, bug_id: int, info_text: str) -> Path:
    bug_dir = root / "projects" / project / "bugs" / str(bug_id)
    bug_dir.mkdir(parents=True)
    (bug_dir / "bug.info").write_text(info_text, encoding="utf-8")
    return bug_dir


def test_list_bugs_sorted_numeric(tmp_path):
    _make_bug(tmp_path, "tqdm", 2, "")
    _make_bug(tmp_path, "tqdm", 1, "")
    (tmp_path / "projects" / "tqdm" / "bugs" / "notanum").mkdir()
    assert info.list_bugs(tmp_path, "tqdm") == [1, 2]


def test_list_bugs_missing_project(tmp_path):
    assert info.list_bugs(tmp_path, "nope") == []


def test_read_bug_info_parses_fields(tmp_path):
    _make_bug(
        tmp_path,
        "tqdm",
        1,
        'python_version="3.6.9"\nbuggy_commit_id="abc"\n'
        'fixed_commit_id="def"\ntest_file="tqdm/tests/x.py"\n',
    )
    bi = info.read_bug_info(tmp_path, "tqdm", 1)
    assert bi.python_version == "3.6.9"
    assert (bi.buggy_commit, bi.fixed_commit) == ("abc", "def")
    assert bi.test_file == "tqdm/tests/x.py"


def test_read_bug_info_missing_defaults_empty(tmp_path):
    assert info.read_bug_info(tmp_path, "tqdm", 99).python_version == ""


def test_read_test_command_parses_pytest_line(tmp_path):
    project_dir = tmp_path / "tqdm"
    project_dir.mkdir()
    (project_dir / "bugsinpy_run_test.sh").write_text(
        "#!/bin/bash\npython3 -m pytest tqdm/tests/tests_contrib.py::test_enumerate\n",
        encoding="utf-8",
    )
    assert info.read_test_command(project_dir) == ["tqdm/tests/tests_contrib.py::test_enumerate"]


def test_read_test_command_missing_returns_empty(tmp_path):
    assert info.read_test_command(tmp_path) == []
