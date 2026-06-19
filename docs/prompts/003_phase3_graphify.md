# Prompt log 003 — Phase 3: Graphify run + graph.json parser

**Phase:** 3 — Turn the buggy codebase into a knowledge graph (C1) + a queryable model
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-19

## Prompt issued

> Phase 3 goal: turn the buggy codebase into a knowledge graph (C1) and a
> queryable model (`../CLAUDE_CODE_PLAYBOOK.md` §5). Invoke the graphify CLI on
> data/target's source; copy graph.json + GRAPH_REPORT.md + graph.html into
> artifacts/. Parse graph.json (NetworkX node_link) into typed Node/Edge with
> evidence tier (Extracted/Inferred/Ambiguous), communities, centrality
> (betweenness/degree), god_nodes(), neighbors(). Parse GRAPH_REPORT.md god-nodes
> /surprising-edges/suggested-questions. DIY ast+networkx fallback if the CLI
> fails. Tests mock the CLI.

## What was done

A parallel subagent ran the REAL `graphify` (v0.8.42) on `data/target/tqdm/tqdm`
and reported the exact output schema, which shaped the parser:
- Build command is **`graphify extract <src> --backend gemini --out <dir>`**
  (graph.json), then **`graphify cluster-only <dir>`** (GRAPH_REPORT.md +
  graph.html). v0.8.42 has **no `--obsidian`/`--wiki`** flags (the playbook
  assumed an older release) — so our Obsidian vault is fully self-generated in
  Phase 4 (the playbook already specifies that).
- graph.json is `networkx.node_link_data` but **edges are under `"links"`**; each
  edge's evidence tier is the **`confidence`** field (`EXTRACTED`/`INFERRED`/
  `AMBIGUOUS`) with a paired `confidence_score`. Nodes carry `community` /
  `community_name` (28 communities) but **no centrality** → computed with networkx.

Built (TDD, CLI mocked):
- **`graphify/run.py`** — `extract` then `cluster-only` (idempotent); copies the
  three core artifacts into `artifacts/`.
- **`graphify/model.py`** — `GraphModel.from_json` → typed `Node`/`Edge`,
  `degree_centrality`, `betweenness`, `god_nodes`, `communities`, `neighbors`,
  `edges_by_tier` (tiers normalised to lower-case Extracted/Inferred/Ambiguous).
- **`graphify/report.py`** — `parse_report` → god-nodes, surprising connections,
  suggested questions, summary line.
- **`graphify/fallback.py`** — DIY ast+networkx builder emitting graphify's OWN
  schema, so `graph.json` always exists if the CLI is unavailable (ADR-003).
- **`SDK.run_graphify`** (graphify → fallback on failure) + CLI `graphify`.

## Verification

```bash
uv run pytest -m "not live"   # 87 passed, coverage 99.0%
uv run cosmos77-rev graphify
#   graph: 500 nodes, 1071 edges, 28 communities
#   tiers: {'extracted': 813, 'inferred': 258, 'ambiguous': 0}
#   god_nodes: ['tqdm', ...]
test -f artifacts/graph.json && test -f artifacts/GRAPH_REPORT.md   # both present
```

## Honesty note (matters for Phase 8)

For a **pure-Python, code-only** target, graphify's **Gemini semantic pass never
runs** — the corpus scan finds 0 docs/papers/images, so `needs_llm = False`. The
graph is built by AST + symbol resolution at **0 LLM tokens**; the 258 `INFERRED`
edges are AST heuristics (unresolved cross-file calls), not model inferences. We
report this truthfully: the knowledge graph is essentially **free**, and the
token savings we will measure come from the AGENT *using* the graph for focused
retrieval — not from graphify spending tokens. (`GRAPH_REPORT.md` itself prints
`Token cost: 0 input · 0 output`.)
