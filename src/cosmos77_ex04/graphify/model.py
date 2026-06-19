"""Typed, queryable model over graphify's graph.json (C1, C14).

graphify writes ``networkx.node_link_data`` with edges under ``"links"``; each
edge carries a ``confidence`` evidence tier (``EXTRACTED``/``INFERRED``/
``AMBIGUOUS`` — the professor's tiers) and a numeric ``confidence_score``. Nodes
carry a ``community`` id but NO centrality, so we compute degree + betweenness
with networkx. This model is the queryable surface the vault, reveng, and the
graph-guided agent all read.
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import networkx as nx

from cosmos77_ex04.constants import EVIDENCE_TIERS


@dataclass
class Node:
    """A graph node (a code symbol or file)."""

    id: str
    label: str
    file: str
    file_type: str
    community: int
    community_name: str
    location: str = ""


@dataclass
class Edge:
    """A graph edge with its evidence tier (C14)."""

    src: str
    dst: str
    relation: str
    tier: str
    confidence: float


def normalise_tier(value: str) -> str:
    """Lower-case a graphify ``confidence`` to one of EVIDENCE_TIERS (default ambiguous)."""
    tier = (value or "").strip().lower()
    return tier if tier in EVIDENCE_TIERS else "ambiguous"


class GraphModel:
    """A parsed, queryable graphify graph."""

    def __init__(self, nodes: list[Node], edges: list[Edge]) -> None:
        self.nodes: dict[str, Node] = {n.id: n for n in nodes}
        self.edges: list[Edge] = list(edges)
        self._graph: nx.DiGraph | None = None
        self._betweenness: dict[str, float] | None = None

    @classmethod
    def from_json(cls, path: Path | str) -> GraphModel:
        """Parse a graphify ``graph.json`` (edges live under ``links``)."""
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        nodes = [cls._node(n) for n in data.get("nodes", [])]
        edges = [cls._edge(e) for e in data.get("links", data.get("edges", []))]
        return cls(nodes, edges)

    @staticmethod
    def _node(raw: dict) -> Node:
        return Node(
            id=raw["id"],
            label=raw.get("label", raw["id"]),
            file=raw.get("source_file", ""),
            file_type=raw.get("file_type", ""),
            community=int(raw.get("community", -1)),
            community_name=raw.get("community_name", ""),
            location=raw.get("source_location", ""),
        )

    @staticmethod
    def _edge(raw: dict) -> Edge:
        return Edge(
            src=raw["source"],
            dst=raw["target"],
            relation=raw.get("relation", ""),
            tier=normalise_tier(raw.get("confidence", "")),
            confidence=float(raw.get("confidence_score", 0.0) or 0.0),
        )

    @property
    def graph(self) -> nx.DiGraph:
        """The lazily-built directed networkx graph."""
        if self._graph is None:
            g: nx.DiGraph = nx.DiGraph()
            for nid, node in self.nodes.items():
                g.add_node(nid, label=node.label, community=node.community)
            for edge in self.edges:
                g.add_edge(edge.src, edge.dst, relation=edge.relation, tier=edge.tier)
            self._graph = g
        return self._graph

    def degree_centrality(self) -> dict[str, int]:
        """Total (in + out) degree per node — graphify's "most connected" measure."""
        g = self.graph
        return {nid: g.degree(nid) for nid in g.nodes}

    def betweenness(self) -> dict[str, float]:
        """Betweenness centrality (bridges); computed once on the undirected view."""
        if self._betweenness is None:
            self._betweenness = nx.betweenness_centrality(self.graph.to_undirected())
        return self._betweenness

    def god_nodes(self, top: int = 10) -> list[tuple[str, int]]:
        """The ``top`` highest-degree nodes (candidate God Nodes / hubs)."""
        ranked = sorted(self.degree_centrality().items(), key=lambda kv: kv[1], reverse=True)
        return ranked[:top]

    def communities(self) -> dict[int, list[str]]:
        """Node ids grouped by their graphify community id."""
        out: dict[int, list[str]] = defaultdict(list)
        for nid, node in self.nodes.items():
            out[node.community].append(nid)
        return dict(out)

    def neighbors(self, node_id: str) -> list[str]:
        """All adjacent node ids (successors ∪ predecessors), sorted."""
        g = self.graph
        if node_id not in g:
            return []
        return sorted(set(g.successors(node_id)) | set(g.predecessors(node_id)))

    def edges_by_tier(self) -> dict[str, int]:
        """Count edges per evidence tier (Extracted/Inferred/Ambiguous)."""
        counts = dict.fromkeys(EVIDENCE_TIERS, 0)
        for edge in self.edges:
            counts[edge.tier] = counts.get(edge.tier, 0) + 1
        return counts

    def label_of(self, node_id: str) -> str:
        """The human label for a node id (falls back to the id)."""
        node = self.nodes.get(node_id)
        return node.label if node else node_id
