"""Tests for the isolated-Python provisioning helpers (rule 6 — uv mocked)."""

from __future__ import annotations

import os
from pathlib import Path
from types import SimpleNamespace

from cosmos77_ex04.target import isolation


def test_ensure_python_installs_and_finds():
    calls = []

    def runner(cmd, **kwargs):
        calls.append(cmd)
        if cmd[:3] == ["uv", "python", "find"]:
            return SimpleNamespace(stdout="/path/to/py\n", returncode=0)
        return SimpleNamespace(stdout="", returncode=0)

    path = isolation.ensure_python("3.8.20", runner=runner)
    assert path == "/path/to/py"
    assert ["uv", "python", "install", "3.8.20"] in calls


def test_ensure_pyshim_creates_and_is_idempotent(tmp_path):
    target = tmp_path / "real_python"
    target.write_text("#!", encoding="utf-8")
    shim = isolation.ensure_pyshim(tmp_path / "shim", target)
    assert (shim / "python").is_symlink()
    assert (shim / "python3").is_symlink()
    isolation.ensure_pyshim(tmp_path / "shim", target)  # re-run replaces, no error
    assert (shim / "python").resolve() == target


def test_path_env_prepends_dirs():
    env = isolation.path_env([Path("/a"), Path("/b")], {"PATH": "/usr/bin"})
    assert env["PATH"].split(os.pathsep)[:2] == ["/a", "/b"]
    assert env["PATH"].endswith("/usr/bin")
