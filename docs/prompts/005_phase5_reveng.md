# Prompt log 005 — Phase 5: Reverse-engineering diagrams (block + OOP) + God Nodes

**Phase:** 5 — The two mandatory illustrations (C3, C4) + God-Node analysis (C14)
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-19

## Prompt issued

> Phase 5 goal: the two mandatory illustrations extracted FROM THE GRAPH —
> engineering understanding, not folder listings (`../CLAUDE_CODE_PLAYBOOK.md`
> §7). Deterministic Python. `block_diagram.py`: communities (subsystems), hubs,
> bridges → Mermaid flowchart + PNG; macro→meso→micro. `oop_schema.py`: ast over
> the target → classes/inheritance/composition → Mermaid classDiagram + PNG.
> `godnodes.py`: rank by centrality (betweenness/degree); classify each
> high-centrality node as a healthy HUB or a bottleneck GOD NODE via the
> diagnosis questions (alternatives exist? mandatory path? hidden over-coupling?)
> → reports/ARCHITECTURE.md with findings + diagrams.

## What was done

Implemented (deterministic, no LLM) under `src/cosmos77_ex04/reveng/`:
- **`block_diagram.py`** — `bridges()` (cross-community edge counts),
  `block_mermaid()` (a `flowchart` of communities + bridges + flow),
  `render_block_png()` (networkx + matplotlib **Agg**, one node per Community
  sized by member count, edges = Bridges — rendered at the macro level, never 500
  raw nodes).
- **`oop_schema.py`** — `extract_classes()` (AST: classes, base classes =
  inheritance, methods), `oop_mermaid()` (a `classDiagram` with `<|--`),
  `render_oop_png()`.
- **`godnodes.py`** + **`report.py`** — `classify()` and the macro→meso→micro
  `ARCHITECTURE.md` writer.
- **`extract.py`** — `extract_diagrams(model, source, artifacts_dir, reports_dir)`
  orchestrator; wired to `SDK.extract_diagrams` + CLI `diagrams`.

**God Node vs Hub rule (documented, applied to real data):** among the top-10
degree nodes, normalised betweenness = `betweenness / max_betweenness`; a node is
a **God Node** when normalised betweenness ≥ 0.5 (high degree AND a mandatory
cross-community Bridge with few alternative paths), else a healthy **Hub**
(well-connected but not the sole path).

## Verification

```bash
uv run pytest -m "not live" -q   # 134 passed, coverage 99.3%
uv run cosmos77-rev diagrams
#   block: artifacts/block_diagram.png  oop: artifacts/oop_schema.png
#   god_nodes: 1, hubs: 9, classes: 32
#   report: reports/ARCHITECTURE.md
ls artifacts/block_diagram.png artifacts/oop_schema.png   # both present
grep -c 'classDiagram\|flowchart' reports/ARCHITECTURE.md  # 2
```

## Findings (real data)

On the tqdm graph (500 nodes / 28 communities), the classifier names exactly ONE
**God Node** — `tqdm` (degree 106, normalised betweenness 1.00): a mandatory
Bridge across communities with few alternatives — and 9 healthy **Hubs**
(`tests_tqdm.py`, `closing()`, `StringIO`, …) with high degree but moderate
betweenness. The OOP schema extracted **32 classes**. ARCHITECTURE.md presents
the macro (communities) → meso (bridges) → micro (God-Node/Hub) reading with both
fenced Mermaid diagrams embedded — engineering understanding, not a folder tree.

## Notes

- PNGs render via matplotlib Agg (no node/npm needed); the reveng package was
  built by a parallel subagent and verified by the orchestrator on the real graph.
