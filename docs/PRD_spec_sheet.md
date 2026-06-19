# PRD — Token Spec Sheet / Gatekeeper Ledger (`shared/gatekeeper.py` + `spec_sheet()`)

**Course:** Orchestration of AI Agents (203.3763), Dr. Yoram Segal · **Assignment:** HW4 (COSMOS77-ex04)
**Authors:** Abdallah Khaldi, Tasneem Natour · **Version:** 1.00 · **Status:** Specification
**Maps to:** acceptance criterion **C15** (Token Spec Sheet committed as a report) · supplies the measured numbers behind **C8** (naive-vs-guided token comparison) and **C13** (reproducible run record)

---

## 1. Purpose

This mechanism is the **measurement instrument** of the whole assignment. The thesis we must *prove* — that
graph-guided focused-context work beats naive raw-file reading — is only credible if the token numbers are
**measured, not asserted**. The Gatekeeper ledger is the single point through which every Gemini call's
`usage_metadata` is recorded; `spec_sheet()` renders that record as a committed report. This is **honest
measurement** over hand-waving: the ledger reflects real `usage_metadata` returned by the model, never a
hand-tuned estimate.

A load-bearing distinction from a *cap*: the agent (`config/setup.json → agent.max_llm_calls`) has a hard call
budget, but the **ledger has no cap** — it is pure evidence and **always records**, whatever the run does. The
ledger answers the professor's two questions in numbers: *how much did the model read* (signal-to-noise) and
*how little did it have to spend* (token economy). Because both the **graph-guided** run and the **naive
baseline** route through the same ledger, the comparison is apples-to-apples by construction. The ledger IS the
deliverable's evidence (CLAUDE.md rule 13); if it is wrong, every later claim is hollow.

## 2. Inputs / Outputs

**Inputs (no network, no LLM of its own — it only observes calls made elsewhere):**

- **`usage_metadata`** dicts handed to `record(...)` by the agent/baseline after each Gemini call. Shape
  (LangChain `langchain-google-genai` convention): `{"input_tokens": int, "output_tokens": int, "total_tokens": int}`.
  Missing `total_tokens` is derived as `input + output`; missing counts default to `0` (never crash a run for a
  metric).
- **Per-call run metadata** passed alongside: `run` (`"graph_guided"` | `"naive"`), `stage` (CLI stage label),
  `model` (from `config/providers.json`), and optional `note`.
- **Per-run process metrics** the harness feeds at run boundaries: `files_read` / `units_read` (count), `iterations`,
  `wall_clock_s`, and `success_to_root_cause` (bool). These come from `tokens/` (the naive-vs-guided harness),
  not from the model.
- **Config** (read via the dot-path Config loader — rule 4): `paths.reports_dir` (default `reports/`),
  `tokens.measure` (the metric list), `tokens.baseline_mode` / `tokens.guided_mode` (the two run labels).

**Outputs:**

- An in-memory **`Ledger`** aggregate (one per process), returned by `ledger()`.
- **`reports/SPEC_SHEET.md`** — a Markdown report rendered by the SDK `spec_sheet()`: a **per-call table** (one
  row per LLM call) plus an **aggregate / per-run summary table** (graph-guided vs naive side by side). This file
  is the C15 deliverable, committed to the repo.
- A short **after-stage panel**: the same numbers surfaced (via `rich`) after each CLI stage so the operator sees
  the running cost live, not only at the end.
- Optional `reports/spec_sheet.json` — the machine-readable ledger dump, so `tokens/` and CI can assert on numbers
  without re-parsing Markdown.

**Side effects:** writes under `paths.reports_dir`. **No** mutation of the calls it observes. Secrets are
**scrubbed** before anything is written or logged (see `scrub()`).

## 3. Module design (every `.py` ≤ 150 lines — rule 1)

The ledger core lives in `shared/` (it is cross-cutting, used by `agent/`, `tokens/`, and the SDK). Rendering and
metric assembly stay out of the core so `gatekeeper.py` holds only the accounting.

| File | Responsibility | Why separate |
|------|----------------|--------------|
| `shared/gatekeeper.py` | **The ledger core.** `record(usage_metadata, **meta)` appends a `CallRecord` and accrues input/output/total tokens + call count; `ledger()` returns the immutable `Ledger` aggregate; `scrub(text\|dict)` redacts API keys. Pure accounting — no Markdown, no file I/O. | This is the single measurement seam (rule 13). Keeping it I/O-free makes it trivially unit-testable and impossible to break with formatting changes. |
| `shared/ledger_models.py` | Pydantic/`dataclass` models `CallRecord`, `RunTotals`, `Ledger` (§4). No logic. | One definition of the data model shared by core, renderer, and tests (rule 3); keeps `gatekeeper.py` under the cap. |
| `tokens/spec_render.py` | **Renderer.** `render_markdown(ledger, measure) -> str` (per-call + aggregate tables) and `render_panel(ledger)` for the after-stage `rich` panel. Consumes a `Ledger`, returns strings — no accounting. | Most lines (table formatting) live here, isolated from the accounting core so a table tweak can never corrupt a number. |
| `tokens/spec_sheet.py` | **Orchestrator** behind the SDK method: pull the live `Ledger`, attach per-run process metrics, call `render_markdown`, scrub, write `reports/SPEC_SHEET.md` (+ optional JSON), return the path. | Keeps the SDK method thin and the write-path in one place. |

**Splitting rationale.** If accounting, the data model, table formatting, and the write-path shared one file it
would blow the 150-line cap and entangle "the number" with "the look of the number". The core stays in `shared/`
because both `agent/` and the `tokens/` baseline must record into the **same** ledger instance.

**Determinism.** Per-call rows preserve insertion order; aggregates are computed by stable summation. `scrub()` is
deterministic. No timestamps in the committed table beyond an optional run header, so golden-file tests of
`render_markdown` are byte-stable (rule 17).

## 4. Ledger data model

```python
# shared/ledger_models.py
class CallRecord(BaseModel):
    run: str            # "graph_guided" | "naive"
    stage: str          # CLI stage label (e.g. "agent.localize")
    model: str          # from config/providers.json (e.g. "gemini-2.5-flash")
    input_tokens: int
    output_tokens: int
    total_tokens: int   # == input+output, derived if absent
    note: str | None = None

class RunTotals(BaseModel):          # one per run label
    run: str
    calls: int
    input_tokens: int
    output_tokens: int
    total_tokens: int
    files_read: int                  # naive: raw files; guided: vault units read
    iterations: int
    wall_clock_s: float
    success_to_root_cause: bool

class Ledger(BaseModel):
    records: list[CallRecord]        # every call, in order (per-call table)
    runs: dict[str, RunTotals]       # keyed by run label (aggregate table)
    # convenience: totals(run) and grand_total() computed from records
```

The **per-call** rows answer "where did the tokens go"; the **per-run** rows answer the C8 comparison directly.
`success_to_root_cause` is the honesty flag — a cheap run that never found the bug is not a win.

## 5. Public SDK API

All business logic routes through the single `class SDK` (rule 2). Recording itself is not an SDK method — the
agent and baseline call the module-level `record()` so every call site is uniform — but **rendering** is exposed:

```python
class SDK:
    def spec_sheet(self, *, out_dir: Path | None = None) -> Path:
        """Render the measured token ledger to reports/SPEC_SHEET.md (the C15 evidence).

        Reads the live Gatekeeper Ledger (every recorded usage_metadata), attaches per-run
        process metrics (files/units read, iterations, wall-clock, success-to-root-cause),
        scrubs any secret, writes the per-call + aggregate tables, and returns the path.
        Always measured, no cap; surfaced after each CLI stage as a rich panel.
        """
```

Module surface used by callers (in `shared/gatekeeper.py`):
`record(usage_metadata: dict, *, run: str, stage: str, model: str, note: str | None = None) -> None`,
`ledger() -> Ledger`, `scrub(value: str | dict) -> str | dict`, `reset() -> None` (test isolation).

## 6. Test plan (TDD red → green → refactor — rule 6; fake `usage_metadata` as fixtures, NO live calls)

The ledger is *built* to be tested without the model: every test feeds a **fake `usage_metadata` dict** as a
fixture, exactly the contract the real Gemini call returns. `reset()` runs in a fixture for isolation.

1. **Accrual from one call.** `record({"input_tokens":10,"output_tokens":5,"total_tokens":15}, run="naive", …)`;
   assert `ledger().runs["naive"]` has `calls==1`, `input==10`, `output==5`, `total==15`.
2. **Aggregation across calls.** Record three calls for `graph_guided`; assert call count and the summed
   input/output/total are exact (no double counting, no drift).
3. **Two runs kept separate.** Record into `naive` and `graph_guided`; assert each `RunTotals` is independent and
   `grand_total()` equals their sum — the C8 comparison must not cross-contaminate.
4. **Derived total.** Feed `usage_metadata` with **no** `total_tokens`; assert `total == input+output`. Feed
   missing counts; assert they default to `0` and the run still records (no crash for a metric).
5. **`scrub()` redacts a key.** Pass a string and a dict containing a `GOOGLE_API_KEY`-shaped value; assert the
   secret is replaced with a redaction marker and surrounding text/keys are preserved; idempotent on already-clean
   input.
6. **`spec_sheet()` renders a non-empty table.** With a populated ledger, `SDK().spec_sheet(out_dir=tmp_path)`
   writes `SPEC_SHEET.md`; assert it exists, is non-empty, contains a per-call row for each record and an
   aggregate row per run, and contains **no** raw API key (scrub applied on the write-path).
7. **Determinism.** `render_markdown` on a fixed ledger is byte-identical across two calls (golden-file; rule 17).
8. **Process metrics surface.** Attach `files_read`/`iterations`/`wall_clock_s`/`success_to_root_cause`; assert
   they appear in the aggregate table for both runs (the numbers C8 narrates).

Coverage of `shared/` + `tokens/` ≥ 85% (rule 7); `ruff` clean (rule 8); line-cap clean (rule 1).

## 7. Acceptance-criteria mapping

| Criterion | How this mechanism satisfies it |
|-----------|---------------------------------|
| **C15** (Token Spec Sheet committed as a report) | `spec_sheet()` renders `reports/SPEC_SHEET.md` from the measured Gatekeeper ledger — per-call + aggregate tables — and it is committed. **Primary owner of C15.** (Tests 6, 7) |
| **C8** (naive-vs-guided token comparison) | The same ledger records BOTH runs (`tokens.baseline_mode` vs `tokens.guided_mode`); per-run totals (tokens in/out/total, calls, files/units read, iterations, wall-clock, success-to-root-cause) give the side-by-side numbers. (Tests 2, 3, 8) |
| **C13** (reproducible run record) | The committed spec sheet + JSON dump record exactly what each run cost, with the model from `config/providers.json` — reproducible evidence, not prose. |
| Rule 13 / honest measurement | `record()` is the single seam every LLM call routes through; numbers come from real `usage_metadata`; `scrub()` keeps secrets out of the committed evidence. |

## 8. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **`usage_metadata` shape drift** — `langchain-google-genai` returns different keys than expected. | Medium | High | `record()` reads keys defensively (`input_tokens`/`output_tokens`/`total_tokens`), derives `total` if absent, defaults missing to `0`; Test 4 pins the contract against a fixture, so drift fails a test, not a run. |
| **A bypassed call** not routed through `record()` → silent undercount. | Medium | High | All LLM access funnels through one helper in `agent/`; the call-budget check and `record()` sit together; CI asserts call count matches `ledger().runs[*].calls`. |
| **Secret leaks into the committed report** (key echoed in a `note` or error). | Low | High | `scrub()` runs on the write-path (Test 6 asserts no key in output) and on any logged ledger; only `.env.example` is committed (rule 9). |
| **Cap/ledger confusion** — someone caps the ledger to "save tokens". | Low | Medium | PRD + docstring state the ledger has NO cap and ALWAYS records; the cap lives only in `agent.max_llm_calls`. The ledger is evidence, never a throttle. |
| **Non-determinism** breaks golden table / honest diff. | Medium | Medium | Insertion-ordered rows, stable summation, no embedded timestamps in the table body; Test 7 enforces byte-identical renders. |
| **Apples-to-oranges comparison** (different bug/model across runs) voids C8. | Medium | High | Both runs target the same `TargetInfo` and the same model from config; `RunTotals` records the model; `success_to_root_cause` flags any run that "won" on cost but failed the task. |
| **Metric crash aborts a real run** (a missing field raising mid-investigation). | Low | Medium | Measurement never raises on a missing count — it records `0` and proceeds; the run's success is never sacrificed to a metric. |

---

*End of PRD. See `CLAUDE_CODE_PLAYBOOK.md` §1.5 (C8, C13, C15) and CLAUDE.md rule 13 (the Gatekeeper ledger is
the deliverable's evidence); `docs/PRD_target.md` (the `TargetInfo` both runs share) and `config/setup.json`
(`tokens.*`, `paths.reports_dir`).*
