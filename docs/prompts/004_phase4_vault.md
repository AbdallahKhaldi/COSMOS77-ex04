# Prompt log 004 — Phase 4: Obsidian knowledge vault

**Phase:** 4 — The Obsidian vault as an ACTIVE knowledge space (C2)
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-19

## Prompt issued

> Phase 4 goal: the Obsidian vault as an active knowledge space (C2), not a file
> dump (`../CLAUDE_CODE_PLAYBOOK.md` §6). Deterministic Python (no LLM). Generate
> `obsidian/` from the graphify model + report: `index.md` (navigation hub, the
> "question → index → 2-3 pages → answer" protocol, links to `[[hot]]` + top
> communities + suspects), `hot.md` (the bug-critical area: god-nodes + the
> failing test's neighborhood), one page per central component / community /
> god-node (kind, file, `[[wikilinks]]`, evidence tier, one-line role),
> `suspects.md`, plus `investigation.md` / `fix-process.md` templates. Sanitise
> filenames; no orphan wikilinks. Split into build.py + pages.py + links.py.

## What was done

Implemented (deterministic, no LLM) under `src/cosmos77_ex04/vault/`, split to
respect the 150-line cap:
- **`wikilinks.py`** — `sanitize_filename`, `wikilink(stem, alias)`, `frontmatter`.
- **`links.py`** — `PageRegistry`: assigns a UNIQUE sanitised stem per node/
  community key; callers only emit a `[[wikilink]]` to a registered key, which
  **guarantees every link resolves** (duplicate labels get distinct stems).
- **`render.py`** — shared helpers + the protocol string + the static
  `INVESTIGATION_TEMPLATE` / `FIX_PROCESS_TEMPLATE` (filled in Phase 7).
- **`pages.py`** — `render_node_page` / `render_community_page` / `render_index`
  / `render_hot` / `render_suspects`.
- **`build.py`** — `build_vault(model, report, out_dir, *, failing_test="",
  top_gods=15, top_comms=28)` → writes `index/hot/suspects/investigation/
  fix-process.md` + `pages/<stem>.md`, returns `{files, pages, god_nodes, communities}`.
- Wired `SDK.build_vault` (loads graph.json + GRAPH_REPORT.md, calls build_vault)
  and the CLI `vault` command.

`hot.md` seeds its "failing-test neighborhood" from the god-nodes ∪ nodes whose
label matches a token of the failing test (`tests_contrib.py::test_enumerate` →
the `enumerate`/`tenumerate` nodes). God-node pages classify Centrality (degree/
betweenness), name the Community, list neighbours, and show Extracted/Inferred/
Ambiguous tier counts (the professor's vocabulary, applied).

## Verification

```bash
uv run pytest -m "not live" -q   # 116 passed, coverage 99.3%
uv run cosmos77-rev vault
#   vault: 48 files (43 pages, 28 communities)
#   god-node pages: 15
# wikilink-resolution scan over obsidian/**.md -> ALL resolve (no orphans)
ls obsidian/index.md obsidian/hot.md   # both present
```

## Notes / decisions

- The vault package was built by a parallel subagent against a precise spec and
  the hard invariant "every `[[wikilink]]` resolves to a generated file"; the
  orchestrator wired the SDK/CLI, ran the real vault on the 500-node tqdm graph,
  and re-verified the invariant on the actual output (48 md files, 0 orphans).
- `test_sdk.py` was split (it crossed the 150-line cap) into `test_sdk.py` +
  `test_sdk_pipeline.py`.
- The vault is committed (C2 deliverable); open `obsidian/` in Obsidian Desktop
  to screenshot the graph view for the README (Phase 10, manual).
