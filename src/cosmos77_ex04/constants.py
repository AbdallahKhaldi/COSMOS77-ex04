"""Project-wide structural constants (not tunable config — see CLAUDE.md rule 4).

These are fixed enumerations the SDK, agent, and CLI share. Tunable values
(target repo/bug, model, provider, paths, call/step caps) live in
``config/*.json`` and ``.env`` and are read via the Config loader (Phase 2).
"""

from __future__ import annotations

#: Default text encoding for all file I/O across the project.
DEFAULT_ENCODING: str = "utf-8"

#: The importable package name (mirrors pyproject ``name``, underscored).
PACKAGE_NAME: str = "cosmos77_ex04"

#: The version string — kept in lockstep with pyproject and every config file.
PROJECT_VERSION: str = "1.00"

#: The ``cosmos77-rev`` pipeline stages, in run order (wired to the SDK per phase).
PIPELINE_STAGES: tuple[str, ...] = (
    "prepare-target",
    "graphify",
    "vault",
    "diagrams",
    "agent",
    "fix",
    "compare",
    "extensions",
    "run",
)
