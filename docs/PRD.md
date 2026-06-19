# PRD — COSMOS77-ex04: Token-Efficient Graph-Guided Reverse Engineering & Debugging

**Course:** UOH-RL07 — Vibe Coding & AI Agents (Dr. Yoram Segal) · **Assignment:** HW4
**Authors:** Abdallah Khaldi, Tasneem Natour · **Version:** 1.00 · **Status:** Specification (Phase 1)

## 1. Problem statement (the thesis we must prove)

A real codebase is too large to read end-to-end into an LLM context window, and reading it
naively does not just cost tokens — it degrades the answer. This project takes a **small but
REAL** buggy BugsInPy Python project (default **`tqdm`**), reverse-engineers it with the
**Graphify** CLI into a knowledge graph (`graph.json`, `GRAPH_REPORT.md`) plus an **Obsidian**
vault (`index.md` navigation hub + `hot.md` bug-critical area + linked investigation pages), and
then runs a **graph-guided LangGraph agent** on **Google Gemini `gemini-2.5-flash`**. The agent
consults the graph and the vault FIRST, ranks suspects, and requests ONLY the targeted source of
the top suspects before naming a root cause and fixing a real bug (the BugsInPy failing test goes
**FAIL → PASS**). The single claim we must defend with **honest, MEASURED** numbers — not the
folklore "70–95%" — is: **graph-guided, focused-context work beats naive raw-code reading**, on
the SAME bug, measured by tokens consumed, files/units read, iterations, and quality/speed to the
root cause. A measured 35% saving with a clear methodology beats a fabricated 95%.

## 2. Context — UOH-RL07 Lecture 07 concepts

The professor's Lecture 07 names the failure modes that make naive raw-file reading degrade on
real codebases, and the retrieval discipline that fixes them:

- **Overflow vs Context Rot.** *Overflow* is the hard wall — you exceed the context window and
  content is truncated. *Context Rot* is subtler and worse: the window is not full, yet answer
  quality **decays as you stuff in more weakly-relevant tokens**. Dumping ten raw source files to
  "be safe" buys Context Rot, not safety.
- **Lost in the Middle.** Attention is U-shaped: a model recalls the **start** and **end** of a
  long context well, but facts buried in the **middle** are systematically missed. The one
  function that actually holds the bug, sitting on line 4,000 of a 12,000-token dump, is exactly
  where the model stops paying attention.
- **Signal-to-noise.** Every irrelevant file lowers the signal-to-noise ratio of the context. The
  goal is not "more context" but **higher-signal context**: a few load-bearing pages.
- **Graph-guided retrieval.** Instead of linear reading, we navigate a graph of the code
  (functions/classes/modules as nodes; calls/imports/inheritance as edges). **Centrality**
  surfaces what matters, **Community** detection reveals subsystems, and **Bridge** nodes expose
  the seams between them — so retrieval is *guided* rather than exhaustive.
- **"question → index → 2-3 pages → answer".** The vault's `index.md` is a **navigation hub**:
  any investigative question routes through the index, to 2-3 high-signal pages, to the answer —
  never through the whole repository. This is the concrete protocol that keeps signal-to-noise
  high and side-steps both Overflow and Lost in the Middle.

Naive raw-file reading fails on real codebases because it conflates *availability* with
*relevance*: it pays the full token cost of every file, dilutes signal, and pushes the decisive
lines into the un-attended middle. Graph-guided retrieval pays for **a few right pages** instead.

## 3. Research questions (spec §4) — requirements the work MUST answer

Each row is a deliverable obligation, answered across README, `reports/`, and the Obsidian vault.

| # | Research question | How the work answers it | Primary evidence |
|---|---|---|---|
| (a) | What is the **actual architecture** of the target? | Communities/hubs/bridges read from `graph.json`, not the folder tree | Block diagram (C3), `reports/ARCHITECTURE.md` |
| (b) | Which are the **most-central components**? | Betweenness/degree **Centrality** ranking over the graph | `reports/ARCHITECTURE.md`, `obsidian/` pages |
| (c) | Where are the **complexity hotspots / God Nodes**? | Diagnose high-centrality nodes: healthy **Hub** vs bottleneck **God Node** | `godnodes.py` output, `hot.md` |
| (d) | How do we extract a **block diagram + OOP schema** from sparse docs? | Graph + AST extraction → Mermaid + PNG (macro→meso→micro) | Block + OOP diagrams (C3, C4) |
| (e) | How did we **find the bug + its root cause**? | Graph-guided agent: index → hot.md → ranked suspects → targeted snippets | `reports/BUG_ANALYSIS.md` (C5, C6) |
| (f) | What is the **advantage of graph navigation vs linear reading**? | Side-by-side investigation path; signal-to-noise contrast | `reports/TOKEN_COMPARISON.md`, README §9 |
| (g) | How did the graph-guided agent **save tokens**? | Honest baseline vs guided ledger on the SAME bug | `reports/TOKEN_COMPARISON.md`, `SPEC_SHEET.md` (C8, C15) |
| (h) | What **future extensions** follow? | Centrality ranking, dynamic `hot.md`, orphan detection, impact report | `extensions/`, README §extensions (C9) |

## 4. Functional requirements → acceptance criteria C1–C15

Every acceptance criterion C1–C15 appears exactly once; FR-IDs are traceable to TODO/PLAN.

| FR | Requirement | Criterion |
|----|-------------|-----------|
| FR-01 | Run Graphify on the buggy codebase, producing `graph.json` + `GRAPH_REPORT.md` (+ `graph.html`); DIY ast+networkx fallback if the CLI fails | **C1** |
| FR-02 | Generate the Obsidian vault as an active knowledge space: `index.md` nav hub + `hot.md` bug-critical area + linked pages (central components, suspects, tests, findings, fix process) | **C2** |
| FR-03 | Extract an architectural **block diagram** (communities/hubs/bridges + flow) from the graph — not a folder listing | **C3** |
| FR-04 | Extract an **OOP schema** (classes, composition, inheritance, usage, patterns) from the code via AST | **C4** |
| FR-05 | Build the **graph-guided LangGraph agent** that consults graph/Obsidian FIRST, then requests ONLY targeted snippets; bounded calls/steps; explained workflow | **C5** |
| FR-06 | Locate, root-cause, and fix **a real bug**; verify the BugsInPy failing test passes (`bugsinpy-test` FAIL→PASS) | **C6** |
| FR-07 | Record **before/after** at code level (diff) AND knowledge level (vault pages/nodes/links/insights added; understanding changed) | **C7** |
| FR-08 | **Token-savings comparison**: naive raw-files vs graph-guided, measuring tokens, files/units read, iterations, quality/speed to root cause — HONEST numbers | **C8** |
| FR-09 | Ship **≥1 original extension per part** (centrality suspect-ranking, dynamic `hot.md` from `git diff`, orphan detection, diff-based impact report) | **C9** |
| FR-10 | Produce a **rich README** with all spec §8 elements + visuals (screenshots, graphs, block diagram, OOP schema, flow diagrams) | **C10** |
| FR-11 | Maintain **repo structure**: `src/`, `tests/`, `obsidian/`, `reports/`, `artifacts/`, `data/` | **C11** |
| FR-12 | State the **chosen repo + justification** in README; answer the §4 research questions across README/reports/Obsidian | **C12** |
| FR-13 | Run the target in an **isolated environment** (venv/Docker); document clear, reproducible run instructions | **C13** |
| FR-14 | Apply **evidence tiers** (`Extracted`/`Inferred`/`Ambiguous`) when reading graph edges; apply the **God Node vs healthy Hub** distinction | **C14** |
| FR-15 | Commit the **Token Spec Sheet** (the ledger) as a report | **C15** |

## 5. Non-functional requirements

- **Honest measurement.** Both the naive baseline and the graph-guided agent run on the SAME bug;
  token counts come from `usage_metadata` via `shared/gatekeeper.py` — never estimated, never
  rounded up. If savings are modest, the report says so and explains why (small target, Graphify
  semantic-extraction overhead). A measured number is the deliverable; folklore percentages are not.
- **Reproducibility (isolated env).** The BugsInPy target lives in its OWN venv/Docker, separate
  from our `uv`-managed project. A fresh clone + `uv sync` + `.env` (free `GOOGLE_API_KEY`) must
  reproduce the pipeline; `data/target/*` is gitignored, artifacts are committed.
- **Token economy.** The agent loads `index.md`/`hot.md`/graph summary before any source, then
  fetches ONLY ranked suspects — maximizing signal-to-noise and avoiding Context Rot / Lost in the
  Middle by construction. Bounded by `max_llm_calls` (state counter) + `recursion_limit`.
- **Determinism.** Tests seed `random`; ALL LLM/Graphify/BugsInPy/git/subprocess I/O is MOCKED;
  no live calls in the suite; `temperature=0` for the agent. No flakes.
- **English only + professor vocabulary.** All deliverables use the graded terms verbatim:
  Extracted/Inferred/Ambiguous, Context Rot vs Overflow, Lost in the Middle, God Node vs healthy
  Hub, Centrality, Community, Bridge, `index.md` as navigation hub, guided retrieval, signal-to-noise.
- **150-line cap.** Every `.py` file ≤ 150 lines (blanks + comments included); split otherwise.
- **Coverage ≥ 85%**, enforced in CI (`--cov-fail-under=85`); `ruff check` returns zero violations;
  all business logic flows through the single `class SDK` at `src/cosmos77_ex04/sdk/sdk.py`.

## 6. KPIs / Definition of Done

The project is DONE only when every item below is true and reproducible:

1. **Graph produced** — `artifacts/graph.json` + `GRAPH_REPORT.md` exist and parse into nodes/edges
   with evidence tiers, communities, and centrality.
2. **Vault produced** — `obsidian/index.md` (navigation hub) + `obsidian/hot.md` (god-nodes + the
   failing test's neighborhood) + linked investigation pages; all `[[wikilinks]]` resolve.
3. **Diagrams produced** — architectural **block diagram** + **OOP schema** (Mermaid + PNG) extracted
   from graph + AST, with the God Node vs healthy Hub analysis in `reports/ARCHITECTURE.md`.
4. **Bug fixed (FAIL → PASS)** — the BugsInPy failing test fails before the fix and passes after;
   the unified diff and verification output are captured in `reports/BUG_ANALYSIS.md`.
5. **Honest token ledger** — `reports/TOKEN_COMPARISON.md` + `reports/SPEC_SHEET.md` report measured
   tokens, files read, and iterations for baseline vs guided, with a chart and an honest narrative.
6. **≥1 extension per part** — centrality suspect-ranking, dynamic `hot.md`, orphan detection, and
   diff-based impact report, each tested on fixtures.
7. **≥85% coverage** with `ruff check` clean, line-cap clean, and CI green.
8. **≥600 TODO items** — `docs/TODO.md` expanded to ≥600 granular `T-NNNN` tasks across P0–P12.
9. **Before/after recorded** at both code and knowledge level (C7), and the §4 research questions
   (a)–(h) answered across README, reports, and the vault.

## 7. Out of scope

A production-grade fix beyond the single documented BugsInPy bug; supporting multiple bugs or
multiple target projects simultaneously (default `tqdm`; alternates are config swaps only); a
hosted/web UI for the Obsidian vault (plain Markdown is the deliverable; Obsidian Desktop is for
screenshots only); paid LLM tiers or providers other than the config-driven Gemini free tier;
fine-tuning or training any model; and beating a specific savings percentage — the requirement is
an **honest** comparison, whatever the measured number turns out to be.
