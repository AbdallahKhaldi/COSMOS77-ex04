"""The NAIVE raw-file baseline arm of the token comparison (C8).

This arm deliberately ignores the graph and the Obsidian vault: it reads EVERY
``.py`` file under the source root and stuffs them all into one prompt — the
wasteful "load everything" behaviour that invites Context Rot and Lost in the
Middle. Its single metered LLM call routes through :func:`invoke_diagnose`, so
its token cost is measured by the SAME Gatekeeper ledger as the guided agent —
the only honest way to compare the two arms on the same bug and same model.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cosmos77_ex04.agent.llm import invoke_diagnose
from cosmos77_ex04.shared.gatekeeper import Gatekeeper


def collect_source_files(source_root: Path | str, max_files: int = 40) -> dict[str, str]:
    """Read EVERY ``.py`` file under ``source_root`` (the naive, unguided sweep).

    Returns a mapping of POSIX relative path → file text, capped at ``max_files``
    so the prompt stays bounded but still demonstrates the raw-file cost.
    """
    root = Path(source_root)
    files: dict[str, str] = {}
    for path in sorted(root.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        rel = path.relative_to(root).as_posix()
        files[rel] = path.read_text(encoding="utf-8", errors="replace")
        if len(files) >= max_files:
            break
    return files


def baseline_prompt(failing_test: str, test_output: str, files: dict[str, str]) -> str:
    """Build the naive prompt: the failing test, the traceback, and ALL source.

    Every file is concatenated verbatim — low signal-to-noise on purpose, so the
    measured token cost reflects raw-file reading rather than guided retrieval.
    """
    blocks = [f"### {rel}\n```python\n{text}\n```" for rel, text in files.items()]
    body = "\n\n".join(blocks)
    return (
        "You are debugging a Python project with NO knowledge graph to guide you.\n"
        f"Failing test: {failing_test}\n\n"
        f"Test output / traceback:\n{test_output or '(none captured)'}\n\n"
        f"Below is the ENTIRE source ({len(files)} file(s)). Identify the ROOT CAUSE "
        "and name the FILE and FAULTY CODE.\n\n"
        f"{body}\n"
    )


def run_baseline(
    llm: Any,
    gatekeeper: Gatekeeper,
    source_root: Path | str,
    failing_test: str,
    test_output: str = "",
    *,
    max_files: int = 40,
) -> dict[str, Any]:
    """Run the naive baseline: read every file, one metered LLM call, return ledger.

    ``files_read`` lists ALL files swept (the whole-repo cost), in contrast to the
    guided agent's handful of targeted reads — the comparison's central evidence.
    """
    files = collect_source_files(source_root, max_files=max_files)
    prompt = baseline_prompt(failing_test, test_output, files)
    diagnosis = invoke_diagnose(llm, prompt, gatekeeper, label="baseline")
    return {
        "diagnosis": diagnosis,
        "files_read": list(files.keys()),
        "iterations": 1,
        "tokens": gatekeeper.ledger(),
    }
