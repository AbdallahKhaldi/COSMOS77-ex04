"""Graph-guided focused retrieval — the context-reduction mechanism (C5).

The agent reads the navigation hub + hot.md + a compact graph summary FIRST,
ranks suspects by Centrality + proximity to the failing test, and fetches ONLY
the top suspects' source files — never the whole repository (which would invite
Context Rot and Lost in the Middle, and disprove our own thesis). No LLM here.
"""

from __future__ import annotations

import re
from pathlib import Path

from cosmos77_ex04.graphify.model import GraphModel


def _test_tokens(failing_test: str) -> set[str]:
    return {tok.lower() for tok in re.split(r"[^A-Za-z0-9]+", failing_test) if len(tok) > 3}


def rank_suspects(
    model: GraphModel, failing_test: str, top_k: int, test_output: str = ""
) -> list[str]:
    """Rank node ids by Centrality, boosted by name-proximity and traceback files.

    The failing-test traceback (when available) names the faulty file directly, so
    a node whose source file appears in it gets the strongest boost — this is what
    steers the agent to the real bug rather than a plausible look-alike.
    """
    degree = model.degree_centrality()
    betweenness = model.betweenness()
    tokens = _test_tokens(failing_test)
    trace_files = {f.lower() for f in re.findall(r"[\w./-]+\.py", test_output)}

    def score(nid: str) -> float:
        node = model.nodes[nid]
        label = node.label.lower()
        file = node.file.lower()
        proximity = 2.0 if any(tok in label for tok in tokens) else 0.0
        in_trace = 5.0 if file and any(tf.endswith(file) for tf in trace_files) else 0.0
        return degree.get(nid, 0) + 10.0 * betweenness.get(nid, 0.0) + proximity + in_trace

    return sorted(model.nodes, key=score, reverse=True)[:top_k]


def fetch_snippets(
    model: GraphModel, suspect_ids: list[str], source_root: Path | str, max_files: int
) -> tuple[dict[str, str], list[str]]:
    """Read ONLY the distinct source files of the top suspects (targeted reads)."""
    root = Path(source_root)
    snippets: dict[str, str] = {}
    files_read: list[str] = []
    for nid in suspect_ids:
        rel = model.nodes[nid].file
        if not rel or rel in snippets:
            continue
        path = root / rel
        if not path.exists():
            continue
        snippets[rel] = path.read_text(encoding="utf-8", errors="replace")
        files_read.append(rel)
        if len(files_read) >= max_files:
            break
    return snippets, files_read


def graph_summary(model: GraphModel) -> str:
    """A compact, high-signal summary of the graph (no raw source)."""
    gods = ", ".join(f"{model.label_of(n)}({d})" for n, d in model.god_nodes(8))
    return (
        f"{len(model.nodes)} nodes, {len(model.edges)} edges, "
        f"{len(model.communities())} communities. "
        f"Evidence tiers: {model.edges_by_tier()}. God nodes (degree): {gods}."
    )


def read_text_file(path: Path | str) -> str:
    """Read a text file if it exists (the persisted failing-test traceback), else ''."""
    file = Path(path)
    return file.read_text(encoding="utf-8", errors="replace") if file.exists() else ""


def read_vault(vault_dir: Path | str, names: tuple[str, ...] = ("index.md", "hot.md")) -> str:
    """Read the navigation hub + bug-critical area (focused context, no source)."""
    root = Path(vault_dir)
    parts = []
    for name in names:
        path = root / name
        if path.exists():
            parts.append(f"## {name}\n{path.read_text(encoding='utf-8')}")
    return "\n\n".join(parts)
