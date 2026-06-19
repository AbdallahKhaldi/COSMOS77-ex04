# Prompt log 008 — Phase 8: Token-savings comparison (THE PROOF)

**Phase:** 8 — The honest baseline-vs-graph-guided token comparison (C8, C15)
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-19

## Prompt issued

> Phase 8 goal: the honest baseline-vs-graph-guided token comparison (C8, C15) —
> the assignment's central claim (`../CLAUDE_CODE_PLAYBOOK.md` §10). A NAIVE
> baseline on the SAME bug that does NOT use the graph/Obsidian — it loads many
> raw files into context and asks Gemini to find the bug. Record tokens
> (usage_metadata), files read, iterations, success. Compare vs the graph-guided
> ledger; compute deltas/percentages; matplotlib chart →
> artifacts/token_comparison.pdf; reports/TOKEN_COMPARISON.md with an HONEST
> narrative. If savings are modest, explain why. Never fabricate.

## What was done

Built `src/cosmos77_ex04/tokens/` (each ≤150, LLM mocked in tests):
- **`baseline.py`** — the NAIVE arm: `collect_source_files` reads EVERY `.py`
  under the package, `run_baseline` stuffs them all into ONE prompt and makes a
  single metered Gemini call (the wasteful "load everything" behaviour).
- **`compare.py`** — `compare` (deltas + percentages, divide-by-zero guarded) +
  `write_comparison_md` → `reports/TOKEN_COMPARISON.md` (table + honest narrative).
- **`chart.py`** — matplotlib Agg grouped bars (tokens + files) → PDF.
- **`spec_sheet.py`** — `reports/SPEC_SHEET.md` (the C15 ledger, per-run metrics).
- **`run.py`** — `run_comparison`: reverts the target to BUGGY (so both arms see
  the bug), runs the graph-guided agent AND the naive baseline with FRESH
  Gatekeeper ledgers, compares, writes all three deliverables.
- Wired `SDK.compare_tokens` + CLI `compare`.

## Verification (REAL — both arms live on the same buggy code)

```bash
uv run pytest -m "not live" -q   # 163 passed, coverage 98.6%
uv run cosmos77-rev compare
#   baseline: 68336 tokens, 31 files
#   guided:   40826 tokens, 2 files
#   saved: 27510 tokens (40.26%), 29 files
```

## The measured result (honest)

| Metric | Baseline | Guided | Saved |
|---|---|---|---|
| Total tokens | **68,336** | **40,826** | **40.3%** |
| Input tokens | 65,224 | 38,123 | 41.6% |
| Output tokens | 3,112 | 2,703 | 13.1% |
| Files read | **31** | **2** | **93.5%** |
| LLM calls | 1 | 1 | — |

A **measured 40% token saving** and **2 files read vs 31** — graph-guided
focused-context beats naive raw-file reading. The win is concentrated in the
INPUT context (the agent kept a high signal-to-noise context via the navigation
hub + the top suspect files, avoiding Lost in the Middle and Context Rot), which
is exactly the thesis. The output is similar because both arms reach the bug —
honest, not a fabricated 95%.

## Honesty notes

- Both arms ran on the SAME reverted-buggy code, SAME LLM (gemini-2.5-flash),
  FRESH ledgers; every number is from `usage_metadata`. Graphify's own semantic
  pass cost 0 tokens (code-only target — Phase 3 note), so the graph is ~free and
  the savings come entirely from the AGENT reading less.
- `data/target` is left in the buggy state after the comparison; `cosmos77-rev fix`
  re-applies and re-verifies FAIL→PASS.
