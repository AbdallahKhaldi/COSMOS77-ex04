# PRD — `reveng` — Reverse-Engineering Diagrams (Block + OOP) + God-Node Analysis

**Course:** Orchestration of AI Agents (203.3763), Dr. Yoram Segal · **Assignment:** HW4 (Phase 5)
**Authors:** Abdallah Khaldi, Tasneem Natour · **Version:** 1.00 · **Status:** Specification (Phase 1)
**Maps to:** **C3** (architectural block diagram), **C4** (OOP schema), **C14** (evidence tiers + God Node vs healthy Hub).
**Package:** `src/cosmos77_ex04/reveng/` · **SDK entry:** `SDK.extract_diagrams()`

## 1. Purpose

This mechanism produces the two **mandatory illustrations** of HW4 as *engineering understanding
extracted FROM THE GRAPH* — never as a folder listing. From the Graphify model (`graph.json`) it
reads the **actual architecture**: it detects **Communities** (subsystems), **Hubs**, and the
**Bridge** nodes that wire subsystems together, then emits an architectural **block diagram**. From
the target source (`ast` over `data/target`) plus the model it extracts classes, inheritance,
composition, and usage relations into an **OOP schema**. Finally it ranks nodes by **Centrality**
(betweenness/degree) and applies the diagnosis questions to separate a healthy **Hub** from a
bottleneck **God Node**.

The reading discipline is **macro → meso → micro**: first the communities (macro), then the bridges
that connect them (meso), then the classes/God-Node internals (micro). This is the deterministic,
**NO-LLM** counterpart to the agent: Graphify's AST extraction is near-zero token cost, and every
diagram here is computed in plain Python so the deliverable is reproducible and free of LLM
non-determinism. Output is committed Mermaid + rendered PNG plus a written `reports/ARCHITECTURE.md`.

## 2. Inputs / Outputs

**Inputs**
- `artifacts/graph.json` — the Graphify NetworkX `node_link` model (from Phase 3): nodes
  (functions/classes/modules), edges carrying an **evidence tier** (`Extracted` / `Inferred` /
  `Ambiguous`), communities, and centrality. Consumed via the `graphify.model` objects, never re-parsed.
- `data/target/` source tree — the checked-out buggy `tqdm` (Phase 2), read by `ast` for the OOP schema.
- `config/setup.json` — `paths.artifacts_dir`, `paths.reports_dir`; a new `reveng` block (§3) for
  thresholds (top-K centrality, hops, render toggle). NO hardcoded paths or thresholds (rule 4).
- The failing test's targets (from the target harness) — used to mark the bug-critical community.

**Outputs**
- `artifacts/block_diagram.mmd` — Mermaid `flowchart` of communities → bridges → main flow.
- `artifacts/block_diagram.png` — rendered PNG of the block diagram.
- `artifacts/oop_schema.mmd` — Mermaid `classDiagram` of classes/inheritance/composition/usage.
- `artifacts/oop_schema.png` — rendered PNG of the OOP schema.
- `reports/ARCHITECTURE.md` — the written findings: macro→meso→micro walkthrough, the Centrality
  ranking table, the **Hub vs God Node** classification per high-centrality node with the diagnosis
  answers and the evidence tier of each load-bearing edge, and BOTH diagrams embedded.
- Return value of `extract_diagrams()` — a typed `DiagramResult` (paths + the classification list)
  for the SDK/CLI and the README.

## 3. Configuration (added to `config/setup.json`, read via Config loader)

```json
"reveng": {
  "top_k_central": 8,
  "godnode_betweenness_pct": 0.85,
  "test_neighborhood_hops": 2,
  "render_png": true,
  "block_diagram": "block_diagram",
  "oop_schema": "oop_schema"
}
```

`render_png` lets CI run without a Mermaid renderer (emit `.mmd`, skip `.png`); thresholds tune the
God-Node classifier. All values are config — none are literals in code.

## 4. Module design (files ≤ 150 lines — how we split)

The package is split so each file is single-responsibility and well under the 150-line cap. Shared
helpers (community/bridge extraction, Mermaid escaping, PNG render shell-out) live in one module so
no logic is duplicated across the three deliverables (rule 3).

| File | Responsibility | ~Lines |
|------|----------------|-------:|
| `reveng/__init__.py` | Re-export `extract_diagrams`, `DiagramResult`, `NodeRole`. | ~15 |
| `reveng/types.py` | `@dataclass` types: `Subsystem`, `Bridge`, `ClassInfo`, `NodeRole`, `DiagramResult`. Type hints only, no logic. | ~60 |
| `reveng/topology.py` | Read the model: `communities()` → subsystems, `hubs()`, `bridges()` (edges whose endpoints sit in different communities). The macro→meso layer, reused by block + godnodes. | ~120 |
| `reveng/block_diagram.py` | Build the Mermaid `flowchart`: one `subgraph` per community, edges = bridges, annotate the main inter-subsystem flow; mark the bug-critical community. Calls `render`. | ~140 |
| `reveng/oop_schema.py` | `ast` visitor over `data/target`: `ClassDef` → name/bases (**inheritance**), attribute annotations & instantiations (**composition**), method calls into other classes (**usage**); emit Mermaid `classDiagram`. | ~150 |
| `reveng/godnodes.py` | Rank by **Centrality** (betweenness/degree); apply the three diagnosis questions; label each node `HUB` or `GOD_NODE`; render `reports/ARCHITECTURE.md` from a template with both diagrams embedded. | ~145 |
| `reveng/render.py` | Pure helper: write `.mmd`, escape Mermaid labels, shell out to the Mermaid CLI for PNG (mocked in tests), respect `render_png`. Shared by block + oop. | ~80 |

If `oop_schema.py` approaches the cap, the `ast.NodeVisitor` subclass is extracted to
`reveng/ast_visitor.py` and `oop_schema.py` keeps only Mermaid assembly.

### God-Node diagnosis (the C14 heart)
A high-centrality node is **not automatically a God Node**. `godnodes.py` answers three questions
per node and records the answers in `ARCHITECTURE.md`:
1. **Do alternatives exist?** Multiple independent paths through the node ⇒ healthy **Hub**;
   single choke point ⇒ leans **God Node**.
2. **Is it a mandatory path?** If every Community must traverse it to reach another, it is a
   structural bottleneck (**God Node**).
3. **Is there hidden over-coupling?** Unusually high degree AND high betweenness AND fan-in from
   many communities ⇒ **God Node**; a high-degree node confined to one community is a local **Hub**.

A node is labelled `GOD_NODE` when betweenness exceeds `godnode_betweenness_pct` of the max **and**
at least two diagnosis answers indicate a bottleneck; otherwise `HUB`. The evidence tier of the
edges feeding the decision is reported, so an `Ambiguous`-tier-heavy God Node is flagged as a
tentative finding rather than asserted.

## 5. Public SDK API

All callers (CLI `cosmos77-rev diagrams`, README pipeline) go through the single `class SDK` (rule 2):

```python
def extract_diagrams(self) -> DiagramResult:
    """Extract the block diagram, OOP schema, and God-Node analysis from the
    Graphify model + target AST, render Mermaid + PNG, and write reports/ARCHITECTURE.md.

    Reads graph.json (artifacts) and data/target source; applies macro->meso->micro
    (communities -> bridges -> classes/god-nodes). Pure, deterministic, no LLM.

    Returns:
        DiagramResult: paths to the .mmd/.png/ARCHITECTURE.md artifacts plus the
        per-node Hub/God-Node classification (NodeRole list) and the evidence tier
        of each load-bearing edge.

    Raises:
        FileNotFoundError: if artifacts/graph.json is absent (run `graphify` first).
    """
```

`DiagramResult` fields: `block_mmd`, `block_png`, `oop_mmd`, `oop_png`, `architecture_md`,
`roles: list[NodeRole]`. Each `NodeRole` carries `node_id`, `kind`, `centrality`, `label`
(`HUB`/`GOD_NODE`), `diagnosis: dict[str, bool]`, and `evidence_tier`.

## 6. Test plan (TDD — red → green → refactor; deterministic, no I/O)

Fixtures live under `tests/unit/fixtures/`: a small `graph.json` with two clear communities joined
by one bridge node, and a `sample.py` with `class B(A)` plus a composition/usage relation. The
Mermaid PNG render is mocked (`pytest-mock`); no live subprocess.

| Test | Asserts | Path |
|------|---------|------|
| `test_block_diagram_emits_valid_flowchart` | Output starts with `flowchart`, has one `subgraph` per fixture community, and an edge for the bridge between them. | happy |
| `test_block_diagram_annotates_main_flow` | The inter-subsystem main flow is labelled; bug-critical community is marked. | happy |
| `test_block_diagram_missing_graph_raises` | `extract_diagrams` on absent `graph.json` raises `FileNotFoundError`. | error |
| `test_oop_extracts_classes_and_inheritance` | From `sample.py`, output is a `classDiagram` containing `A`, `B`, and the `A <|-- B` inheritance edge. | happy |
| `test_oop_extracts_composition_and_usage` | Composition (`*--`) and usage (`..>`) relations from the fixture appear. | happy |
| `test_oop_handles_unparseable_file` | A syntactically broken `.py` is skipped with a warning, not a crash. | error |
| `test_godnodes_ranks_by_centrality` | Ranking order matches the fixture's known betweenness/degree order. | happy |
| `test_godnodes_labels_hub_vs_godnode` | The single-choke-point bridge node → `GOD_NODE`; a high-degree intra-community node → `HUB`. | happy |
| `test_godnodes_reports_evidence_tier` | `ARCHITECTURE.md` records the `Extracted/Inferred/Ambiguous` tier of each load-bearing edge. | happy |
| `test_render_respects_render_png_false` | With `render_png=false`, `.mmd` is written and PNG render is NOT called. | error |

Coverage target for the package ≥ 85% (rule 7); `ruff check` zero; every public function gets a
happy-path and an error-path test before implementation.

## 7. Acceptance-criteria mapping

| Criterion | Satisfied by | Evidence artifact |
|-----------|--------------|-------------------|
| **C3** — architectural block diagram from the graph (communities/hubs/bridges + flow), not a folder listing | `topology.py` + `block_diagram.py` | `artifacts/block_diagram.{mmd,png}`, `reports/ARCHITECTURE.md` |
| **C4** — OOP schema (classes, inheritance, composition, usage) extracted from code | `oop_schema.py` (`ast`) | `artifacts/oop_schema.{mmd,png}` |
| **C14** — evidence tiers + God Node vs healthy Hub distinction | `godnodes.py` diagnosis questions + tier reporting | `reports/ARCHITECTURE.md` classification table |

Supports research questions (a) actual architecture, (b) most-central components, (c) God Nodes /
complexity hotspots, and (d) extracting block + OOP schemas from sparse docs (PRD.md §3).

## 8. Risks & mitigations

- **Block diagram degenerates into a folder tree (C3 fail).** Mitigation: subsystems come from the
  model's `communities()`, edges come from `bridges()` (cross-community edges) — never from the
  directory layout; a test asserts the bridge edge exists between fixture communities.
- **Mermaid renderer absent in CI.** Mitigation: `render_png` config gates the PNG; `.mmd` is always
  produced and committed, render is mocked in tests, and the README documents the renderer prereq.
- **AST misses dynamic composition/usage** (attributes set outside `__init__`, duck typing).
  Mitigation: report only statically `Extracted` relations as solid edges; heuristic usage edges are
  labelled `Inferred`; ambiguous cases are dropped, keeping the schema honest (C14).
- **Over-calling nodes "God Nodes."** Mitigation: the two-of-three diagnosis gate plus the betweenness
  percentile threshold prevent labelling every Hub a God Node; tentative (Ambiguous-tier) findings
  are flagged, not asserted.
- **150-line cap pressure on `oop_schema.py`/`godnodes.py`.** Mitigation: the `ast` visitor and the
  Mermaid/report templating are pre-factored into `ast_visitor.py` / `render.py` splits noted in §4.
- **Graphify model shape drift.** Mitigation: `reveng` depends only on the typed `graphify.model`
  objects, not raw `graph.json` keys, so an upstream schema change is absorbed in one place.
