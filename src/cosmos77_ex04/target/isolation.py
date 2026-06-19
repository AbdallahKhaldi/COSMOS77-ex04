"""Provision an isolated Python toolchain for the BugsInPy target (C13).

`tqdm` bug 1 pins Python 3.6.9, which is unobtainable on Apple Silicon; 3.8.x
satisfies tqdm's ``setup.py`` (``python_requires='>=2.6'``). We install it via
``uv`` and expose a **pyshim** so the framework's hardcoded ``python``/``python3``
resolve to it — the TARGET's own toolchain, kept entirely separate from our
``uv``-managed project code (CLAUDE.md rule 5). Every shell-out is injectable so
unit tests mock it (rule 6).
"""

from __future__ import annotations

import os
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

_Runner = Callable[..., Any]


def ensure_python(version: str, *, runner: _Runner = subprocess.run) -> str:
    """Install ``version`` via uv and return the interpreter path (``""`` if not found)."""
    runner(["uv", "python", "install", version], capture_output=True, text=True)
    found = runner(["uv", "python", "find", version], capture_output=True, text=True)
    return (getattr(found, "stdout", "") or "").strip()


def ensure_pyshim(shim_dir: Path | str, python_path: str | Path) -> Path:
    """Create a shim dir where ``python`` and ``python3`` point at ``python_path``."""
    shim = Path(shim_dir)
    shim.mkdir(parents=True, exist_ok=True)
    for name in ("python", "python3"):
        link = shim / name
        if link.exists() or link.is_symlink():
            link.unlink()
        link.symlink_to(python_path)
    return shim


def path_env(extra_dirs: list[Path], base_env: dict[str, str] | None = None) -> dict[str, str]:
    """Return an environment with ``extra_dirs`` prepended to ``PATH``."""
    env = dict(base_env if base_env is not None else os.environ)
    prefix = os.pathsep.join(str(d) for d in extra_dirs)
    env["PATH"] = prefix + os.pathsep + env.get("PATH", "")
    return env
