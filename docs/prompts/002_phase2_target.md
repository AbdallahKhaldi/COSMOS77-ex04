# Prompt log 002 — Phase 2: Shared infra + BugsInPy target harness

**Phase:** 2 — Shared layer (port) + the isolated BugsInPy checkout/test harness
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-19

## Prompt issued

> Phase 2 goal: port the shared layer and build the isolated target-checkout
> harness. All TDD; subprocess/LLM mocked (`../CLAUDE_CODE_PLAYBOOK.md` §4).
> Port `shared/{version,config,logging_setup,gatekeeper}` from
> `COSMOS77-ex03`; **repurpose `gatekeeper` as the token ledger**
> (`record(usage_metadata)` accumulating input/output/total tokens + call count;
> `ledger()` returns the aggregate; `scrub()` redacts keys). `constants.py`:
> `EVIDENCE_TIERS`, `NODE_KINDS`. New `target/`: `checkout.py` (+ split
> `bugsinpy_cli.py`) wrapping `bugsinpy-checkout/compile/test` in an isolated
> venv, returning paths + the failing-test command + buggy/fixed commit; `info.py`
> to list a project's bugs. `sdk/sdk.py` stubs (NotImplementedError) for every
> stage. Tests mock subprocess. Verify: `cosmos77-rev prepare-target` checks out
> one `tqdm` bug and the failing test FAILS (that is the bug).

## What was done

A **read-only feasibility probe** (parallel subagent) cloned BugsInPy and
actually checked out + compiled + ran `tqdm` bug 1, surfacing three realities the
harness had to honour:
1. **Python 3.6.9 is unobtainable on arm64** → use uv-installed **3.8.20**
   (tqdm's `setup.py` allows `>=2.6`) via a `python`/`python3` **pyshim**.
2. **`bugsinpy-test` is broken on macOS** (bash-4 `&>>` vs bash-3.2) → read the
   pytest line from `bugsinpy_run_test.sh` and run it in the per-bug venv.
3. Chosen bug: **`tqdm` bug 1**, failing test
   `tqdm/tests/tests_contrib.py::test_enumerate` (`TypeError: 'int' object is not
   subscriptable` at `tqdm/std.py:423`); fixed version passes.

Built (TDD, all I/O mocked):
- **`shared/version.py`** (config-version guard), **`shared/config.py`** (dot-path
  loader with `target/graphify/agent/tokens/paths` + provider accessors),
  **`shared/logging_setup.py`** (dictConfig), **`shared/gatekeeper.py`**
  (repurposed token **ledger**: `record(usage_metadata)` → input/output/total +
  per-call `CallRecord`; `ledger()`; `reset()`; `scrub()`).
- **`constants.py`**: `EVIDENCE_TIERS = (extracted, inferred, ambiguous)`,
  `NODE_KINDS`, `BUGGY_VERSION`/`FIXED_VERSION`.
- **`target/`**: `bugsinpy_cli.py` (pure command builders), `isolation.py`
  (uv-Python + pyshim + PATH env), `info.py` (`list_bugs`, `read_bug_info`,
  `read_test_command`), `checkout.py` (`BugsInPyHarness` — idempotent
  clone→checkout→compile→run-test, returning `TargetInfo`).
- **`sdk/sdk.py`**: real `prepare_target()` + `spec_sheet()` (ledger); every later
  stage a documented `NotImplementedError`. CLI `prepare-target` wired to the SDK.
- ADR-008 added to `docs/PLAN.md` documenting the Python substitution + macOS
  `bugsinpy-test` workaround.

## Verification

```bash
uv run ruff check .          # zero
uv run python scripts/check_line_cap.py   # 0 offenders (largest .py = 135 lines)
uv run pytest -m "not live"  # 64 passed, coverage 98.8% (gate 85%)
uv run cosmos77-rev prepare-target
#   target: tqdm bug #1 -> data/target/tqdm
#   python: 3.6.9  test: FAIL (expected — that is the bug)
```

## Notes / decisions

- **Rule 5 boundary honoured:** our code is `uv`-only; the BugsInPy target builds
  and tests in its OWN per-bug venv (Python 3.8.20), entirely separate.
- The failing test **FAILS** as intended — the bug is reproduced; Phase 7 will
  make it FAIL→PASS.
- Every external call (git, `bugsinpy-*`, `uv python`, pytest) is mocked in the
  suite via an injectable `runner`; no live calls in CI.
