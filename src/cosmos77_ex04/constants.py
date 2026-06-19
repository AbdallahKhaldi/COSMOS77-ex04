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

#: Evidence tiers for graph edges (the professor's vocabulary, C14). An edge is
#: ``extracted`` when the graph proves it (a literal call/import), ``inferred``
#: when reasoned from context, and ``ambiguous`` when uncertain.
EVIDENCE_TIERS: tuple[str, ...] = ("extracted", "inferred", "ambiguous")

#: The kinds of node Graphify emits (and our DIY fallback mirrors).
NODE_KINDS: tuple[str, ...] = ("module", "class", "function", "method")

#: Bug-version selectors for the BugsInPy harness (0 = buggy, 1 = fixed).
BUGGY_VERSION: int = 0
FIXED_VERSION: int = 1
