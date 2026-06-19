"""Shared render helpers, the protocol string, and the static templates (C2).

Extracted from :mod:`pages` so each renderer module stays under the 150-line
cap and the small pure helpers (neighbor links, evidence-tier breakdown, the
one-line Centrality role) have a single home. The investigation / fix-process
templates are static here and filled in Phase 7.
"""

from __future__ import annotations

from cosmos77_ex04.graphify.model import GraphModel
from cosmos77_ex04.vault.links import PageRegistry

#: The professor's guided-retrieval protocol, quoted verbatim everywhere.
PROTOCOL = "question → index → 2-3 pages → answer"

#: Human labels for the three evidence tiers (the professor's vocabulary).
_TIER_LABELS = {
    "extracted": "Extracted",
    "inferred": "Inferred",
    "ambiguous": "Ambiguous",
}


def community_link(registry: PageRegistry, community_id: int) -> str:
    """A resolving wikilink to a Community page, or plain text if it has none."""
    key = PageRegistry.community_key(community_id)
    label = f"Community {community_id}"
    return registry.link(key, label) if registry.has(key) else label


def neighbor_links(model: GraphModel, node_id: str, registry: PageRegistry) -> str:
    """Render a node's neighbors as wikilinks (where a page exists) else plain.

    Why the plain fallback: a neighbor without its own page must NOT become a
    ``[[link]]`` — that would dangle. We print its label instead, preserving the
    invariant that every emitted wikilink resolves.
    """
    parts: list[str] = []
    for nid in model.neighbors(node_id):
        label = model.label_of(nid)
        parts.append(registry.link(nid, label) if registry.has(nid) else label)
    return ", ".join(parts) if parts else "_(no neighbors)_"


def tier_breakdown(model: GraphModel, node_id: str) -> str:
    """Render the Extracted/Inferred/Ambiguous edge counts touching a node."""
    counts = dict.fromkeys(_TIER_LABELS, 0)
    for edge in model.edges:
        if edge.src == node_id or edge.dst == node_id:
            counts[edge.tier] = counts.get(edge.tier, 0) + 1
    return ", ".join(f"{_TIER_LABELS[t]}: {counts[t]}" for t in _TIER_LABELS)


def node_role_line(model: GraphModel, node_id: str) -> str:
    """One-line role mentioning Centrality (degree / betweenness)."""
    degree = model.degree_centrality().get(node_id, 0)
    between = model.betweenness().get(node_id, 0.0)
    verdict = "a God Node (unhealthy Hub)" if degree >= 10 else "a healthy Hub"
    return (
        f"Centrality: degree {degree}, betweenness {between:.3f} — likely {verdict}. "
        "A Bridge spanning Communities raises betweenness."
    )


#: Static investigation template (filled in Phase 7).
INVESTIGATION_TEMPLATE = (
    "---\nkind: investigation\n---\n"
    "# investigation.md\n\n"
    "Follow the protocol: question → index → 2-3 pages → answer.\n\n"
    "1. Read [[index]] to orient (the navigation hub).\n"
    "2. Open [[hot]] for the bug-critical area.\n"
    "3. Read 2-3 god-node / community pages — guided retrieval keeps a high\n"
    "   signal-to-noise ratio (no Context Rot, no Lost in the Middle).\n"
    "4. Form a hypothesis from Extracted edges first, then Inferred, then\n"
    "   Ambiguous.\n\n"
    "_(Phase 7 fills the concrete bug walkthrough here.)_\n"
)

#: Static fix-process template (filled in Phase 7).
FIX_PROCESS_TEMPLATE = (
    "---\nkind: fix-process\n---\n"
    "# fix-process.md\n\n"
    "1. Reproduce the failing test (the bug-critical area, see [[hot]]).\n"
    "2. Localise via Centrality + the God Node neighborhood.\n"
    "3. Apply the minimal change; keep Extracted edges intact.\n"
    "4. Re-run the test and record the token ledger.\n\n"
    "_(Phase 7 fills the concrete fix steps here.)_\n"
)
