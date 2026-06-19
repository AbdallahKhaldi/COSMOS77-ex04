# PRD — Mechanism: Run Graphify + Parse `graph.json`

**Course:** Orchestration of AI Agents (203.3763), Dr. Yoram Segal · **Assignment:** HW4
**Project:** COSMOS77-ex04 · **Mechanism owner package:** `src/cosmos77_ex04/graphify/`
**Maps to acceptance criteria:** **C1** (Graphify run → `graph.json` + `GRAPH_REPORT.md` + `graph.html`)
and **C14** (Evidence tiers Extracted/Inferred/Ambiguous; God Node vs healthy Hub).
**Version:** 1.00 · **Status:** Specification (Phase 1, for Phase 3 build).

---

## 1. Purpose

This mechanism is the **first stage** of the `cosmos77-rev` pipeline: it turns the buggy target
project (default **`tqdm`**, checked out under `data/target/`) into a **knowledge graph** and a
**queryable model** that every downstream stage (vault, diagrams, agent, token comparison) consumes.

It does two jobs:

1. **Run Graphify** — invoke the `graphify <path> --obsidian --wiki` CLI on the target source,
   producing `graphify-out/{graph.json, GRAPH_REPORT.md, graph.html, obsidian/, wiki/index.md}`,
   then persist the durable evidence into `artifacts/` and seed our Obsidian vault from Graphify's
   `obsidian/` folder.
2. **Parse `graph.json`** (NetworkX `node_link_data`) into **typed objects** with **evidence tiers**
   and graph-theory helpers (Centrality, Community, neighbors, God Nodes) so the rest of the project
   navigates the code by **guided retrieval**, never by linear raw-file reading.

Graphify's AST extraction is near-zero token cost; only its *semantic* extraction touches the LLM —
this stage is therefore the cheap, high-signal foundation the whole token thesis rests on.

---

## 2. Inputs / Outputs

### Inputs
- **Target source path** — `config.target.workdir` (default `data/target/`), the checked-out
  BugsInPy project source tree (gitignored; produced by the Phase 2 prepare-target harness).
- **Config** — `config/setup.json`: `graphify.out_dir` (default `graphify-out`),
  `graphify.obsidian` (`true` → `--obsidian`), `graphify.wiki` (`true` → `--wiki`),
  `paths.{artifacts_dir, obsidian_dir}`.
- **Graphify CLI** — `graphify` (PyPI package `graphifyy`, double-y), a SYSTEM prerequisite.

### Outputs (persisted)
- `artifacts/graph.json` — committed; the canonical graph (NetworkX node_link).
- `artifacts/GRAPH_REPORT.md` — committed; Graphify's prose report (god-nodes, surprising edges,
  suggested questions).
- `artifacts/graph.html` — interactive view (may be gitignored if large; copy is best-effort).
- `obsidian/` — seeded from Graphify's `obsidian/` folder (Phase 4 extends it with `index.md`/`hot.md`).

### Outputs (in-memory, returned by the SDK)
- A `Graph` model object exposing `nodes`, `edges`, `communities`, and helpers
  (`centrality`, `god_nodes`, `communities`, `neighbors`).
- A `ReportSummary` object: structured god-nodes, surprising/ambiguous edges, suggested questions.

---

## 3. Module design (every `.py` ≤ 150 lines)

```
src/cosmos77_ex04/graphify/
├── __init__.py        # re-exports: run_graphify_cli, Graph, Node, Edge, Community, ReportSummary
├── run.py             # invoke CLI, persist artifacts, seed vault, DIY fallback dispatch  (≤120)
├── model.py           # parse node_link_data → Node/Edge/Community + graph helpers          (≤150)
├── report.py          # parse GRAPH_REPORT.md → ReportSummary                                (≤100)
└── fallback.py        # DIY ast+networkx builder → graph.json (ADR-fallback)                 (≤150)
```

**Split policy (CLAUDE.md rules 1 & 3).** `model.py` carries the dataclasses **and** the
graph-theory helpers; if it approaches the 150-line cap, split the pure graph algorithms into
`graphify/metrics.py` (`centrality`, `god_nodes`, `communities`) so `model.py` keeps only the
typed objects + `from_node_link()` constructor. `fallback.py` is a separate file (not inlined into
`run.py`) because the AST walker is reused logic and would blow `run.py`'s budget. No duplication:
tier-labelling and confidence thresholds live as named constants in one place
(`graphify/_tiers.py` or `model.py` module-level), referenced by `model.py`, `report.py`, and
`fallback.py`.

### 3.1 `run.py` — orchestration (no business logic leaks)
- `run_graphify_cli(target, out_dir, *, obsidian, wiki, runner=subprocess.run) -> Path`:
  build the argv `["graphify", str(target), "--obsidian", "--wiki"]` (flags gated by config),
  invoke via an **injected `runner`** (so tests mock it — CLAUDE.md rule 6), and return the
  `out_dir` path. Raises `GraphifyError` on non-zero exit so the SDK can choose the fallback.
- `persist_artifacts(out_dir, artifacts_dir, obsidian_dir) -> None`: copy `graph.json`,
  `GRAPH_REPORT.md`, `graph.html` into `artifacts/`; copy `out_dir/obsidian/` into `obsidian/`
  as the **seed** of our vault (idempotent; best-effort for `graph.html`).
- `build_graph_with_fallback(target, out_dir, runner) -> Path`: try the CLI; on `GraphifyError`
  or `FileNotFoundError` (CLI not installed) delegate to `fallback.build(target, out_dir)`.

### 3.2 `model.py` — the queryable graph (C14 lives here)
- `@dataclass(frozen=True) Node(id: str, kind: str, file: str)` — `kind ∈ {function, class, module}`.
- `@dataclass(frozen=True) Edge(src: str, dst: str, tier: Tier, confidence: float)` —
  `Tier = Literal["extracted", "inferred", "ambiguous"]`.
- `@dataclass(frozen=True) Community(id: int, members: tuple[str, ...])`.
- `class Graph`: holds `nodes`, `edges`, lazy `networkx.DiGraph`; constructed by
  `Graph.from_node_link(data: dict) -> Graph`.
- Helpers:
  - `centrality(kind="betweenness"|"degree") -> dict[str, float]` (via `networkx`).
  - `god_nodes(top_k, min_degree) -> list[Node]` — high-centrality + high fan-in/out candidates.
  - `communities() -> list[Community]` — `networkx` community detection (greedy modularity).
  - `neighbors(node_id, hops=1) -> set[str]` — ego graph for the agent's focused context.

### 3.3 `report.py` — prose → structure
- `parse_report(text: str) -> ReportSummary` with regex/section scanning over the Markdown
  headings Graphify emits (`## God Nodes`, `## Surprising Edges`, `## Suggested Questions`).
- `@dataclass ReportSummary(god_nodes, surprising_edges, suggested_questions)`; tolerant of
  missing sections (returns empty lists, never raises) so a thin report degrades gracefully.

### 3.4 `fallback.py` — DIY builder (documented ADR fallback)
- `build(target, out_dir) -> Path`: walk `*.py` with `ast`, emit module/class/function nodes and
  `import`/`call`/`inherits` edges into a `networkx.DiGraph`, write
  `node_link_data` to `out_dir/graph.json` and a minimal `GRAPH_REPORT.md`. All such edges are
  tagged **`extracted`** tier with `confidence=1.0` for the structural ones the AST proves and
  **`inferred`** for resolved-by-name calls (see §4).

---

## 4. Evidence tiers — Extracted / Inferred / Ambiguous (C14)

Every `Edge` carries a `tier` that states **how much we trust the relationship**, so downstream
reasoning (and the agent) can weight evidence honestly:

| Tier | Meaning | Source signal | Typical `confidence` |
|------|---------|---------------|----------------------|
| **Extracted** | Proven by the AST/import graph; the relationship is in the syntax. | `import X`, direct `inherits`, a call to a locally-defined symbol. | `≥ 0.9` |
| **Inferred** | Resolved by name/heuristic; very likely but not syntactically certain. | call resolved by matching name across modules; duck-typed usage. | `0.5–0.9` |
| **Ambiguous** | Multiple plausible targets or weak signal; flag, don't trust blindly. | overloaded names, dynamic dispatch, monkey-patching. | `< 0.5` |

`model.py` reads the per-edge `tier`/`confidence` straight from `graph.json` when Graphify provides
them; when absent, it derives the tier from a confidence threshold (constants in one place). This is
the **C14 discipline**: an *Ambiguous* edge is a hypothesis to verify, an *Extracted* edge is a fact.

**God Node vs healthy Hub (also C14).** `god_nodes()` surfaces high-**Centrality** nodes; the
*diagnosis* (is this a healthy **Hub** that legitimately coordinates, or a **God Node** bottleneck
that does too much?) is applied here by combining centrality with fan-in/out and **Community** spread
— a Hub serves one community; a God Node bridges many and concentrates responsibility.

---

## 5. Public SDK API

All business logic flows through the single `class SDK` (`src/cosmos77_ex04/sdk/sdk.py`,
CLAUDE.md rule 2). This mechanism contributes:

```python
def run_graphify(self) -> GraphifyResult:
    """Run Graphify on the configured target and persist artifacts (C1).

    Reads config.target.workdir + config.graphify.*, invokes the graphify CLI
    (graph-guided foundation), copies graph.json / GRAPH_REPORT.md / graph.html
    into artifacts/, seeds obsidian/ from graphify's obsidian/ folder, and parses
    graph.json + GRAPH_REPORT.md into a queryable model. Falls back to the DIY
    ast+networkx builder if the CLI is unavailable (ADR-fallback), so graph.json
    is ALWAYS produced. Returns the parsed Graph + ReportSummary + artifact paths.
    """
```

`GraphifyResult` (typed): `graph: Graph`, `report: ReportSummary`,
`artifacts: dict[str, Path]` (`graph_json`, `report_md`, `graph_html`), `used_fallback: bool`.
Type hints on every public signature; no bare `Any` (rule 16). The CLI surface
`uv run cosmos77-rev graphify` calls `SDK.run_graphify()` and nothing else.

---

## 6. Test plan (Graphify CLI MOCKED — no live calls)

TDD red→green→refactor; ALL subprocess/CLI/filesystem-external I/O mocked (rules 6 & 17);
deterministic (`random` seeded in `conftest.py`). Fixtures live under `tests/fixtures/graphify/`.

**Fixtures**
- `graph.json` — small node_link graph: ~6 nodes (mix of module/class/function), edges across all
  three tiers (one `extracted`, one `inferred`, one `ambiguous`) with explicit `confidence`.
- `GRAPH_REPORT.md` — minimal report with `## God Nodes`, `## Surprising Edges`,
  `## Suggested Questions` sections (plus one missing-section variant for graceful-degradation).

**`tests/unit/test_graphify_model.py`**
- parses fixture `graph.json` into the right count of `Node`/`Edge`; asserts each edge's `tier`
  and `confidence` round-trip correctly (happy path for C14).
- `centrality("degree")` and `centrality("betweenness")` return finite, correctly-ranked scores on
  the fixture; the known central node ranks first.
- `god_nodes(top_k=2)` returns the seeded high-centrality node(s); a leaf node is never a god-node.
- `communities()` partitions every node exactly once; `neighbors(n, hops=1)` returns the seeded ego set.
- **Error path:** malformed `graph.json` (missing `nodes`) raises a typed `GraphParseError`.

**`tests/unit/test_graphify_report.py`**
- `parse_report` extracts the seeded god-nodes / surprising (ambiguous) edges / suggested questions.
- missing-section fixture → empty lists, no exception (graceful degradation).

**`tests/unit/test_graphify_run.py`**
- `run_graphify_cli` with a **mock `runner`** asserts the exact argv (`graphify <path> --obsidian
  --wiki`) and that flags toggle off when config disables them.
- `persist_artifacts` (against `tmp_path`) copies the three artifacts and seeds `obsidian/`.
- **Fallback:** mock `runner` raising `FileNotFoundError`/non-zero → `build_graph_with_fallback`
  calls `fallback.build`, which (on a tiny `tmp_path` `.py` tree) writes a valid `graph.json` that
  `Graph.from_node_link` can parse — proving graph.json is always produced.

**`tests/integration/test_sdk_run_graphify.py`**
- `SDK.run_graphify()` end-to-end with the CLI mocked + fixtures wired through config; asserts a
  populated `GraphifyResult` and that `artifacts/graph.json` exists. No live `graphify`/network call.

Coverage ≥ 85% for the package; `ruff check` zero; line-cap clean.

---

## 7. Acceptance-criteria mapping

| Criterion | How this mechanism satisfies it | Verifying test/artifact |
|-----------|---------------------------------|-------------------------|
| **C1** | `run_graphify_cli` produces `graph.json` + `GRAPH_REPORT.md` + `graph.html`; `persist_artifacts` commits them to `artifacts/`. | `test_graphify_run.py`, `artifacts/graph.json` |
| **C1 (fallback)** | DIY `ast`+`networkx` builder guarantees `graph.json` even if the CLI fails (ADR). | fallback test; `used_fallback` flag |
| **C14 (tiers)** | `Edge.tier ∈ {extracted, inferred, ambiguous}` parsed/derived from confidence. | `test_graphify_model.py` |
| **C14 (God Node vs Hub)** | `god_nodes()` + centrality + community spread enable the Hub/God-Node diagnosis. | `test_graphify_model.py` |
| **C11** | Outputs land in `artifacts/` and seed `obsidian/`, honoring repo structure. | integration test |

The parsed `Graph` + `ReportSummary` are the contract consumed by `reveng/` (C3/C4),
`vault/` (C2), and `agent/` (C5) — keeping every later stage on **guided retrieval**.

---

## 8. Risks & mitigations

- **Graphify CLI unavailable / version drift / non-zero exit.** *Mitigation:* the documented
  **ADR-fallback** DIY `ast`+`networkx` builder (`fallback.py`) — graph.json is always produced;
  `used_fallback` is recorded so reports stay honest about provenance.
- **`graph.json` schema differs from assumed node_link shape.** *Mitigation:* tolerant
  `from_node_link` with a typed `GraphParseError`; tier/confidence defaulted from constants when fields
  are absent; tested against a fixture, not a live graph.
- **150-line cap pressure in `model.py`.** *Mitigation:* pre-planned split of graph algorithms into
  `metrics.py` (§3); helpers are pure functions, easy to relocate without API change.
- **Semantic-extraction token cost / time on a larger target.** *Mitigation:* AST extraction is the
  bulk and near-zero cost; semantic edges are a small, bounded share — noted honestly in the token
  ledger; this stage is run once and its artifacts committed.
- **Mock drift (tests pass but real CLI argv is wrong).** *Mitigation:* argv asserted explicitly in
  `test_graphify_run.py`; a manual Phase 3 verification (`uv run cosmos77-rev graphify`) runs the real
  CLI once outside the suite to confirm the contract.
- **Centrality on a disconnected / tiny graph (edge cases).** *Mitigation:* `networkx` handles
  disconnected components; tests include a leaf node and assert sane (non-crashing) scores.
