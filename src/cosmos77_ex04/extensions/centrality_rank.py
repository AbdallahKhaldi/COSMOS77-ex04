"""Original extension — the agent's suspect ranking made explicit (C9).

``rank_suspects`` (agent/retrieval.py) returns only ids; here we surface the WHY:
a per-node row carrying its Centrality (degree + betweenness) and the proximity/
traceback boost, then persist it as ``obsidian/suspects.md`` — a ranked table of
candidate buggy nodes the investigator reads top-first (high signal-to-noise, no
Context Rot). Deterministic, no LLM.
"""

from __future__ import annotations

import re
from pathlib import Path

from cosmos77_ex04.graphify.model import GraphModel

#: Weights mirror agent/retrieval.rank_suspects so the table explains its ranking.
_BETWEENNESS_WEIGHT = 10.0
_PROXIMITY_BOOST = 2.0
_TRACEBACK_BOOST = 5.0


def _test_tokens(failing_test: str) -> set[str]:
    """Significant (>3 char) tokens of the failing-test name, lower-cased."""
    return {tok.lower() for tok in re.split(r"[^A-Za-z0-9]+", failing_test) if len(tok) > 3}


def rank_suspects_scored(
    model: GraphModel, failing_test: str, test_output: str = "", top: int = 10
) -> list[dict]:
    """Rank nodes by an explicit Centrality + proximity score, returning rows.

    Each row exposes ``degree``, ``betweenness`` and the combined ``score`` so the
    ranking is auditable — this is what steers the agent to the real bug rather
    than a plausible look-alike.
    """
    degree = model.degree_centrality()
    betweenness = model.betweenness()
    tokens = _test_tokens(failing_test)
    trace_files = {f.lower() for f in re.findall(r"[\w./-]+\.py", test_output)}

    rows: list[dict] = []
    for nid, node in model.nodes.items():
        label, file = node.label.lower(), node.file.lower()
        proximity = _PROXIMITY_BOOST if any(tok in label for tok in tokens) else 0.0
        in_trace = (
            _TRACEBACK_BOOST if file and any(tf.endswith(file) for tf in trace_files) else 0.0
        )
        deg, bet = degree.get(nid, 0), betweenness.get(nid, 0.0)
        score = deg + _BETWEENNESS_WEIGHT * bet + proximity + in_trace
        rows.append(
            {
                "node_id": nid,
                "label": node.label,
                "file": node.file,
                "degree": deg,
                "betweenness": round(bet, 4),
                "score": round(score, 4),
            }
        )
    rows.sort(key=lambda r: r["score"], reverse=True)
    return rows[:top]


def write_suspects_md(ranking: list[dict], out_path: Path | str) -> Path:
    """Overwrite ``obsidian/suspects.md`` with a ranked candidate-buggy-node table."""
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        "kind: suspects",
        "---",
        "# suspects.md",
        "",
        "Ranked by **Centrality** (degree + betweenness) and proximity to the "
        "failing test. High signal-to-noise: read the top first.",
        "",
        "| Rank | Candidate | File | Degree | Betweenness | Score |",
        "| ---: | --- | --- | ---: | ---: | ---: |",
    ]
    for rank, row in enumerate(ranking, start=1):
        lines.append(
            f"| {rank} | {row['label']} | {row['file'] or '-'} | "
            f"{row['degree']} | {row['betweenness']} | {row['score']} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
