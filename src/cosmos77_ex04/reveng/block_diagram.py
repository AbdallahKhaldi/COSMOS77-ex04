"""Architectural BLOCK diagram (C3) — extracted from the graph, not folders.

The right macro abstraction is one block per **Community** (sized by member
count); the connections between blocks are **Bridges** — the cross-community
edges that carry control/data flow between sub-systems. We render the Mermaid
``flowchart`` (for the report) AND a matplotlib/networkx PNG (headless Agg).
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # headless backend — set BEFORE importing pyplot.
import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402

from cosmos77_ex04.graphify.model import GraphModel  # noqa: E402


def bridges(model: GraphModel) -> dict[tuple[int, int], int]:
    """Count cross-community edges (Bridges) as ``{(low, high): count}``.

    A Bridge is any edge whose endpoints live in different communities; the
    ordered ``(low, high)`` key makes the undirected block edge deterministic.
    """
    counts: dict[tuple[int, int], int] = {}
    for edge in model.edges:
        src = model.nodes.get(edge.src)
        dst = model.nodes.get(edge.dst)
        if src is None or dst is None or src.community == dst.community:
            continue
        key = (min(src.community, dst.community), max(src.community, dst.community))
        counts[key] = counts.get(key, 0) + 1
    return counts


def _community_label(model: GraphModel, community: int) -> str:
    """Human label for a community (its ``community_name`` or ``Community N``)."""
    for nid in model.communities().get(community, []):
        name = model.nodes[nid].community_name
        if name:
            return name
    return f"Community {community}"


def block_mermaid(model: GraphModel) -> str:
    """Render a Mermaid ``flowchart`` of communities (blocks) + bridges (flow)."""
    comms = model.communities()
    lines = ["flowchart TD"]
    for community in sorted(comms):
        size = len(comms[community])
        label = _community_label(model, community)
        lines.append(f'    C{community}["{label}<br/>({size} nodes)"]')
    for (low, high), weight in sorted(bridges(model).items()):
        lines.append(f"    C{low} -->|{weight} bridge edges| C{high}")
    return "\n".join(lines)


def _community_graph(model: GraphModel) -> nx.Graph:
    """Build the macro networkx graph: one node per community, edges = bridges."""
    comms = model.communities()
    graph: nx.Graph = nx.Graph()
    for community in sorted(comms):
        graph.add_node(
            community,
            size=len(comms[community]),
            label=_community_label(model, community),
        )
    for (low, high), weight in bridges(model).items():
        graph.add_edge(low, high, weight=weight)
    return graph


def render_block_png(model: GraphModel, out_path):
    """Render the community/bridge block graph to ``out_path`` (a PNG ``Path``)."""
    from pathlib import Path

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    graph = _community_graph(model)
    sizes = [300 + 120 * graph.nodes[n]["size"] for n in graph.nodes]
    pos = nx.spring_layout(graph, seed=77, k=0.9)
    fig, ax = plt.subplots(figsize=(12, 9))
    nx.draw_networkx_nodes(graph, pos, node_size=sizes, node_color="#9ecae1", ax=ax)
    nx.draw_networkx_edges(graph, pos, alpha=0.4, ax=ax)
    nx.draw_networkx_labels(graph, pos, font_size=7, ax=ax)
    ax.set_title("Block Diagram — Communities (macro) linked by Bridges")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out
