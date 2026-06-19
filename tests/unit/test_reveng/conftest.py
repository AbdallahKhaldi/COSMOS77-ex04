"""Shared fixtures for the reveng tests: an in-memory GraphModel + a temp package."""

from __future__ import annotations

import pytest

from cosmos77_ex04.graphify.model import Edge, GraphModel, Node


def _node(node_id: str, community: int) -> Node:
    return Node(
        id=node_id,
        label=node_id,
        file="f.py",
        file_type="code",
        community=community,
        community_name=f"Community {community}",
    )


@pytest.fixture
def model() -> GraphModel:
    """Two communities joined by one mandatory ``bridge`` (a God-Node bottleneck).

    Community 0 is a hub meshed with a ring of leaves (high degree, low
    betweenness -> healthy Hub). ``bridge`` is the single inter-community edge
    feeding the community-1 chain (high degree AND high betweenness -> God Node).
    """
    nodes: list[Node] = [_node("hub", 0)]
    edges: list[Edge] = []
    leaves = [f"l{k}" for k in range(6)]
    for leaf in leaves:
        nodes.append(_node(leaf, 0))
        edges.append(Edge("hub", leaf, "calls", "extracted", 1.0))
    for k, leaf in enumerate(leaves):
        edges.append(Edge(leaf, leaves[(k + 1) % len(leaves)], "calls", "extracted", 1.0))
    nodes.append(_node("bridge", 0))
    edges.append(Edge("l0", "bridge", "calls", "extracted", 1.0))
    for k in range(5):
        nodes.append(_node(f"r{k}", 1))
        edges.append(Edge("bridge", f"r{k}", "calls", "extracted", 1.0))
    for k in range(4):
        edges.append(Edge(f"r{k}", f"r{k + 1}", "calls", "extracted", 1.0))
    return GraphModel(nodes, edges)


@pytest.fixture
def package(tmp_path):
    """A tiny ``.py`` package: a ``Base`` class and a ``Child(Base)`` subclass."""
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "base.py").write_text(
        "class Base:\n    def greet(self):\n        return 'hi'\n",
        encoding="utf-8",
    )
    (pkg / "child.py").write_text(
        "from .base import Base\n\n\nclass Child(Base):\n    def run(self):\n        return 1\n",
        encoding="utf-8",
    )
    return pkg
