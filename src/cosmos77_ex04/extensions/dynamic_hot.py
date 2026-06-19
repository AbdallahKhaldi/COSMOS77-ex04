"""Original extension — a ``hot.md`` that tracks where the action is (C9).

The static vault freezes the bug-critical area at graph-build time. Here we make
it dynamic: read the working tree's changed files via ``git diff``, intersect
them with graph nodes, and regenerate ``obsidian/hot.md`` from those nodes plus
their 1-hop neighbourhood (the blast radius of the edit). If nothing changed we
fall back to the God Nodes so the hub is never empty. git is mocked in tests.
"""

from __future__ import annotations

import subprocess
from collections.abc import Callable
from pathlib import Path

from cosmos77_ex04.graphify.model import GraphModel


def changed_files_from_git(
    target_dir: Path | str, runner: Callable[..., subprocess.CompletedProcess] = subprocess.run
) -> list[str]:
    """Return the basenames git reports as changed (``git -C <dir> diff --name-only``).

    ``runner`` is injected so tests mock the subprocess — no live git in CI (rule 6).
    """
    result = runner(
        ["git", "-C", str(target_dir), "diff", "--name-only"],
        capture_output=True,
        text=True,
        check=False,
    )
    out = getattr(result, "stdout", "") or ""
    return [line.strip() for line in out.splitlines() if line.strip()]


def _nodes_for_files(model: GraphModel, changed_files: list[str]) -> list[str]:
    """Graph node ids whose source file matches any changed file (by basename)."""
    wanted = {Path(f).name for f in changed_files}
    return [
        nid for nid, node in model.nodes.items() if node.file and Path(node.file).name in wanted
    ]


def rebuild_hot(model: GraphModel, changed_files: list[str], out_path: Path | str) -> Path:
    """Regenerate ``obsidian/hot.md`` from changed nodes + their 1-hop neighbourhood.

    Empty diff -> fall back to the God Nodes, so hot.md always points somewhere.
    """
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    touched = _nodes_for_files(model, changed_files)

    lines = ["---", "kind: hot", "---", "# hot.md — where the action is", ""]
    if touched:
        lines.append(f"Tracking **{len(touched)}** changed node(s) and their 1-hop neighbours.")
        lines.append("")
        for nid in sorted(touched, key=model.label_of):
            lines.append(f"## {model.label_of(nid)} (changed)")
            neighbours = model.neighbors(nid)
            if neighbours:
                joined = ", ".join(model.label_of(n) for n in neighbours)
                lines.append(f"- 1-hop neighbours: {joined}")
            else:
                lines.append("- orphan/isolated node — no neighbours")
            lines.append("")
    else:
        lines.append("No changed files — falling back to the **God Nodes** (central hubs).")
        lines.append("")
        for nid, deg in model.god_nodes(10):
            lines.append(f"- {model.label_of(nid)} — {deg} edges")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
