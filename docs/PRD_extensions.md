# PRD — Original Extensions (`run_extensions`)

**Course:** Orchestration of AI Agents (203.3763), Dr. Yoram Segal · **Assignment:** HW4
**Authors:** Abdallah Khaldi, Tasneem Natour · **Version:** 1.00 · **Status:** Specification (Phase 9)
**Maps to acceptance criteria:** **C9** (≥1 original extension per part) · supports **C2** (vault), **C3/C14** (architecture, God Node vs Hub), **C7** (before/after at knowledge level)

## 1. Purpose

This mechanism delivers the **original extensions** that turn the static pipeline (graph → vault →
agent → fix) into a *self-sharpening* loop. Each extension is a real, tested module — not a sketch —
that reads the artifacts produced upstream (`artifacts/graph.json`, the BugsInPy `TargetInfo`, the
git working tree) and writes a concrete deliverable back into the vault or `reports/`. Four
extensions, one per "part" of the assignment, satisfy **C9**:

1. **`centrality_rank.py`** — rank suspect nodes by **Centrality** (betweenness/degree) *and* by
   proximity (graph distance) to the failing test, then feed the ranking into the agent's suspect
   selection and into `obsidian/suspects.md`. This is guided retrieval made measurable: the agent
   reads the *highest-signal* suspects first, side-stepping Lost in the Middle and Context Rot.
2. **`dynamic_hot.py`** — regenerate `obsidian/hot.md` from `git diff` (changed files) **∩**
   `graph.json` (the changed files' graph neighborhood). A `hot.md` that tracks *where the action is*
   rather than a frozen snapshot. Optionally wired to a git `post-commit` hook.
3. **`orphans.py`** — detect **isolated/orphan** nodes (no in- and no out-edges) and classify each as
   *intentional adapter/legacy* vs *dead code* per a documented verification protocol; write
   `reports/ORPHANS.md` with an `Extracted`/`Inferred`/`Ambiguous` evidence tier per node.
4. **`impact_report.py`** — diff the graph **before vs after** the fix and answer "what breaks if we
   change X": did the **God Node** betweenness drop, did **Community** boundaries get cleaner, which
   **Bridge** edges moved? Write `reports/IMPACT.md`.

Each extension is independent (no shared mutable state), config-driven (Rule 4), and ≤150 lines per
file (Rule 1). All graph/git/LLM I/O is mocked in tests (Rule 6); the only business entry is
`SDK().run_extensions()` (Rule 2). The extensions are the project's *answer to research question (h)*.

## 2. Inputs / Outputs

**Inputs** (all config-driven; read via the dot-path Config loader — new `extensions.*` block):

| Source | Key | Default | Meaning |
|--------|-----|---------|---------|
| `config/setup.json` | `extensions.enabled` | `["centrality_rank","dynamic_hot","orphans","impact_report"]` | Which extensions `run_extensions()` runs, in order. |
| `config/setup.json` | `extensions.centrality.metric` | `betweenness` | Primary centrality metric (`betweenness`\|`degree`). |
| `config/setup.json` | `extensions.centrality.proximity_weight` | `0.5` | Blend of centrality vs failing-test proximity in the suspect score. |
| `config/setup.json` | `extensions.centrality.top_k` | `10` | Suspects written to `suspects.md` / handed to the agent. |
| `config/setup.json` | `extensions.dynamic_hot.diff_base` | `HEAD` | Git ref the working tree is diffed against. |
| `config/setup.json` | `extensions.dynamic_hot.neighborhood_radius` | `1` | Hops of graph neighbours pulled in around each changed node. |
| `config/setup.json` | `extensions.dynamic_hot.install_hook` | `false` | Whether to write a `post-commit` hook stub. |
| `config/setup.json` | `extensions.impact.baseline_graph` | `artifacts/graph_before.json` | Pre-fix graph snapshot for the diff. |
| `config/setup.json` | `paths.{obsidian_dir,reports_dir,artifacts_dir}` | (existing) | Output roots. |

**Outputs** — written under the configured `obsidian/` and `reports/` roots, plus an in-memory
`ExtensionsResult` returned by `run_extensions()` and serialized to `artifacts/extensions.json`:

- `obsidian/suspects.md` — ranked suspects table (rank, node, centrality, distance-to-test, score,
  evidence tier), `[[wikilinked]]` into the vault navigation hub.
- `obsidian/hot.md` — regenerated bug-critical area: changed files ∩ their graph neighborhood.
- `reports/ORPHANS.md` — orphan inventory with classification + verification status per node.
- `reports/IMPACT.md` — before/after graph diff: God-Node betweenness delta, community-boundary
  cleanliness delta, moved bridges, and the "what breaks if we change X" narrative.
- `ExtensionsResult(ranked_suspects, hot_nodes, orphans, impact_delta)` — typed, for tests + README.

**Side effects:** the four files above; `artifacts/extensions.json`; optionally `.git/hooks/post-commit`.

## 3. Module design (files + responsibilities — each ≤150 lines)

All live under `src/cosmos77_ex04/extensions/`. The 150-line cap drives a **one-extension-per-file**
split with two shared helpers so graph loading and Markdown emission are never duplicated (Rule 3).

### 3.1 `extensions/graph_io.py` — shared graph loader (~70 lines)
Pure-ish I/O isolated behind one seam so every extension shares it (Rule 3): `load_graph(path) ->
nx.DiGraph` (parses `graph.json` into a `networkx.DiGraph` with node/edge attributes incl. evidence
tier), `failing_test_nodes(graph, target_info) -> list[str]` (maps the BugsInPy failing test to its
graph node(s)), and `neighborhood(graph, nodes, radius) -> set[str]`. The single mock seam for graph data.

### 3.2 `extensions/centrality_rank.py` — suspect ranking (~120 lines)
`rank_suspects(graph, test_nodes, cfg) -> list[Suspect]`. Computes `nx.betweenness_centrality` (or
degree per `metric`), computes shortest-path distance from each node to the nearest `test_node`,
normalizes both to `[0,1]`, and blends: `score = (1-w)*centrality + w*(1/(1+distance))`. Returns the
top-`k` `Suspect(node, centrality, distance, score, tier)` sorted descending. `write_suspects_md(...)`
renders the vault page; `as_agent_seed(suspects) -> list[str]` returns node ids the agent's suspect-
selection state consumes first. **No I/O in the ranking core** — graph in, list out — so order is unit-testable.

### 3.3 `extensions/dynamic_hot.py` — hot.md from git ∩ graph (~120 lines)
`changed_files(diff_base, runner) -> list[Path]` (parses `git diff --name-only`), `hot_nodes(graph,
changed, radius) -> list[str]` (nodes whose file ∈ changed, plus their `neighborhood`), and
`write_hot_md(graph, hot_nodes, godnodes)` (renders the bug-critical area, flagging any God Node in
the hot set). `maybe_install_hook(cfg, runner)` writes a `post-commit` stub that re-invokes
`cosmos77-rev extensions --only dynamic_hot` when `install_hook` is true. `git` is the only live I/O,
behind a `runner` callable (the mock seam).

### 3.4 `extensions/orphans.py` — orphan detection + classification (~120 lines)
`find_orphans(graph) -> list[str]` (nodes with `in_degree==0 and out_degree==0`).
`classify(node, graph, source_index) -> OrphanVerdict` applies the **verification protocol**:
(a) referenced only via dynamic dispatch / `__all__` / entry-point ⇒ *intentional adapter*, tier
`Inferred`; (b) test-only or `__init__` re-export ⇒ *intentional*, `Extracted`; (c) no references
anywhere in source ⇒ *dead code candidate*, `Inferred`; (d) undecidable ⇒ *Ambiguous* (never asserted
dead). `write_orphans_md(verdicts)` renders `reports/ORPHANS.md`. Classification core takes data in,
verdict out — fully testable on a fixture graph.

### 3.5 `extensions/impact_report.py` — before/after graph diff (~120 lines)
`betweenness_delta(before, after) -> dict[str,float]` and `god_node_delta(before, after, threshold)`
(did the top God Node's betweenness drop?). `community_cleanliness(graph) -> float` (e.g. modularity
or inter-community edge ratio via `nx.algorithms.community`), `moved_bridges(before, after) ->
list[Edge]`. `write_impact_md(...)` renders the "what breaks if we change X" report: God-Node
betweenness before→after, community-boundary delta, bridges added/removed. Pure functions over two graphs.

### 3.6 `extensions/runner.py` — orchestration (~90 lines)
`run(cfg, target_info) -> ExtensionsResult`: loads the graph once via `graph_io`, dispatches the
`extensions.enabled` list in order, collects each extension's typed result, writes
`artifacts/extensions.json`, and returns `ExtensionsResult`. The only module the SDK imports. Shared
dataclasses (`Suspect`, `OrphanVerdict`, `ExtensionsResult`, `Edge`) live in `shared/models.py` if
reused by the agent; otherwise local. `markdown.py` (a ~50-line helper) owns table rendering so the
five extensions don't each reinvent it (Rule 3).

## 4. Public SDK API

Single entry point — all business logic flows through `class SDK` (Rule 2):

```python
# src/cosmos77_ex04/sdk/sdk.py
def run_extensions(self, only: list[str] | None = None) -> ExtensionsResult:
    """Run the original extensions (C9) over the produced graph + target.

    Loads artifacts/graph.json + TargetInfo, then runs the extensions named in
    config extensions.enabled (or the `only` subset): centrality_rank (ranked
    suspects -> obsidian/suspects.md + agent seed), dynamic_hot (git diff ∩ graph
    -> obsidian/hot.md), orphans (isolated nodes -> reports/ORPHANS.md), and
    impact_report (before/after graph diff -> reports/IMPACT.md). Config-driven
    (Rule 4); all git/graph I/O behind mockable seams. Returns ExtensionsResult
    and writes artifacts/extensions.json. Does not mutate the source tree.
    """
```

CLI surface (Typer): `uv run cosmos77-rev extensions [--only NAME ...]` invokes
`SDK().run_extensions(only=...)` and prints the four output paths plus the headline numbers (top
suspect, hot-node count, orphan count, God-Node betweenness delta). Wired as the `extensions` stage in
`PIPELINE_STAGES`.

## 5. Test plan (TDD, ALL git/graph/LLM I/O MOCKED — Rule 6; deterministic, seeded)

Mock seams: `graph_io.load_graph` fed a small fixture `DiGraph`; the `git` `runner` callable fed a
canned `git diff` stdout; `tmp_path` for all writes; no live git, no network, no real LLM. Fixtures
live in `tests/fixtures/` (`fixture_graph.json` with a known God Node, a community split, a bridge,
and one isolated node; `fixture_diff.txt`; a `fixture_graph_before.json` / `_after.json` pair).

**Happy path**
- `test_centrality_rank_order` — on `fixture_graph.json` with a known failing-test node, `rank_suspects`
  returns the central, test-adjacent node **first**; assert the exact ranked node-id order and that
  `score` is monotonically non-increasing (the core C9 claim: highest-signal suspect surfaces first).
- `test_centrality_proximity_weight` — raising `proximity_weight` re-orders a far-but-central node
  below a near-but-peripheral one (blend behaves as specified).
- `test_centrality_writes_suspects_md` — `suspects.md` is written with the top-`k` rows, evidence tiers,
  and resolvable `[[wikilinks]]`; `as_agent_seed` returns the same node ids in rank order.
- `test_dynamic_hot_intersects_diff_with_graph` — given `fixture_diff.txt` (two changed files) and the
  graph, `hot_nodes` returns exactly the nodes in those files plus their radius-1 neighbours; a God Node
  in the hot set is flagged; `hot.md` is regenerated.
- `test_orphans_detects_isolated_node` — `find_orphans` returns exactly the one fixture node with no
  in/out edges; a connected node is never reported.
- `test_orphans_classification_protocol` — an `__all__`-exported orphan classifies as *intentional
  adapter* (`Inferred`); a never-referenced orphan as *dead code candidate* (`Inferred`); an
  undecidable one as *Ambiguous* (never asserted dead). `ORPHANS.md` carries the tier.
- `test_impact_betweenness_delta` — on the before/after fixture pair, `betweenness_delta` reports the
  God Node's betweenness **dropping** by the expected amount and `community_cleanliness` improving;
  `IMPACT.md` contains the before→after numbers.
- `test_run_extensions_runs_enabled_in_order` — `run_extensions()` with the default config writes all
  four files, returns a populated `ExtensionsResult`, and persists `artifacts/extensions.json`;
  `--only dynamic_hot` runs just that one.

**Error path**
- `test_missing_graph_raises` — absent `artifacts/graph.json` raises a clear `GraphNotFoundError`
  naming the path (never silently emits empty reports).
- `test_no_test_node_match` — when the failing test maps to no graph node, `rank_suspects` falls back to
  pure centrality and records `distance=inf`/tier `Ambiguous` rather than crashing.
- `test_dynamic_hot_empty_diff` — an empty `git diff` yields an explicit "no changed nodes" `hot.md`,
  not a stack trace; `git` errors surface as `GitDiffError`.
- `test_impact_missing_baseline` — absent `graph_before.json` raises rather than reporting a fake delta.
- `test_unknown_extension_name` — `extensions.enabled=["bogus"]` raises `ValueError` listing valid names.

Determinism: seeded `random`; `betweenness_centrality` is deterministic on the fixed fixture; coverage
of `extensions/` ≥85%; `ruff check` clean; every file ≤150 lines.

## 6. Acceptance-criteria mapping

| Criterion | How this mechanism satisfies it | Evidence |
|-----------|--------------------------------|----------|
| **C9** — ≥1 original extension per part | Four real, tested extensions (centrality suspect-ranking, dynamic `hot.md`, orphan detection, diff-based impact report), each with happy + error unit tests on fixtures. | `src/cosmos77_ex04/extensions/*`, `tests/unit/test_extensions_*`, `artifacts/extensions.json`. |
| Supports **C2** — active vault | `centrality_rank` writes `suspects.md`; `dynamic_hot` regenerates `hot.md` as a live bug-critical area with resolving `[[wikilinks]]`. | `obsidian/suspects.md`, `obsidian/hot.md`. |
| Supports **C3/C14** — architecture, God Node vs Hub, evidence tiers | `impact_report` quantifies God-Node betweenness + community cleanliness; orphans + suspects carry `Extracted`/`Inferred`/`Ambiguous` tiers. | `reports/IMPACT.md`, `reports/ORPHANS.md`. |
| Supports **C7** — before/after at knowledge level | `impact_report` is the graph-level before/after; the regenerated `hot.md` records how understanding shifted post-fix. | `reports/IMPACT.md`, vault diff. |
| Supports **C5** — guided agent | `as_agent_seed` feeds ranked suspects into the agent's suspect-selection state, so it reads highest-signal nodes first. | agent state log, `obsidian/suspects.md`. |

## 7. Verification (real, after the fix — NOT in the test suite)

```bash
uv run cosmos77-rev extensions          # ranks suspects, regenerates hot.md, lists orphans,
                                        # and diffs the before/after graph for the impact report.
```

Run after `prepare-target` → `graphify` (which snapshots `graph_before.json`) → `fix`. EXPECTED:
`suspects.md` ranks the true buggy node near the top; `IMPACT.md` shows the God-Node betweenness
dropping after the fix (the "what breaks if we change X" answer, measured). This human run proves C9
end-to-end; the unit suite never touches live git or the real graph.

## 8. Risks

- **Centrality vs proximity blend is arbitrary (MED).** A bad `proximity_weight` could bury the real
  suspect. *Mitigation:* the weight is config-driven and tested both ways; the suspect table shows both
  raw scores so a human can audit the ranking; the agent still reads `index.md`/`hot.md` first.
- **Graph-before snapshot missing (MED).** If `graphify` is not re-run pre-fix, the impact diff has no
  baseline. *Mitigation:* `graphify` writes `graph_before.json` by contract; `impact_report` raises
  loudly on a missing baseline rather than fabricating a delta.
- **Orphan misclassification (MED).** Calling a live adapter "dead code" is a graded error (God Node vs
  Hub discipline applied to orphans). *Mitigation:* the verification protocol defaults to `Ambiguous`,
  never asserts "dead" without a source scan, and tiers every verdict `Extracted`/`Inferred`/`Ambiguous`.
- **Git hook side effects (LOW).** An installed `post-commit` hook could surprise a collaborator.
  *Mitigation:* `install_hook` defaults to `false`; the hook is an opt-in stub documented in the README.
- **`networkx` cost on a large graph (LOW).** Betweenness is O(V·E). *Mitigation:* the `tqdm` target is
  small; if scaled, swap to `betweenness_centrality(k=...)` sampling — already behind one function.
- **Empty diff / disconnected test node (LOW).** Edge cases could yield empty pages. *Mitigation:* both
  produce explicit, honest "nothing here" output (tested) rather than silent empty files.
