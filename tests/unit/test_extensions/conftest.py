"""Shared in-memory fixtures for the extensions tests (no live I/O, rule 17).

The toy graph has a clear top suspect (``a`` = tqdm, the most connected), an
ORPHAN (``orph``, no edges), an ``_``-prefixed intentional orphan (``_helper``),
and a node (``c``) with reverse-dependents so impact has a real blast radius.
"""

from __future__ import annotations

import pytest

from cosmos77_ex04.graphify.model import Edge, GraphModel, Node


@pytest.fixture
def model() -> GraphModel:
    """A small, fully deterministic GraphModel covering every extension path."""
    nodes = [
        Node("a", "tqdm", "std.py", "code", 0, "Community 0"),
        Node("b", "tenumerate", "contrib_init.py", "code", 0, "Community 0"),
        Node("c", "helper", "utils.py", "code", 1, "Community 1"),
        Node("orph", "lonely", "dead.py", "code", 2, "Community 2"),
        Node("_helper", "_helper", "compat.py", "code", 2, "Community 2"),
    ]
    edges = [
        Edge("a", "b", "calls", "extracted", 1.0),
        Edge("a", "c", "calls", "extracted", 1.0),
        Edge("b", "c", "uses", "inferred", 0.8),
    ]
    return GraphModel(nodes, edges)
