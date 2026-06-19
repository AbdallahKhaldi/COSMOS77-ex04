"""Tests for the pure BugsInPy command builders (rule 6 — no execution)."""

from __future__ import annotations

from pathlib import Path

from cosmos77_ex04.target import bugsinpy_cli as cli


def test_checkout_cmd_flags():
    assert cli.checkout_cmd("tqdm", 1, 0, Path("/w")) == [
        "bugsinpy-checkout",
        "-p",
        "tqdm",
        "-v",
        "0",
        "-i",
        "1",
        "-w",
        "/w",
    ]


def test_simple_cmds():
    assert cli.compile_cmd() == ["bugsinpy-compile"]
    assert cli.test_cmd() == ["bugsinpy-test"]
    assert cli.info_cmd("tqdm", 2) == ["bugsinpy-info", "-p", "tqdm", "-i", "2"]
    assert cli.clone_cmd(Path("/d"))[:3] == ["git", "clone", "--depth"]


def test_paths():
    assert cli.framework_bin(Path("/b")) == Path("/b/framework/bin")
    assert cli.project_dir(Path("/w"), "tqdm") == Path("/w/tqdm")


def test_env_with_bin_prepends_path():
    env = cli.env_with_bin(Path("/b"), {"PATH": "/usr/bin"})
    assert env["PATH"].startswith(str(Path("/b/framework/bin")))
    assert env["PATH"].endswith("/usr/bin")
