"""DIY ast+networkx fallback graph builder (ADR-003) — graph.json always exists.

Used ONLY when the graphify CLI is unavailable or fails. Walks the target's
``.py`` files and emits module/class/function nodes plus contains/imports/inherits
edges in graphify's OWN graph.json schema (nodes + ``links``, ``confidence`` tier),
so :class:`~cosmos77_ex04.graphify.model.GraphModel` parses it identically.
Communities are the connected components.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import networkx as nx


def _node_id(scope: str, name: str) -> str:
    raw = f"{scope}:{name}"
    return "".join(ch if ch.isalnum() else "_" for ch in raw).lower()


def _add(nodes: dict, graph: nx.Graph, nid: str, label: str, rel: str) -> None:
    if nid not in nodes:
        nodes[nid] = {
            "id": nid,
            "label": label,
            "norm_label": label,
            "file_type": "code",
            "source_file": rel,
            "source_location": "L1",
            "_origin": "ast",
            "community": 0,
            "community_name": "Community 0",
        }
        graph.add_node(nid)


def _link(links: list, graph: nx.Graph, src: str, dst: str, relation: str) -> None:
    links.append(
        {
            "source": src,
            "target": dst,
            "relation": relation,
            "confidence": "EXTRACTED",
            "confidence_score": 1.0,
            "weight": 1.0,
        }
    )
    graph.add_edge(src, dst)


def _walk_module(
    tree: ast.AST, rel: str, mod_id: str, nodes: dict, links: list, g: nx.Graph
) -> None:
    for item in ast.walk(tree):
        if isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            nid = _node_id(rel, item.name)
            _add(nodes, g, nid, item.name, rel)
            _link(links, g, mod_id, nid, "contains")
            if isinstance(item, ast.ClassDef):
                for base in item.bases:
                    name = getattr(base, "id", None)
                    if name:
                        bid = _node_id(rel, name)
                        _add(nodes, g, bid, name, rel)
                        _link(links, g, nid, bid, "inherits")
        elif isinstance(item, ast.Import | ast.ImportFrom):
            module = getattr(item, "module", None) or (item.names[0].name if item.names else "")
            if module:
                tid = _node_id(module, module)
                _add(nodes, g, tid, module, module)
                _link(links, g, mod_id, tid, "imports")


def build_graph(source: Path | str) -> dict:
    """Build a graphify-schema graph dict from the ``.py`` files under ``source``."""
    source = Path(source)
    nodes: dict[str, dict] = {}
    links: list[dict] = []
    graph: nx.Graph = nx.Graph()
    for py in sorted(source.rglob("*.py")):
        rel = str(py.relative_to(source))
        mod_id = _node_id(rel, rel)
        _add(nodes, graph, mod_id, rel, rel)
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        _walk_module(tree, rel, mod_id, nodes, links, graph)
    for cid, component in enumerate(nx.connected_components(graph)):
        for nid in component:
            nodes[nid]["community"] = cid
            nodes[nid]["community_name"] = f"Community {cid}"
    return {
        "directed": False,
        "multigraph": False,
        "graph": {},
        "nodes": list(nodes.values()),
        "links": links,
        "hyperedges": [],
    }


def write_fallback(source: Path | str, out_path: Path | str) -> Path:
    """Build the DIY graph and write it to ``out_path`` as graph.json."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build_graph(source), indent=2), encoding="utf-8")
    return out
