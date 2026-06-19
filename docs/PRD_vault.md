# PRD — Obsidian Knowledge Vault (mechanism: `vault/`)

**Course:** UOH-RL07 — Vibe Coding & AI Agents (Dr. Yoram Segal) · **Assignment:** HW4 (COSMOS77-ex04)
**Maps to:** acceptance criterion **C2** (vault as an active knowledge space) · supports **C14** (evidence tiers), **C9** (suspect-ranking extension)
**Authors:** Abdallah Khaldi, Tasneem Natour · **Version:** 1.00 · **Status:** Specification

---

## 1. Purpose

This mechanism turns the Graphify knowledge model into an **active knowledge space**, not a file dump. The
vault is the medium through which the graph-guided agent (and a human reader) navigates an unfamiliar real
codebase (`tqdm`) **without reading it end-to-end**. It is deterministic and **contains NO LLM call** — it is a
pure, config-driven Markdown projection of the graph model plus the failing-test report.

The vault encodes the professor's retrieval protocol in prose and in link structure:
**"question → index → 2–3 pages → answer"**. The `index.md` is the **navigation hub**; `hot.md` is the
**bug-critical area** the agent loads first; one page per central component / Community / God Node carries the
local detail. Because retrieval routes through a few high-signal pages instead of the whole repository, the
vault is the structural reason the token ledger (C8/C15) comes out in our favour — it sidesteps **Context Rot**,
**Lost in the Middle**, and **Overflow** by construction.

A load-bearing distinction: **Graphify does NOT emit `hot.md`** — Graphify produces a generic Obsidian export.
`hot.md` is **our** contribution: god-nodes plus the failing test's neighborhood (functions/classes within `N`
hops of the failing test's targets). It is the focused-context page that makes guided retrieval concrete.

## 2. Inputs / Outputs

**Inputs (read-only; no network, no LLM):**

- A parsed **graph model** from `graphify/model.py`: typed `Node(id, kind, file)` and
  `Edge(src, dst, tier ∈ {extracted, inferred, ambiguous}, confidence)`, plus `centrality()`, `god_nodes()`,
  `communities()`, `neighbors(node)`. The **evidence tier** per edge is load-bearing for C14.
- The **failing-test descriptor** (from the report / `target/`): the test id and its target node ids — the
  seeds for the `hot.md` neighborhood.
- **Config** (`config/setup.json`, read via the Config loader, never hardcoded — rule 4): `paths.obsidian_dir`
  (default `obsidian/`), and vault knobs under a new `vault` block: `hot_hops` (N, default 2), `top_communities`,
  `top_suspects`, `top_neighbors_per_page`.

**Outputs (written under `paths.obsidian_dir`):**

- `index.md` — navigation hub: system overview, main Communities/subsystems, explicit navigation paths, the
  protocol in prose, and links to `[[hot]]`, top communities, and `[[suspects]]`.
- `hot.md` — god-nodes + the failing-test neighborhood (each node linked).
- one page **per central component / Community / God Node** — kind, file, `[[wikilinks]]` to neighbors, the
  evidence tier of key edges, a one-line role.
- `suspects.md` — ranked candidate buggy nodes (seeded here, refined by the Phase-9 centrality extension).
- `investigation.md`, `fix-process.md` — **templates** at build time (filled in Phase 7 by the agent run).
- Return value of `build_vault()`: a `VaultManifest` (output dir + list of written relative paths) so callers
  and tests can assert what was produced without re-scanning the disk blindly.

## 3. Module design (every `.py` ≤ 150 lines — rule 1)

Split by responsibility so each file stays small, testable, and single-purpose (rule 3 — composition, not
duplication). All live under `src/cosmos77_ex04/vault/`.

| File | Responsibility | Why it is separate |
|------|----------------|--------------------|
| `build.py` | **Orchestrator only.** Takes the model + test descriptor + config, calls `pages`/`links`/`wikilinks`, writes every file, returns the `VaultManifest`. Holds the page-selection policy (which nodes get pages). | Keeps the entry point thin; one place that decides *what* the vault contains. |
| `pages.py` | **Page bodies.** Pure functions `render_index(...)`, `render_hot(...)`, `render_node_page(...)`, `render_suspects(...)`, `render_templates(...)` → each returns a Markdown `str`. No file I/O. | Most lines live here; isolating rendering keeps `build.py` under the cap and makes bodies unit-testable as strings. |
| `links.py` | **Graph→link logic.** `select_pages(model)`, `hot_neighborhood(model, seeds, hops)`, `rank_suspects(model)` (seed ranking, later refined by the extension), `top_communities(model, k)`. Returns plain data (node-id lists), no Markdown. | Separates *what to link* (graph reasoning) from *how it reads* (prose) and *how it is encoded* (wikilinks). |
| `wikilinks.py` | **Encoding helpers.** `wikilink(node_id) -> "[[slug|label]]"`, `frontmatter(dict) -> YAML block`, `sanitize_filename(name)` (strip `/ \ : * ? " < > |`), `slug(node_id)`. Guarantees no orphan index (every page links back). | The one place filename safety + YAML + link syntax is defined, so it cannot drift across pages. |
| `__init__.py` | Re-export `build_vault` impl and the `VaultManifest` dataclass for the SDK. | Stable import surface. |

**Splitting rationale.** `build.py` would exceed 150 lines if it also rendered every page body, so rendering
moves to `pages.py` and graph reasoning to `links.py`; `wikilinks.py` holds the leaf helpers shared by all of
them. If `pages.py` itself approaches the cap, split per-page-type into `pages.py` + `pages_node.py`.

**Determinism.** All ordering (communities, suspects, neighbors) is **sorted by a stable key**
(centrality desc, then node id asc) so two builds of the same model are byte-identical — required for golden-file
tests and an honest diff in C7. No `set` iteration leaks into output; no timestamps in committed pages.

## 4. Public SDK API

All business logic routes through the single `class SDK` (rule 2 / ADR-006). The CLI sub-command `vault` maps
1:1 to this method; no logic lives in the CLI.

```python
class SDK:
    def build_vault(
        self,
        model: GraphModel | None = None,      # default: load from artifacts/graph.json via graphify/model.py
        *,
        failing_test: FailingTest | None = None,  # default: read from the prepared target / report
        out_dir: Path | None = None,          # default: config paths.obsidian_dir
    ) -> VaultManifest:
        """Project the graph model into an active Obsidian vault (index/hot/pages/suspects/templates).

        Deterministic, no LLM, no network. Returns the manifest of written files so callers and
        tests can assert structure. Encodes the 'question -> index -> 2-3 pages -> answer' protocol.
        """
```

Supporting public types (in `vault/__init__.py`): `VaultManifest(out_dir: Path, files: list[Path])`. Inputs
`GraphModel` / `FailingTest` are owned by `graphify/` and `target/` respectively; the vault only consumes them.

## 5. Test plan (TDD, red → green → refactor — rule 6; all I/O deterministic, no live calls)

Tests run against a **small in-memory fixture model** (a `conftest` factory: ~6 nodes spanning ≥2 communities,
one god-node, one failing-test seed, edges across all three tiers). They write into `tmp_path`.

1. **`index.md` is a hub.** Build → assert `index.md` exists and links to `[[hot]]`, to `[[suspects]]`, and to
   each top-community page; assert the prose contains the protocol string `question → index → 2-3 pages → answer`.
2. **`hot.md` content.** Assert every god-node id appears and is linked; assert exactly the nodes within `N`
   hops of the failing-test seeds are present (parametrize `N=1` and `N=2`); assert a non-neighbor node is absent.
3. **One page per selected node.** Assert a `.md` file exists for each node returned by `select_pages`; each
   page shows kind, file, a one-line role, neighbor `[[wikilinks]]`, and the **evidence tier** of its key edges.
4. **All wikilinks resolve.** Parse every `[[...]]` across all generated files; assert each target resolves to an
   existing `.md` in the output dir (no dangling links) — the core C2 guarantee.
5. **Filenames sanitized.** Feed a node id containing `/ \ : * ? " < > |`; assert the written filename strips
   every forbidden character and the wikilink to it still resolves (round-trip via `slug`/`sanitize_filename`).
6. **No orphan index + templates.** Assert `index.md` is reachable from `hot.md`/`suspects.md` (back-link) and
   that `investigation.md` / `fix-process.md` are written as fill-in templates with the expected headings.
7. **Determinism.** Build twice into two dirs; assert byte-for-byte identical output (stable ordering).
8. **Suspects ranking seed.** Assert `suspects.md` lists candidates ordered by the seed rank and is the hook the
   Phase-9 centrality extension refines (no regression in contract).

Coverage target for the package ≥ 85% (rule 7); `ruff` clean (rule 8); line-cap clean (rule 1).

## 6. Acceptance-criteria mapping

| Criterion | How this mechanism satisfies it |
|-----------|---------------------------------|
| **C2** (vault as active knowledge space) | `build.py` generates `index.md` (hub) + `hot.md` (bug-critical) + linked pages + `suspects.md` + templates; all `[[wikilinks]]` resolve (Test 4); navigation protocol is encoded in prose and link structure. **Primary owner of C2.** |
| **C14** (evidence tiers) | Each node page and `hot.md` surface the `Extracted` / `Inferred` / `Ambiguous` tier of key edges (Test 3); god-nodes are labelled distinctly from healthy Hubs. |
| **C9** (extension hook) | `suspects.md` + `links.rank_suspects` provide the seam the Phase-9 centrality suspect-ranking extension refines (Test 8). |
| **C7** (knowledge-level before/after) | Deterministic, diffable pages (Test 7) let us record the vault delta (pages/links/insights added) once the agent fills `investigation.md` / `fix-process.md`. |
| Supports **C8/C15** | By making focused retrieval (`index → hot → 2–3 pages`) the path of least resistance, the vault is the structural cause of the measured token saving the ledger reports. |

## 7. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Orphan / dangling wikilinks** — a link points at a page that was never written. | Medium | High | `wikilinks.py` is the single link encoder; Test 4 asserts every `[[link]]` resolves to an existing file, Test 6 asserts no orphan index. Build fails the test, not the user. |
| **Filename collisions / illegal chars** from node ids with `/ : * …`. | Medium | Medium | `sanitize_filename` + `slug` strip forbidden chars deterministically; collisions disambiguated by suffix; round-trip asserted (Test 5). |
| **`build.py` exceeds the 150-line cap.** | High | Low | Rendering → `pages.py`, graph reasoning → `links.py`, encoding → `wikilinks.py`; orchestrator stays thin. `check_line_cap.py` in CI catches regressions. |
| **`hot.md` neighborhood too large/small** (N mis-tuned) → noise or missing the bug area. | Medium | Medium | `hot_hops` is config-driven (default 2), not hardcoded; Test 2 parametrizes N; suspects page provides a ranked fallback. |
| **Non-determinism** (set iteration / timestamps) breaks golden tests and C7 diffs. | Medium | Medium | Stable sort keys everywhere; no timestamps in committed pages; Test 7 enforces byte-identical rebuilds. |
| **Coupling to Graphify's exact JSON shape.** | Medium | Medium | Vault consumes only the typed `GraphModel` from `graphify/model.py`, not raw `graph.json`; the DIY `ast`+`networkx` fallback yields the same model, so the vault is unaffected. |
| **Mislabeling a healthy Hub as a God Node** in `hot.md`. | Low | Medium | God-node selection comes from `model.god_nodes()` (centrality + fan-in heuristic), reused from `reveng/godnodes.py` — one definition, not a vault-local guess (rule 3). |

---

*End of PRD. See `docs/PRD.md` (FR-02 → C2), `docs/PLAN.md` §1.2 (`vault/` container) and ADR-004 (graph-first
protocol the vault feeds), and `CLAUDE_CODE_PLAYBOOK.md` §1.5 for the binding C1–C15 spec.*
