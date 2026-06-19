# Prompt log 007 — Phase 7: Fix the bug + before/after (code + knowledge)

**Phase:** 7 — A REAL fix verified by the failing test (C6) + before/after (C7)
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-19

## Prompt issued

> Phase 7 goal: a REAL fix verified by the failing test (C6), with before/after at
> code AND knowledge level (C7) (`../CLAUDE_CODE_PLAYBOOK.md` §9). Propose the
> minimal code change for the diagnosed root cause; apply it to data/target;
> re-run bugsinpy-test → the failing test must now PASS. Capture the unified diff.
> Update the vault (investigation.md, fix-process.md, new nodes/links, hot.md);
> record a knowledge-level BEFORE/AFTER. Finalize BUG_ANALYSIS.md. A guard
> prevents claiming success unless the (mocked) test transitions FAIL→PASS.

## What was done

The graph-guided agent's diagnosis (Phase 6) matched the **canonical BugsInPy
fix** byte-for-byte:
```diff
-    return enumerate(tqdm_class(iterable, start, **tqdm_kwargs))
+    return enumerate(tqdm_class(iterable, **tqdm_kwargs), start)
```
(`tenumerate` passed `start` positionally as tqdm's `desc`, so an int hit string
operations → `TypeError`.) The fix is recorded in `config/setup.json`
(`fix.file/search/replace`) — the exact change, config-driven (rule 4).

Built (TDD):
- **`agent/fix.py`** — `verify_fail_to_pass`: restore buggy → run test (must
  FAIL) → apply fix → run test (must PASS) → capture the unified diff; the
  `FixNotVerifiedError` guard refuses to claim success on anything but a genuine
  FAIL→PASS. `run_fix` orchestrates verify + the knowledge deliverables.
- **`agent/fix_report.py`** — writes `investigation.md` (the path: problem →
  index/hot → suspects → root cause; the knowledge added) and `fix-process.md`
  (the diff + FAIL→PASS verification), and appends the verification to
  `reports/BUG_ANALYSIS.md`.
- **`target/factory.py`** — `harness_from_config` (shared harness builder).
- Wired `SDK.apply_fix` (thin) + CLI `fix`.

## Verification (REAL — the big checkpoint)

```bash
uv run pytest -m "not live" -q   # 148 passed, coverage 98.6%
uv run cosmos77-rev fix
#   fix: tqdm/contrib/__init__.py  before=FAIL -> after=PASS  applied=True
# independent re-run in the per-bug venv:
cd data/target/tqdm && env/bin/python -m pytest tqdm/tests/tests_contrib.py::test_enumerate -q
#   1 passed
```

The BugsInPy failing test **goes FAIL → PASS** — C6 verified, and independently
re-confirmed (`1 passed`). The guard makes a fabricated success impossible.

## Before / after

- **Code level:** the one-line diff above, captured in `fix-process.md`.
- **Knowledge level:** added `investigation.md` + `fix-process.md` to the vault;
  the new insight is that the central `tqdm` constructor is a Bridge whose `desc`
  contract a caller violated — a defect the graph surfaced via the traceback, not
  by reading the whole repo. BUG_ANALYSIS.md now ends with the FAIL→PASS evidence.

## Notes

- `data/target` is left in the FIXED state (gitignored). Phase 8 reverts to buggy
  so the naive baseline investigates the SAME bug for an apples-to-apples token
  comparison.
