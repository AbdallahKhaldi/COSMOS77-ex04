# Prompt log 006 — Phase 6: Graph-guided LangGraph debug agent (the core)

**Phase:** 6 — The graph-guided debugging agent (C5) — the heart of the grade
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-19

## Prompt issued

> Phase 6 goal: the graph-guided debugging agent (C5). It must consult the
> graph/Obsidian FIRST and request code snippets ONLY for the top suspects, with
> tightly bounded LLM calls (`../CLAUDE_CODE_PLAYBOOK.md` §8). LangGraph
> `StateGraph` + Gemini `gemini-2.5-flash`; state carries step_count + suspects +
> files_read + tokens; cap calls with a state counter AND `recursion_limit`; read
> tokens from `response.usage_metadata`. Nodes: load_context (index.md + hot.md +
> graph summary, NO source), rank_suspects, request_snippets (ONLY the top-K),
> diagnose (LLM), should_continue. Persist reports/BUG_ANALYSIS.md. Unit tests
> mock the LLM; assert the agent loads context BEFORE any source and never
> bulk-reads the repo.

## What was done

Built `src/cosmos77_ex04/agent/` (each file ≤150):
- **`state.py`** — `AgentState` TypedDict + an injectable `AgentDeps` (so tests
  pass a fake LLM).
- **`llm.py`** — `build_llm` (ChatGoogleGenerativeAI from providers.json) +
  `invoke_diagnose` (records `usage_metadata` into the Gatekeeper ledger).
- **`retrieval.py`** — the context-reduction core (NO LLM): `rank_suspects`
  (Centrality + name-proximity + **traceback-file** boost), `fetch_snippets`
  (reads ONLY the distinct suspect files, capped), `graph_summary`, `read_vault`.
- **`nodes.py`** — load_context / rank_suspects / request_snippets / diagnose /
  should_continue.
- **`graph.py`** — the `StateGraph` (load_context → rank_suspects →
  request_snippets → diagnose → loop/END), `recursion_limit` from config, and the
  `investigate()` high-level entry.
- **`analysis.py`** — writes `reports/BUG_ANALYSIS.md`.
- Wired `SDK.run_agent` + CLI `agent`; `prepare_target` now persists the failing
  test traceback to `data/target/_test_output.txt` for the agent to read.

**Key accuracy improvement:** the first live run mis-diagnosed (a plausible
look-alike) because the agent lacked the runtime error. We feed the **failing-test
traceback** (the universal debugging starting point — given to BOTH arms, so the
Phase-8 comparison stays fair) into the agent's context and boost suspects whose
file appears in it. The second run then correctly identified the real bug.

## Verification (real Gemini, free)

```bash
uv run pytest -m "not live" -q   # 142 passed, coverage 98.7%
uv run cosmos77-rev prepare-target   # persists the traceback
uv run cosmos77-rev agent
#   files_read (2): ['std.py', 'tests/tests_tqdm.py']   <- graph-guided, NOT the whole repo
#   tokens: {input 38123, output 2703, total 40826, calls 1}  iterations: 1
cat reports/BUG_ANALYSIS.md
```

## The diagnosis (correct)

> ROOT CAUSE: `tenumerate` in `tqdm.contrib` passes its `start` argument as the
> `desc` parameter to the `tqdm` constructor, causing a `TypeError` when tqdm does
> string operations on the integer `desc`. FILE: `tqdm/contrib/__init__.py`. FIX:
> `return enumerate(tqdm_class(iterable, **tqdm_kwargs), start)`.

This matches the real BugsInPy tqdm bug 1: the `std.py` TypeError in the traceback
traces back to `tenumerate`. The agent reached it reading only **2 files** —
graph-guided, never the whole repository. Tokens are MEASURED (40,826), the
evidence Phase 8 compares against a naive baseline.

## Notes

- Unit tests assert the invariants: context loaded before any source, only suspect
  files read (a planted `other.py` with a secret is NEVER read), the step cap
  halts the loop, and the ledger records the call.
