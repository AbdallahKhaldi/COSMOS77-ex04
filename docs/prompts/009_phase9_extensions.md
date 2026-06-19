# Prompt log 009 — Phase 9: Original extensions (≥1 per part)

**Phase:** 9 — The original initiatives the spec demands (C9)
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-19

## Prompt issued

> Phase 9 goal: the original initiatives the spec demands (C9). Implement at least
> (`../CLAUDE_CODE_PLAYBOOK.md` §11): `centrality_rank.py` (rank suspects by
> centrality + proximity to the failing test → obsidian/suspects.md);
> `dynamic_hot.py` (regenerate hot.md from `git diff` ∩ graph.json neighbourhoods);
> `orphans.py` (isolated-node detection + classification → reports/ORPHANS.md);
> `impact_report.py` (diff-based "what breaks if we change X" → reports/IMPACT.md).
> Each gets unit tests on fixtures.

## What was done

Built `src/cosmos77_ex04/extensions/` (each ≤150, deterministic, no LLM):
- **`centrality_rank.py`** — `rank_suspects_scored` makes the agent's ranking
  explicit (degree + betweenness + traceback/proximity boost) and
  `write_suspects_md` writes `obsidian/suspects.md` (a ranked table).
- **`dynamic_hot.py`** — `changed_files_from_git` (`git diff --name-only`, runner
  injected) ∩ graph nodes + 1-hop neighbourhoods → regenerated `obsidian/hot.md`
  (falls back to the God Nodes when the diff is empty, so hot.md is never empty).
- **`orphans.py`** — `find_orphans` (no in/out edges) + a label heuristic
  classifier (intentional adapter/legacy vs possible dead code) → `reports/ORPHANS.md`.
- **`impact_report.py`** — `impacted_nodes` (reverse-reachable callers) +
  God-Node betweenness → `reports/IMPACT.md` ("what breaks if we change X").
- **`run.py`** — `run_extensions(config, repo_root)` orchestrator; wired to
  `SDK.run_extensions` + CLI `extensions`.

The impact target is the **top God Node** (the most central component), the
meaningful blast-radius question, rather than a low-degree file.

## Verification

```bash
uv run pytest -m "not live" -q   # 189 passed, coverage 98.8%
uv run cosmos77-rev extensions
ls reports/ORPHANS.md reports/IMPACT.md obsidian/suspects.md   # all present
```

## Findings (real data, honest)

- **suspects.md** — ranked: `tqdm` #1 (degree 106, betweenness 0.5066, score 113).
- **ORPHANS.md** — **0 orphans**: the tqdm graph is well-connected (an honest
  deterministic result, reported with the verification caveat).
- **IMPACT.md** — "what breaks if we change `tqdm`" → **135 dependent callers**
  (reverse-reachable blast radius) + the God-Node betweenness Bridges.
- **hot.md** — regenerated dynamically; all `[[wikilinks]]` still resolve.

## Notes

- The extensions package was built by a parallel subagent (fully fixture-tested,
  git mocked); the orchestrator wired the SDK/CLI, ran them on the real graph, and
  retargeted the impact analysis to the God Node for a meaningful blast radius.
