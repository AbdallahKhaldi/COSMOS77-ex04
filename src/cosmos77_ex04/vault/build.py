"""Assemble the Obsidian knowledge vault from a GraphModel (C2).

This is the orchestration seam Phase 8 wires into the CLI. It builds a
:class:`PageRegistry` so EVERY wikilink resolves, writes the five static pages
plus one page per god-node and per community, and returns a small manifest the
CLI prints. The static pages share stems with their registry keys so the
templates' ``[[index]]`` / ``[[hot]]`` links resolve too.
"""

from __future__ import annotations

from pathlib import Path

from cosmos77_ex04.constants import DEFAULT_ENCODING
from cosmos77_ex04.graphify.model import GraphModel
from cosmos77_ex04.vault.links import PageRegistry
from cosmos77_ex04.vault.pages import (
    FIX_PROCESS_TEMPLATE,
    INVESTIGATION_TEMPLATE,
    render_community_page,
    render_hot,
    render_index,
    render_node_page,
    render_suspects,
)

#: The five always-written top-level pages (key == stem == filename minus .md).
_STATIC_PAGES = ("index", "hot", "suspects", "investigation", "fix-process")


def _seed_ids(model: GraphModel, god_ids: list[str], failing_test: str) -> list[str]:
    """Seed the failing-test neighborhood: god nodes ∪ label-token matches.

    Why: ``hot.md`` must surface nodes named in the failing test (e.g. a label
    containing ``enumerate``) alongside the God Nodes, per the bug-critical
    "failing-test neighborhood" section.
    """
    tokens = [t.lower() for t in failing_test.replace("::", " ").split() if len(t) > 2]
    seeds = list(god_ids)
    for nid, node in model.nodes.items():
        label = node.label.lower()
        if nid not in seeds and any(tok in label for tok in tokens):
            seeds.append(nid)
    return seeds


def _build_registry(model: GraphModel, god_ids: list[str], top_comms: int) -> PageRegistry:
    """Register static pages, god-node pages, and community pages (unique stems)."""
    registry = PageRegistry()
    for name in _STATIC_PAGES:
        registry.register(name, name)
    for nid in god_ids:
        registry.register(nid, model.label_of(nid))
    for cid in sorted(model.communities())[:top_comms]:
        registry.register(PageRegistry.community_key(cid), f"Community {cid}")
    return registry


def build_vault(
    model: GraphModel,
    report: object,
    out_dir: Path | str,
    *,
    failing_test: str = "",
    top_gods: int = 15,
    top_comms: int = 28,
) -> dict:
    """Write the vault to ``out_dir`` and return a manifest of what was emitted.

    Returns ``{"files", "pages", "god_nodes", "communities"}`` where ``files`` is
    every ``.md`` written, ``pages`` is just the ``pages/<stem>.md`` set, and
    ``god_nodes`` is the ordered list of god-node ids that got a page.
    """
    out = Path(out_dir)
    pages_dir = out / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    god_ids = [nid for nid, _ in model.god_nodes(top=top_gods)]
    registry = _build_registry(model, god_ids, top_comms)
    seed_ids = _seed_ids(model, god_ids, failing_test)

    statics = {
        "index": render_index(model, registry, report),
        "hot": render_hot(model, registry, failing_test, seed_ids),
        "suspects": render_suspects(model, registry),
        "investigation": INVESTIGATION_TEMPLATE,
        "fix-process": FIX_PROCESS_TEMPLATE,
    }
    for name, text in statics.items():
        (out / f"{registry.stem_of(name)}.md").write_text(text, encoding=DEFAULT_ENCODING)

    page_count = 0
    for nid in god_ids:
        text = render_node_page(model, nid, registry)
        (pages_dir / f"{registry.stem_of(nid)}.md").write_text(text, encoding=DEFAULT_ENCODING)
        page_count += 1
    communities = model.communities()
    for cid in sorted(communities)[:top_comms]:
        key = PageRegistry.community_key(cid)
        text = render_community_page(model, cid, communities[cid], registry)
        (pages_dir / f"{registry.stem_of(key)}.md").write_text(text, encoding=DEFAULT_ENCODING)
        page_count += 1

    return {
        "files": len(statics) + page_count,
        "pages": page_count,
        "god_nodes": god_ids,
        "communities": min(len(communities), top_comms),
    }
