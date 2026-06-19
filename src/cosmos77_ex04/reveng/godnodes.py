"""God-Node / Centrality analysis (C14) — the diagnosis questions in code.

A **God Node** is a bottleneck: a node with BOTH high degree AND high normalised
betweenness — a mandatory cross-community **Bridge** that few alternative paths
can route around. A healthy **Hub** has high degree but moderate/low betweenness:
it is well-connected yet NOT the sole path, so removing it does not sever the
graph. The thresholds are documented on ``classify`` below.
"""

from __future__ import annotations

from dataclasses import dataclass

from cosmos77_ex04.graphify.model import GraphModel
from cosmos77_ex04.reveng.report import write_architecture_report  # noqa: F401

#: A node is a God Node when its degree is in the top-``top`` AND its betweenness
#: is at least this fraction of the graph's maximum betweenness. High degree +
#: high *relative* betweenness == a mandatory bridge bottleneck.
BETWEENNESS_GOD_FRACTION: float = 0.5


@dataclass
class Verdict:
    """A diagnosis for one candidate node: God Node vs healthy Hub."""

    node_id: str
    label: str
    degree: int
    betweenness: float
    kind: str  # "god_node" | "hub"
    reason: str


def classify(model: GraphModel, top: int = 10) -> list[Verdict]:
    """Diagnose the ``top`` highest-degree nodes as ``god_node`` or ``hub``.

    Threshold rule: among the top-``top`` degree nodes, a node is a **God Node**
    when its normalised betweenness (betweenness / max-betweenness in the graph)
    is >= ``BETWEENNESS_GOD_FRACTION`` (0.5) — high degree AND it sits on at least
    half as many shortest paths as the busiest node, i.e. a mandatory Bridge with
    few alternatives. Otherwise it is a healthy **Hub** (well-connected, not a
    sole path). A node bridging two communities reinforces the God-Node verdict.
    """
    between = model.betweenness()
    peak = max(between.values(), default=0.0) or 1.0
    verdicts: list[Verdict] = []
    for node_id, degree in model.god_nodes(top):
        score = between.get(node_id, 0.0)
        norm = score / peak
        crosses = _bridges_communities(model, node_id)
        if norm >= BETWEENNESS_GOD_FRACTION:
            kind = "god_node"
            reason = (
                f"God Node: high degree ({degree}) AND high normalised betweenness "
                f"({norm:.2f} of max) — a mandatory Bridge"
                + (" across communities" if crosses else "")
                + " with few alternative paths."
            )
        else:
            kind = "hub"
            reason = (
                f"Healthy Hub: high degree ({degree}) but moderate/low betweenness "
                f"({norm:.2f} of max) — well-connected, not the sole path."
            )
        verdicts.append(Verdict(node_id, model.label_of(node_id), degree, score, kind, reason))
    return verdicts


def _bridges_communities(model: GraphModel, node_id: str) -> bool:
    """True when ``node_id`` is adjacent to nodes from another community (a Bridge)."""
    node = model.nodes.get(node_id)
    if node is None:
        return False
    return any(
        (nb := model.nodes.get(neighbor)) is not None and nb.community != node.community
        for neighbor in model.neighbors(node_id)
    )
