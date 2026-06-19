"""Pure markdown renderers for every vault page (C2).

Each function returns a markdown string; writing to disk is :mod:`build`'s job.
The pages embody the protocol: ``index.md`` is the navigation hub, ``hot.md`` is
the bug-critical area, and the per-node / per-community pages are the "2-3 pages"
a reader opens. Wikilinks are emitted ONLY for keys the registry knows.
"""

from __future__ import annotations

from cosmos77_ex04.graphify.model import GraphModel
from cosmos77_ex04.vault.links import PageRegistry
from cosmos77_ex04.vault.render import (
    FIX_PROCESS_TEMPLATE,
    INVESTIGATION_TEMPLATE,
    PROTOCOL,
    community_link,
    neighbor_links,
    node_role_line,
    tier_breakdown,
)
from cosmos77_ex04.vault.wikilinks import frontmatter

# Re-export the static templates so callers import them from `pages` (the public
# surface) while `render` keeps them under the 150-line cap.
__all__ = (
    "FIX_PROCESS_TEMPLATE",
    "INVESTIGATION_TEMPLATE",
    "render_community_page",
    "render_hot",
    "render_index",
    "render_node_page",
    "render_suspects",
)


def render_node_page(model: GraphModel, node_id: str, registry: PageRegistry) -> str:
    """Render a god-node page: kind, file, community, neighbors, evidence tiers."""
    node = model.nodes[node_id]
    community = community_link(registry, node.community)
    body = [
        frontmatter({"kind": node.file_type or "node", "community": str(node.community)}),
        f"# {node.label}",
        "",
        node_role_line(model, node_id),
        "",
        f"- **kind:** {node.file_type or 'node'}",
        f"- **file:** {node.file or 'unknown'}",
        f"- **Community:** {community}",
        "",
        "## Neighbors",
        neighbor_links(model, node_id, registry),
        "",
        "## Evidence tiers (Extracted / Inferred / Ambiguous)",
        tier_breakdown(model, node_id),
    ]
    return "\n".join(body) + "\n"


def render_community_page(
    model: GraphModel, community_id: int, member_ids: list[str], registry: PageRegistry
) -> str:
    """Render a Community page listing its members (wikilinks where a page exists)."""
    name = next(
        (model.nodes[m].community_name for m in member_ids if model.nodes[m].community_name),
        "",
    )
    title = f"Community {community_id}" + (f" — {name}" if name else "")
    lines = [
        frontmatter({"kind": "community", "id": str(community_id)}),
        f"# {title}",
        "",
        f"A **Community** of {len(member_ids)} nodes. A **Bridge** links it to others.",
        "",
        "## Members",
    ]
    for mid in member_ids:
        label = model.label_of(mid)
        lines.append(f"- {registry.link(mid, label) if registry.has(mid) else label}")
    return "\n".join(lines) + "\n"


def render_index(model: GraphModel, registry: PageRegistry, report: object) -> str:
    """Render the navigation hub: protocol, hot/suspects, communities, god-nodes."""
    summary = getattr(report, "summary_line", "") or "graph summary unavailable"
    lines = [
        frontmatter({"kind": "index"}),
        "# index.md — navigation hub",
        "",
        f"Protocol: **{PROTOCOL}**.",
        "",
        f"> {summary}",
        "",
        f"- {registry.link('hot', 'hot.md (bug-critical area)')}",
        f"- {registry.link('suspects', 'suspects.md')}",
        "",
        "## Communities",
    ]
    for cid in sorted(model.communities()):
        key = PageRegistry.community_key(cid)
        if registry.has(key):
            lines.append(f"- {registry.link(key, f'Community {cid}')}")
    lines += ["", "## God Nodes (most connected — candidate hubs)"]
    for nid, deg in model.god_nodes(top=len(model.nodes)):
        if registry.has(nid):
            lines.append(f"- {registry.link(nid, model.label_of(nid))} — {deg} edges")
    return "\n".join(lines) + "\n"


def render_hot(
    model: GraphModel, registry: PageRegistry, failing_test: str, seed_ids: list[str]
) -> str:
    """Render hot.md: the God Nodes + the failing-test neighborhood (seeded)."""
    lines = [
        frontmatter({"kind": "hot"}),
        "# hot.md — bug-critical area",
        "",
        f"Failing test: `{failing_test or 'n/a'}`. Start here, then open 2-3 pages.",
        "",
        "## God Nodes (a God Node is an unhealthy Hub — too central)",
    ]
    for nid, deg in model.god_nodes(top=15):
        label = model.label_of(nid)
        entry = registry.link(nid, label) if registry.has(nid) else label
        lines.append(f"- {entry} — {deg} edges")
    lines += ["", "## Failing-test neighborhood"]
    for nid in seed_ids:
        if nid not in model.nodes:
            continue
        label = model.label_of(nid)
        entry = registry.link(nid, label) if registry.has(nid) else label
        lines.append(f"- {entry}")
    return "\n".join(lines) + "\n"


def render_suspects(model: GraphModel, registry: PageRegistry) -> str:
    """Render suspects.md: high-Centrality nodes ranked for guided retrieval."""
    lines = [
        frontmatter({"kind": "suspects"}),
        "# suspects.md",
        "",
        "Ranked by **Centrality** (degree). High signal-to-noise: read the top first.",
        "",
    ]
    between = model.betweenness()
    for nid, deg in model.god_nodes(top=15):
        label = model.label_of(nid)
        entry = registry.link(nid, label) if registry.has(nid) else label
        lines.append(f"- {entry} — degree {deg}, betweenness {between.get(nid, 0.0):.3f}")
    return "\n".join(lines) + "\n"
