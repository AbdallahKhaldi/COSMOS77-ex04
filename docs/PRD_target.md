# PRD — BugsInPy Target Checkout / Test Harness (`prepare_target`)

**Course:** UOH-RL07 — Vibe Coding & AI Agents (Dr. Yoram Segal) · **Assignment:** HW4
**Authors:** Abdallah Khaldi, Tasneem Natour · **Version:** 1.00 · **Status:** Specification (Phase 2)
**Maps to acceptance criteria:** **C6** (a real bug, reproduced via its failing test) · **C13** (isolated environment + reproducible run instructions)

## 1. Purpose

This mechanism is the *front door* of the whole pipeline: it produces the **real, buggy substrate**
every later deliverable depends on. It clones the **BugsInPy** benchmark once (cached), checks out
ONE bug of the default project **`tqdm`** into `data/target/`, compiles it, and runs its
**pinned failing test** inside an **isolated environment** (the target's OWN venv or Docker — never
our `uv`-managed interpreter). The harness's contract is honest and narrow: it tells the rest of the
system *where the buggy source lives*, *the exact command that reproduces the failure*, and the
*buggy and fixed commit SHAs*. Without a credible failing test (C6) the bug-fix verification is
hollow; without env isolation (C13) the reproduction is not portable. This PRD specifies the module
split (each file ≤150 lines), the single SDK method `prepare_target()`, and a fully-mocked test plan.

A toy target would make the downstream block diagram, OOP schema, and token comparison meaningless.
Choosing a small-but-REAL `tqdm` bug is the design decision that gives every later artifact teeth.

## 2. Inputs / Outputs

**Inputs** (all config-driven — Rule 4, zero hardcoded values; read via the dot-path Config loader):

| Source | Key | Default | Meaning |
|--------|-----|---------|---------|
| `config/setup.json` | `target.source` | `bugsinpy` | Benchmark provider (only `bugsinpy` for v1.00). |
| `config/setup.json` | `target.project` | `tqdm` | BugsInPy project name. |
| `config/setup.json` | `target.bug_id` | `null` | Chosen bug index; `null` ⇒ harness resolves a clean one via `info.py`. |
| `config/setup.json` | `target.workdir` | `data/target` | Checkout destination (gitignored). |
| `config/setup.json` | `target.isolation` | `venv` | `venv` (per-project) or `docker`. Honored on every compile/test invocation. |
| env / constants | `BUGSINPY_REPO_URL`, cache dir | — | Where to clone BugsInPy once and cache it. |

**Outputs** — an immutable `TargetInfo` dataclass returned by `prepare_target()` and serialized to
`artifacts/target_info.json` for downstream stages (graphify, agent, fix) and the README:

- `source_dir: Path` — the buggy project source tree (input to Graphify in Phase 3).
- `workdir: Path` — the BugsInPy checkout root (`data/target/`).
- `failing_test_cmd: list[str]` — the exact command that reproduces the failure (the bug, C6).
- `buggy_commit: str`, `fixed_commit: str` — SHAs read from BugsInPy bug metadata.
- `python_version: str`, `pinned_deps: list[str]` — the target's required Python + dependencies.
- `isolation: str` — `venv` | `docker`, echoed for the README's reproducibility section (C13).

**Side effects:** a cached BugsInPy clone; a populated `data/target/`; `artifacts/target_info.json`.
**Expected real-run result:** the failing test **FAILS** — that failure *is* the bug we will fix.

## 3. Module design (files + responsibilities — each ≤150 lines)

All live under `src/cosmos77_ex04/target/`. The 150-line cap drives a three-file split so that
*orchestration*, *command strings*, and *bug discovery* never share a file (Rules 1 & 3).

### 3.1 `target/bugsinpy_cli.py` — thin command builders (~70 lines)
Pure functions, **no I/O**, returning `list[str]` argv vectors — trivially unit-testable and the
single source of truth for command shape:
- `clone_cmd(repo_url, dest) -> list[str]` → `git clone --depth 1 <url> <dest>`.
- `checkout_cmd(project, version, bug_id, workdir) -> list[str]` → `bugsinpy-checkout -p <project> -v <version> -i <bug_id> -w <workdir>`.
- `compile_cmd() -> list[str]` → `bugsinpy-compile`.
- `test_cmd() -> list[str]` → `bugsinpy-test`.
- `info_cmd(project) -> list[str]` → `bugsinpy-info -p <project>`.
- `wrap_for_isolation(argv, isolation, image) -> list[str]` → identity for `venv`; prefixes a
  `docker run --rm -v <workdir>:<mnt> <image> …` shell for `docker`. **This is where C13 isolation
  is honored**, so every compile/test path is testable for the right interpreter context.

### 3.2 `target/info.py` — bug discovery (~80 lines)
Wraps `bugsinpy-info` so we pick a *small, clean* bug instead of guessing an id:
- `list_bugs(project, runner) -> list[BugMeta]` — runs `info_cmd`, parses stdout into
  `BugMeta(bug_id, test_file, buggy_commit, fixed_commit, python_version)`.
- `read_bug_metadata(workdir) -> BugMeta` — after checkout, reads BugsInPy's `bug.info` /
  `bugsinpy_*` files for the authoritative failing-test command, commits, deps, and Python version.
- `choose_clean_bug(bugs) -> BugMeta` — selects the candidate with a single, narrowly-scoped failing
  test and the fewest pinned deps (heuristic documented inline). Used only when `bug_id` is `null`.

### 3.3 `target/checkout.py` — orchestration (~110 lines)
The conductor; owns sequencing and the `TargetInfo` assembly, delegates all command shape to
`bugsinpy_cli` and all parsing to `info.py`:
- `_run(argv, cwd) -> CompletedProcess` — the **one** wrapper over `subprocess.run` (the single mock
  seam; `check=False` so a failing test does not raise — a non-zero exit is the *expected* bug).
- `ensure_bugsinpy(cache_dir) -> Path` — clone once if absent, else reuse the cache.
- `checkout_bug(cfg) -> Path`, `compile_target(workdir, isolation) -> CompletedProcess`.
- `run_failing_test(workdir, isolation) -> CompletedProcess` — returns result; **does not** assert
  pass/fail (Phase 7's fix flips FAIL→PASS).
- `prepare(cfg) -> TargetInfo` — the public entry the SDK calls: ensure → (resolve bug) → checkout →
  read metadata → compile → capture failing-test command → return `TargetInfo` and persist JSON.

`shared/`: `models.py` holds `TargetInfo` / `BugMeta` dataclasses if reused elsewhere; constants
(`BUGSINPY_REPO_URL`, cache path, `ISOLATION_MODES`) live in `constants.py`. If `checkout.py`
approaches 150 lines, lift `ensure_bugsinpy` + isolation wiring into `target/env.py`.

## 4. Public SDK API

Single entry point — all business logic flows through `class SDK` (Rule 2):

```python
# src/cosmos77_ex04/sdk/sdk.py
def prepare_target(self) -> TargetInfo:
    """Clone BugsInPy (cached), check out one tqdm bug into the configured isolated
    workdir, compile it, and capture the failing-test command + buggy/fixed commits.

    Reads target.* from config; never hardcodes project/bug/paths (Rule 4). Honors
    target.isolation (venv|docker) for compile/test (C13). Returns a TargetInfo with
    source_dir, workdir, failing_test_cmd, buggy_commit, fixed_commit, python_version,
    pinned_deps. Does NOT assert the test passes — the failing test reproduces the
    bug (C6); Phase 7 flips it FAIL->PASS. Side effect: artifacts/target_info.json.
    """
```

CLI surface (Typer): `uv run cosmos77-rev prepare-target` invokes `SDK().prepare_target()` and
prints the resolved `TargetInfo` (source dir, failing-test command, commits, isolation mode).

## 5. Test plan (TDD, ALL subprocess/git/BugsInPy I/O MOCKED — Rule 6; no live calls)

Mock seam: `subprocess.run` via the single `_run` wrapper, fed canned `CompletedProcess` objects.
`tmp_path` for the filesystem; `random` seeded; no network, no real clone, no real checkout.

**Happy path**
- `test_checkout_cmd_shape` — `checkout_cmd("tqdm","1","0","data/target")` equals
  `["bugsinpy-checkout","-p","tqdm","-v","1","-i","0","-w","data/target"]` (exact argv, C6 reproducibility).
- `test_compile_and_test_cmd_shape` — `compile_cmd()`/`test_cmd()` are `["bugsinpy-compile"]` / `["bugsinpy-test"]`.
- `test_isolation_venv_is_identity` / `test_isolation_docker_prefixes_run` — `wrap_for_isolation`
  leaves venv argv untouched but prefixes `docker run … <image>` when `isolation="docker"` (C13).
- `test_prepare_returns_targetinfo` — with mocked `_run` returning fixture stdout, `prepare(cfg)`
  yields a `TargetInfo` whose `failing_test_cmd`, `buggy_commit`, `fixed_commit`, and `python_version`
  match the fixture metadata; assert `artifacts/target_info.json` is written.
- `test_failing_test_command_captured` — the failing-test command is recorded verbatim even though
  the mocked test exits non-zero (FAIL is expected, not an error).
- `test_clone_is_cached` — second `prepare` with an existing cache does **not** re-issue the clone argv.
- `test_choose_clean_bug` — given fixture `bugsinpy-info` output, `choose_clean_bug` picks the
  single-failing-test / fewest-deps candidate; `bug_id=null` triggers discovery, an explicit id skips it.

**Error path**
- `test_checkout_failure_raises` — non-zero exit on `bugsinpy-checkout` (not the test) raises a clear
  `TargetCheckoutError` naming the failing argv.
- `test_unknown_isolation_rejected` — `isolation="chroot"` raises `ValueError` listing valid modes.
- `test_info_parse_empty` — empty/garbled `bugsinpy-info` stdout raises a parse error, never silently
  returns an empty bug list.
- `test_missing_metadata` — absent `bug.info` after checkout raises rather than fabricating commits.

Determinism: seeded `random`, mocked clock if timing is recorded; coverage of this package ≥85%.

## 6. Acceptance-criteria mapping

| Criterion | How this mechanism satisfies it | Evidence |
|-----------|--------------------------------|----------|
| **C6** — a real bug, root-caused & fixed, failing test verified | Checks out a real `tqdm` bug and captures its exact failing-test command; the real `prepare-target` run **fails that test** (the bug), and `failing_test_cmd` is the command Phase 7 flips FAIL→PASS. | `artifacts/target_info.json`; `reports/BUG_ANALYSIS.md`; real-run failing-test output. |
| **C13** — isolated environment + reproducible instructions | `wrap_for_isolation` runs compile/test in the target's OWN venv/Docker per `target.isolation`; `TargetInfo` records Python version + pinned deps for the README's reproduction steps. | `target.isolation` config; README §run; `TargetInfo.python_version`/`pinned_deps`. |
| Supports C1 | Emits `source_dir` consumed by Graphify (Phase 3). | `TargetInfo.source_dir`. |

**Bug-selection record (filled at implementation; example shape):** project `tqdm`, bug id `<N>`,
buggy commit `<sha>`, fixed commit `<sha>`, failing test `bugsinpy-test` →
`tests/<…>::test_<…>`, target Python `3.<x>`, pinned deps `<list>`. A bug with exactly one
narrowly-scoped failing test and minimal deps is chosen so the substrate is small but real.

## 7. Verification (real, sets up the bug — NOT in the test suite)

```bash
uv run cosmos77-rev prepare-target   # clones BugsInPy (cached), checks out one tqdm bug into
                                     # data/target/, compiles it, runs the failing test.
                                     # EXPECTED: the failing test FAILS — that IS the bug (C6).
```

The unit suite never performs this live checkout; this command is the human-run reproduction that
proves C6/C13 end-to-end before Phase 7 applies the fix.

## 8. Risks

- **BugsInPy dependency / Python drift (HIGH).** The target may pin an old Python or heavy deps.
  *Mitigation:* the per-project venv/Docker isolation (C13); prefer a `tqdm` bug with the fewest
  pinned deps via `choose_clean_bug`; record exact versions in `TargetInfo`.
- **No clean reproducible failing test (HIGH).** Some bugs are flaky or environment-coupled.
  *Mitigation:* `choose_clean_bug` favors a single deterministic failing test; verify the real run
  before committing to the bug id; document the chosen id in config and `reports/`.
- **`bugsinpy-*` CLI not on PATH (MED).** System prerequisite, like `graphify`.
  *Mitigation:* README lists BugsInPy + Docker/venv as prerequisites; `_run` surfaces a clear
  "command not found" error rather than a silent failure.
- **Output-format brittleness in `bugsinpy-info`/`bug.info` parsing (MED).** *Mitigation:* parse from
  fixtures in tests; fail loudly on unexpected formats; never fabricate commits or deps.
- **Tempted to mock the bug away (LOW but fatal to grade).** Faking the failing test would void C6.
  *Mitigation:* unit tests mock only *I/O*, never the FAIL outcome; the real `prepare-target` run is
  the honest reproduction. The verified bug fix outranks everything (CLAUDE.md).
- **Cache staleness (LOW).** A stale BugsInPy clone could mask metadata changes. *Mitigation:*
  shallow clone, documented cache dir, and a manual refresh path; `data/target/*` is gitignored.
