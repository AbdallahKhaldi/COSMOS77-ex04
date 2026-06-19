# PRD — Real Fix + Before/After (code + knowledge) (mechanism: `agent/fix.py`)

**Course:** UOH-RL07 — Vibe Coding & AI Agents (Dr. Yoram Segal) · **Assignment:** HW4 (COSMOS77-ex04)
**Maps to:** acceptance criteria **C6** (a real bug located, root-caused, fixed, test FAIL→PASS) and **C7** (before/after at code AND knowledge level) · supports **C2** (vault update), **C8/C15** (the verified fix anchors the honest ledger)
**Authors:** Abdallah Khaldi, Tasneem Natour · **Version:** 1.00 · **Status:** Specification (Phase 7)

---

## 1. Purpose

This mechanism is where the investigation becomes *true*. Phase 6's graph-guided agent produced a
`Diagnosis` (root cause + ranked suspects + the targeted snippets it read); this mechanism turns that
diagnosis into the **MINIMAL** code change, applies it to the BugsInPy checkout in `data/target/`, and
**re-runs `bugsinpy-test` so the pinned failing test goes FAIL → PASS**. The verified bug fix and the
honest token ledger are the two artifacts that outrank everything else in this project (CLAUDE.md), so
this mechanism is held to the strictest honesty rule in the repo: **it may not claim success unless the
(mocked-in-tests, real-at-runtime) failing test actually transitions FAIL → PASS.**

It also records the **before/after at two levels**, the C7 obligation. At the **code level**: the unified
diff of the one-function change. At the **knowledge level**: the delta to the Obsidian vault — the new
`investigation.md` (the path problem → suspects → tests → root cause), the new `fix-process.md` (the change
+ its verification), the new nodes/links the investigation surfaced, and the updated `hot.md`. The
knowledge-level before/after names which pages/nodes/links/insights were added and how the architecture
*understanding* changed — e.g. a node previously read as a healthy **Hub** is re-labelled a **God Node**
once the failing test pins it as the bottleneck, or a previously-**Ambiguous** edge is promoted to
**Extracted** by the snippet the agent read. The mechanism then finalizes `reports/BUG_ANALYSIS.md`.

A fix that is large, speculative, or unverified would void C6; a fix recorded only as a diff (no vault
delta) would void C7. The design enforces both by construction: a minimal patch, a hard FAIL→PASS guard,
and a deterministic vault-delta record.

## 2. Inputs / Outputs

**Inputs** (config-driven via the dot-path Config loader — rule 4; no hardcoded paths/project/bug):

| Source | Key / value | Meaning |
|--------|-------------|---------|
| Phase 6 | `Diagnosis` (root-cause node, ranked suspects, snippets read, file+line targets) | What to change and where. |
| Phase 2 | `TargetInfo` (`source_dir`, `workdir`, `failing_test_cmd`, `buggy_commit`, `fixed_commit`, `isolation`) | Where the buggy source lives and the exact command that reproduces the failure. |
| `config/setup.json` | `target.workdir` (`data/target`), `target.isolation` (`venv`\|`docker`), `paths.obsidian_dir`, `paths.reports_dir`, `paths.artifacts_dir` | Checkout root, isolation mode for the re-run, vault/report destinations. |
| `config/setup.json` | `fix.max_diff_lines` (new knob, default e.g. 40) | Honesty cap: a minimal change, not a rewrite. |
| LLM (optional) | the Phase-6 Gemini call already proposed the change; the patch text may be reused — no *new* LLM call is required here | Keep token cost on the ledger, not duplicated. |

**Outputs:**

- A **unified diff** of the applied change, captured as text and saved to `artifacts/fix.diff`.
- The **patched** `data/target/` source tree (gitignored substrate; the diff is the committed evidence).
- A **`FixResult`** dataclass returned by `apply_fix()`: `diff: str`, `test_before: TestOutcome` (FAIL),
  `test_after: TestOutcome` (PASS), `verified: bool`, `changed_files: list[Path]`, `vault_delta: VaultDelta`.
- Vault updates under `paths.obsidian_dir`: `investigation.md`, `fix-process.md`, updated `hot.md`, plus any
  new node pages/links the investigation surfaced. (`investigation.md`/`fix-process.md` started as Phase-2
  **templates**; this mechanism fills them.)
- A **`VaultDelta`** record (pages added, nodes added, links added, insights, re-tier/re-label events) — the
  knowledge-level before/after, serialized to `artifacts/vault_delta.json`.
- Finalized `reports/BUG_ANALYSIS.md`: problem, root cause, investigation steps, the fix, and the verified
  test output (before = FAIL, after = PASS).

**Side effects:** patched `data/target/`; `artifacts/fix.diff`; `artifacts/vault_delta.json`; vault pages;
`reports/BUG_ANALYSIS.md`. **Expected real-run result:** the previously-failing test now **PASSES**.

## 3. Module design (every `.py` ≤ 150 lines — rule 1)

All live under `src/cosmos77_ex04/agent/`. The 150-line cap (and the playbook's ≤120 hint for `fix.py`)
drives a four-file split so *patch application*, *the success guard*, *the vault delta*, and *the report*
never share a file (rules 1 & 3 — composition, not duplication).

| File | Responsibility | Why separate |
|------|----------------|--------------|
| `agent/fix.py` (≤120 lines) | **Orchestrator / fix node.** Takes `Diagnosis` + `TargetInfo` + config; computes the minimal patch, applies it to `data/target/`, captures the unified diff, drives the FAIL→PASS re-run through `guard.py`, assembles `FixResult`. Holds the LangGraph fix-node wiring. | Thin conductor; one place that decides *what* the fix run does. |
| `agent/patch.py` | **Patch mechanics (pure where possible).** `build_patch(diagnosis, source_dir) -> Patch`, `apply_patch(patch, source_dir) -> list[Path]`, `unified_diff(before, after, path) -> str`. Enforces `fix.max_diff_lines`. No subprocess. | Isolates text/AST surgery + diff generation; trivially unit-testable as strings. |
| `agent/guard.py` | **Success guard + test re-run (the honesty rule).** `rerun_test(target_info) -> TestOutcome` (the single `subprocess.run` mock seam, reusing `target/checkout.run_failing_test`), and `assert_fail_to_pass(before, after) -> bool` which **raises `FixNotVerifiedError` unless `before == FAIL and after == PASS`**. | The one gate that can block a false PASS claim; kept tiny and 100%-tested. |
| `agent/fix_record.py` | **Knowledge-level before/after.** `record_vault_delta(vault, diagnosis, patch) -> VaultDelta` writes `investigation.md` + `fix-process.md`, updates `hot.md`, adds new node pages/links, and computes the `VaultDelta`; `write_bug_analysis(result, diagnosis) -> Path` finalizes `reports/BUG_ANALYSIS.md`. Reuses `vault/pages.py` + `vault/wikilinks.py` (rule 3 — no duplicate Markdown logic). | Keeps `fix.py` under the cap; the C7 record is testable independently of patching. |

Shared types (`shared/models.py` or `agent/__init__.py` re-export): `Patch`, `TestOutcome` (enum
`FAIL`/`PASS`/`ERROR`), `FixResult`, `VaultDelta`. New exceptions `FixNotVerifiedError`,
`PatchTooLargeError` live in `shared/errors.py`. If `fix_record.py` approaches the cap, split
`write_bug_analysis` into `agent/report.py`.

## 4. Public SDK API

All business logic routes through the single `class SDK` (rule 2 / ADR-006); the CLI sub-command `fix`
maps 1:1 to it and holds no logic.

```python
class SDK:
    def apply_fix(
        self,
        diagnosis: Diagnosis | None = None,   # default: load from artifacts/diagnosis.json (Phase 6)
        target_info: TargetInfo | None = None,  # default: load from artifacts/target_info.json (Phase 2)
        *,
        update_vault: bool = True,            # write investigation/fix-process, update hot.md, record delta
    ) -> FixResult:
        """Apply the MINIMAL code change for the diagnosed root cause to data/target, re-run
        bugsinpy-test, and verify the failing test goes FAIL -> PASS (C6). Capture the unified
        diff (artifacts/fix.diff). Record before/after at code AND knowledge level (C7): fill
        investigation.md + fix-process.md, update hot.md, add new nodes/links, write VaultDelta,
        and finalize reports/BUG_ANALYSIS.md. Honesty rule: RAISES FixNotVerifiedError unless the
        test transitions FAIL -> PASS; verified=True is never returned on a false PASS claim.
        """
```

CLI surface (Typer): `uv run cosmos77-rev fix` invokes `SDK().apply_fix()` and prints the diff summary, the
before=FAIL / after=PASS outcome, and the vault-delta counts (pages/nodes/links/insights added).

## 5. Test plan (TDD red→green→refactor — rule 6; `bugsinpy-test`/git/subprocess MOCKED, no live calls)

Mock seam: `agent/guard.rerun_test` wraps the single `subprocess.run` (via `target/checkout`), fed canned
`TestOutcome`s. A small in-memory `Diagnosis` + `TargetInfo` fixture and a tmp `data/target/` source file
are built in `conftest`; `random` seeded; no real checkout, no real test, no LLM call.

**Code-level (C6)**
1. `test_apply_patch_produces_diff` — `build_patch` + `apply_patch` on the fixture source mutate exactly the
   diagnosed line(s); `unified_diff` returns a non-empty unified diff naming the changed file; `fix.diff` written.
2. `test_patch_is_minimal` — a patch exceeding `fix.max_diff_lines` raises `PatchTooLargeError` (honesty: a
   minimal change for the root cause, not a rewrite).
3. `test_fail_to_pass_verified` — mocked `rerun_test` returns FAIL then PASS; `apply_fix` returns
   `FixResult(verified=True, test_before=FAIL, test_after=PASS)`.

**The success guard (the honesty rule — C6)**
4. `test_guard_blocks_false_pass` — mocked test returns PASS both before and after (no real transition):
   `assert_fail_to_pass` raises `FixNotVerifiedError`; `apply_fix` does **not** return `verified=True`.
5. `test_guard_blocks_still_failing` — test FAIL then FAIL (fix ineffective) → `FixNotVerifiedError`, no success.
6. `test_guard_blocks_error_outcome` — test ERROR after patch (broke compilation) → not treated as PASS; raises.

**Knowledge-level before/after (C7)**
7. `test_vault_delta_recorded` — `record_vault_delta` writes `investigation.md` (headings: problem → suspects
   → tests → root cause) and `fix-process.md` (change + verification); updates `hot.md`; `VaultDelta` lists the
   pages/nodes/links/insights added; `vault_delta.json` written; all new `[[wikilinks]]` resolve (no orphans).
8. `test_vault_before_after_delta` — given the pre-fix vault snapshot, assert the delta is exactly the new
   pages/links (e.g. a node re-labelled Hub→God Node, an edge re-tiered Ambiguous→Extracted) — byte-stable.
9. `test_bug_analysis_finalized` — `write_bug_analysis` produces `reports/BUG_ANALYSIS.md` containing problem,
   root cause, investigation steps, the diff, and the verified `before=FAIL` / `after=PASS` test output.

Determinism: seeded `random`, stable sort keys, no timestamps in committed pages (rule 17). Package coverage
≥ 85% (rule 7) with `guard.py` at 100%; `ruff` clean (rule 8); line-cap clean (rule 1).

## 6. Acceptance-criteria mapping

| Criterion | How this mechanism satisfies it | Evidence |
|-----------|----------------------------------|----------|
| **C6** — real bug located, root-caused, fixed, test verified | Applies the minimal change to `data/target`, re-runs `bugsinpy-test`, and the guard enforces **FAIL → PASS**; `apply_fix` raises rather than ever claiming a false PASS (Tests 3–6). **Primary owner of C6's fix half.** | `artifacts/fix.diff`; `FixResult(verified=True)`; `reports/BUG_ANALYSIS.md` before=FAIL/after=PASS; real-run test output. |
| **C7** — before/after at code AND knowledge level | **Code:** unified diff captured (Test 1). **Knowledge:** `investigation.md` + `fix-process.md` filled, `hot.md` updated, new nodes/links added, `VaultDelta` records what changed in the architecture understanding (Hub↔God Node, edge re-tiering) (Tests 7–8). | `artifacts/fix.diff`; `artifacts/vault_delta.json`; vault pages. |
| Supports **C2** | Updates the active knowledge vault with investigation/fix pages and resolving wikilinks, reusing `vault/` renderers (no duplicate Markdown logic). | `obsidian/investigation.md`, `obsidian/fix-process.md`, updated `obsidian/hot.md`. |
| Supports **C8/C15** | The verified FAIL→PASS fix is the anchor that makes the baseline-vs-guided token ledger meaningful — both runs solve the *same, now-proven* bug. | `reports/TOKEN_COMPARISON.md`, `reports/SPEC_SHEET.md` (Phase 8). |

**Fix record (filled at implementation; example shape):** project `tqdm`, bug id `<N>`, root-cause node
`<module>.<func>`, change `<one-line description>`, diff `<K>` lines (≤ `fix.max_diff_lines`), test
`bugsinpy-test → tests/<…>::test_<…>` before = **FAIL**, after = **PASS**; vault delta: `+investigation.md`,
`+fix-process.md`, `+<N>` nodes, `+<M>` links, hot.md re-label `<node>` Hub→God Node.

## 7. Verification (real, flips the bug — NOT in the test suite)

```bash
uv run cosmos77-rev fix            # applies the minimal change to data/target, re-runs bugsinpy-test.
                                   # EXPECTED: the previously-failing test now PASSES (FAIL -> PASS, C6).
# Independently confirm in the target's OWN isolated env:
cd data/target && bugsinpy-test    # EXPECTED: PASS
```

The unit suite never performs this live re-run; this command is the human-run reproduction that proves
C6/C7 end-to-end. A `verified=True` `FixResult` is only honest if this command really passes.

## 8. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Fix claimed without real verification** (the fatal C6 failure). | Medium | Fatal to grade | `guard.assert_fail_to_pass` raises `FixNotVerifiedError` unless before=FAIL **and** after=PASS; `verified=True` is unreachable on a false claim; tests 4–6 enforce it; the real `fix` run re-confirms. |
| **Mocking the bug away** — tests assert PASS without a transition. | Medium | Fatal to grade | Unit tests mock only *I/O* (`subprocess.run`), never the FAIL→PASS *outcome*; Test 5 (FAIL→FAIL) and Test 4 (PASS→PASS) both assert the guard blocks success. The real run is the honest reproduction. |
| **Over-broad patch** that passes the test by coincidence/rewrite. | Medium | High | `fix.max_diff_lines` caps the diff; `PatchTooLargeError` (Test 2); the change targets only the diagnosed root-cause node from Phase 6, not the whole file. |
| **Patch breaks compilation** (test ERRORs, not PASSes). | Medium | High | `TestOutcome.ERROR` is distinct from `PASS`; the guard treats ERROR as not-verified (Test 6); compile step re-run in the target's isolated env (C13). |
| **Vault delta non-deterministic** (set iteration / timestamps) breaks the C7 diff. | Medium | Medium | Stable sort keys, no timestamps in committed pages; Test 8 enforces a byte-stable delta. |
| **Duplicate Markdown logic** drifting from `vault/`. | Low | Medium | `fix_record.py` reuses `vault/pages.py` + `vault/wikilinks.py` (rule 3); wikilinks resolved by the same encoder (Test 7). |
| **`fix.py` exceeds the 150-line cap.** | Medium | Low | Patch mechanics → `patch.py`, guard → `guard.py`, knowledge record → `fix_record.py`; orchestrator stays ≤120; `check_line_cap.py` in CI catches regressions. |

---

*End of PRD. See `docs/PRD.md` (FR-06/FR-07 → C6/C7), `docs/PRD_target.md` (`prepare_target` supplies the
failing test this mechanism flips), `docs/PRD_vault.md` (the `investigation.md`/`fix-process.md` templates
this mechanism fills), `docs/PLAN.md` ADR-005/ADR-006 and the run sequence diagram, and
`CLAUDE_CODE_PLAYBOOK.md` §1.5 (C1–C15) + §9 (Phase 7 spec).*
