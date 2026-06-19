# Prompt log 001 — Phase 1: Mandatory documentation

**Phase:** 1 — All mandatory docs BEFORE business logic
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-19

## Prompt issued

> Phase 1 goal: ALL mandatory documentation before business logic. Substantive,
> not stubs. Per `../CLAUDE_CODE_PLAYBOOK.md` §3: `docs/PRD.md` (context = L07
> Lost in the Middle / Context Rot / graph-guided retrieval; the §4 research
> questions as requirements; functional requirements mapped to acceptance
> C1–C15; non-functional; KPIs); nine per-mechanism PRDs (target, graphify,
> vault, reveng, agent, tokens, bugfix, extensions, spec_sheet) — **parallelize**;
> `docs/PLAN.md` (C4 + a run sequence diagram + ADR-001…007 + a risk register);
> `docs/TODO.md` (**≥600** granular `T-NNNN` tasks across P0–P12); the prompt log.
> English + the professor's vocabulary throughout.

## What was done

Per the playbook's "parallelize the per-mechanism PRDs" directive (and the
ultracode mandate), the documentation was produced by **12 parallel subagents**,
each writing exactly one file and returning only a short summary (keeping the
orchestrator's context lean for the multi-phase build). The orchestrator then
verified counts, read the backbone docs, and committed.

- **`docs/PRD.md`** (135 lines) — problem statement (the honest-numbers thesis);
  L07 context (Overflow vs Context Rot, Lost in the Middle, signal-to-noise,
  guided retrieval, "question → index → 2-3 pages → answer"); the §4 research
  questions (a)–(h) as a requirements table; FR-01…FR-15 mapped 1:1 to **C1–C15**;
  non-functional requirements; KPIs / Definition of Done; out of scope.
- **`docs/PLAN.md`** (268 lines) — the **C4 model** (Context/Container/Component/
  Code) with a Mermaid `flowchart`; a Mermaid `sequenceDiagram` of the full run
  (checkout → graphify → vault → reveng → graph-first agent → fix FAIL→PASS →
  token compare); **seven ADRs** (ADR-001 LangGraph over CrewAI, ADR-002 Gemini
  free tier, ADR-003 BugsInPy/tqdm over a toy, ADR-004 graph-guided-first
  protocol, ADR-005 honest measurement, ADR-006 single SDK entry, ADR-007
  150-line cap), each Status/Context/Decision/Consequences; an 8-row risk register.
- **Nine per-mechanism PRDs** (`docs/PRD_{target,graphify,vault,reveng,agent,
  tokens,bugfix,extensions,spec_sheet}.md`, ~145–256 lines each) — Purpose,
  Inputs/Outputs, module design under the 150-line cap (with the concrete file
  splits), the single-`class SDK` API method, a fully-mocked TDD test plan,
  acceptance-criteria mapping, and risks. They agree on SDK method names, module
  layout, config keys, and vocabulary.
- **`docs/TODO.md`** — expanded from the Phase-0 seed to **670** granular
  `T-NNNN` tasks (contiguous T-0001…T-0670), distributed P0 (15, done) through
  P12, each with a Definition of Done and a status.

## Verification

```bash
grep -c '^T-' docs/TODO.md     # 670  (>= 600)
ls docs/PRD_*.md | wc -l       # 9    (>= 9)
grep -c 'ADR-' docs/PLAN.md    # 12   (>= 7; seven ADR sections)
uv run ruff check .            # zero (no .py added this phase)
uv run pytest -m "not live"    # green, coverage 100%
```

## Notes / decisions

- **No business logic** was written — Phase 1 is documentation only; the gates
  remain green from Phase 0 (the doc set adds no Python).
- **Parallel subagents** wrote the 12 docs concurrently; the orchestrator owns
  verification, the git history, and (from Phase 2 onward) the live runs.
- The TODO budget intentionally overshoots 600 (→670) to leave margin as tasks
  are split further during implementation.
