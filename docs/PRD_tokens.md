# PRD — `tokens/` Mechanism: THE PROOF (Naive vs Graph-Guided Token Comparison)

**Course:** Orchestration of AI Agents (203.3763), Dr. Yoram Segal · **Assignment:** HW4 · COSMOS77-ex04
**Maps to:** C8 (honest token-savings comparison) + C15 (committed Token Spec Sheet) · **Version:** 1.00
**Status:** Per-mechanism specification (Phase 8) · **Authors:** Abdallah Khaldi, Tasneem Natour

## 1. Purpose — the central claim this mechanism defends

This is **THE PROOF**. Every other part of the project (Graphify, the Obsidian vault, the
graph-guided LangGraph agent) exists so that this mechanism can make one defensible statement:
**graph-guided, focused-context debugging beats naive raw-file reading on the SAME bug**, measured
in tokens consumed, files/units read, iterations, and time-to-root-cause. The deliverable is an
**honest, MEASURED** comparison — never the folklore "70–95%". A measured 35% saving with a clear
methodology outranks a fabricated 95%. The mechanism instruments *both* arms of the experiment,
collects their numbers from one shared ledger, computes the deltas, renders a chart, and writes the
narrative. If savings are large we show the numbers; if modest, we **explain why** (small target,
Graphify semantic-extraction overhead) and never round up.

The "why" connects to Lecture 07: naive reading conflates *availability* with *relevance*. It pays
full token cost for every file, lowers signal-to-noise, and buries the one decisive function in the
**un-attended middle** (Lost in the Middle) — buying **Context Rot**, not safety. Graph-guided
retrieval pays for a few right pages. This mechanism turns that argument into numbers.

## 2. Inputs / Outputs

**Inputs:**
- The SAME prepared BugsInPy target the guided agent debugged (default `tqdm`, `config/setup.json
  → target`) — its source tree on disk under `data/target/` (gitignored, isolated venv).
- The guided run's numbers, already recorded in the Gatekeeper ledger (`shared/gatekeeper.py`)
  during the agent run — tokens (in/out/total), files read, iterations, time, success/root-cause.
- Config: `config/setup.json → tokens` (`baseline_mode: "raw_files"`, `guided_mode:
  "graph_guided"`, `measure: [...]`) and `agent.max_llm_calls` / `recursion_limit` as the cap basis.
- The active provider/model from `config/providers.json` (Gemini `gemini-2.5-flash`, free tier).

**Outputs:**
- `reports/TOKEN_COMPARISON.md` — the table + embedded chart + honest narrative (C8).
- `reports/SPEC_SHEET.md` — the committed Token Spec Sheet / ledger snapshot (C15).
- `artifacts/token_comparison.pdf` — matplotlib bar chart (tokens + files read, baseline vs guided).
- A structured `ComparisonResult` returned by `SDK.compare_tokens()` for programmatic use/tests.

## 3. Module design (files ≤ 150 lines — how to split)

All code lives under `src/cosmos77_ex04/tokens/` and routes through the single `class SDK`. No file
exceeds the 150-line cap; we split by single responsibility so each unit stays small and testable.

- **`tokens/baseline.py`** — the NAIVE agent. Runs the SAME bug WITHOUT the graph or Obsidian vault.
  Enumerates raw source files of the target (or the whole module), loads many of them into a single
  Gemini context, asks it to find the bug, and iterates (feed more files / refine) until it names a
  root cause or hits a **hard cap**. Every call goes through the Gatekeeper, so `usage_metadata` is
  recorded identically to the guided arm. Records: tokens, `files_read`, `iterations`,
  `time_to_root_cause`, `reached_root_cause: bool`. Exposes `run_baseline(target_dir, cap) ->
  BaselineResult`. If this file approaches the cap, split file-enumeration/ordering into
  `tokens/_corpus.py` (gather + deterministically order `.py` units) so `baseline.py` keeps only the
  iterate-and-measure loop.
- **`tokens/compare.py`** — pure aggregation, NO LLM. Reads the `BaselineResult` and the guided
  numbers from the Gatekeeper ledger, normalizes both into one `ArmMetrics` shape, and computes
  deltas and percentages (token Δ and %, files Δ and %, iterations Δ, time Δ, success parity).
  Exposes `compare(baseline, guided) -> ComparisonResult`. Deterministic and fully unit-testable
  with fixtures (no I/O beyond reading the in-memory ledger object).
- **`tokens/chart.py`** — rendering only. Takes a `ComparisonResult`, draws a grouped matplotlib bar
  chart (one panel for tokens in/out/total, one for files-read; baseline vs guided side by side),
  and writes `artifacts/token_comparison.pdf`. Uses the `Agg` backend (headless/CI-safe). Exposes
  `render(result, out_path) -> Path`.
- **`tokens/report.py`** — assembles `reports/TOKEN_COMPARISON.md` (table + chart embed + narrative)
  and `reports/SPEC_SHEET.md` from the `ComparisonResult`. Pure string/template work; honest-number
  formatting helper lives here (no rounding-up; truncate-toward-truth). Split out from `compare.py`
  so number-crunching and prose generation never share a file.
- **`tokens/models.py`** — small frozen dataclasses (`ArmMetrics`, `BaselineResult`,
  `ComparisonResult`) with type hints, shared by all of the above (rule 3: ≥2 users → shared module).

The `class SDK` orchestrates: `compare_tokens()` calls `baseline.run_baseline(...)`, pulls the
guided arm from the Gatekeeper, calls `compare.compare(...)`, then `chart.render(...)` and
`report.*`. The CLI is the only user boundary; it just calls the SDK.

## 4. Honest-measurement methodology (the non-negotiable core)

1. **Same bug, same model, same ledger.** Both arms debug the identical BugsInPy bug on
   `gemini-2.5-flash`, and **both write to the one `shared/gatekeeper.py` ledger** that records
   `response.usage_metadata` (prompt/candidates/total token counts) directly from Gemini. Because a
   single ledger is the source of truth, the comparison **cannot be fudged downstream**
   (ADR-005). Token numbers are MEASURED, never estimated, never rounded up.
2. **Naive arm is genuinely naive.** `baseline.py` must NOT consult `graph.json`, `index.md`,
   `hot.md`, centrality, or any guided artifact. It reads raw files in a deterministic order and
   stuffs them into context — exactly the practice the thesis criticizes (Context Rot / Lost in the
   Middle). This is the fair, unflattering control.
3. **Bounded so it can't run forever.** The baseline is capped independently (`max_iterations` and a
   token/file budget derived from config) so a free-tier loop cannot blow up. Reaching the cap
   WITHOUT the root cause is itself a valid, honest result — record it as `reached_root_cause:
   False` and report it.
4. **Symmetric metric definitions.** `files_read`, `iterations`, and `time_to_root_cause` are
   counted the same way for both arms (a file/unit "read" = its bytes entered an LLM context;
   an "iteration" = one LLM round-trip). No metric is defined to favor the guided arm.
5. **Report what happened, including ties/regressions.** If the guided arm used MORE tokens on a
   small target (because Graphify semantic-extraction has fixed overhead and `tqdm` is tiny), the
   narrative says so and explains the mechanism. Honesty is the grade, not the percentage (§7, C8).
6. **Reproducible.** Numbers are recomputed from the committed ledger + a fresh baseline run; the
   report records the model, target, bug id, caps, and timestamp so the experiment is auditable.

## 5. Public SDK API

All behavior is reached through `class SDK` (`src/cosmos77_ex04/sdk/sdk.py`); the CLI never imports
`tokens/*` directly. Signatures are fully type-hinted (rule 16) and docstringed (rule 15).

```python
class SDK:
    def compare_tokens(
        self,
        *,
        guided: ArmMetrics | None = None,   # default: pull guided arm from the Gatekeeper ledger
        write_reports: bool = True,         # emit TOKEN_COMPARISON.md + SPEC_SHEET.md + chart
    ) -> ComparisonResult:
        """Run the NAIVE baseline on the SAME bug, read the guided arm from the
        Gatekeeper ledger, compute honest deltas, and (optionally) write reports + chart.
        Why: this is THE PROOF — the measured evidence for the project's central claim."""

    def spec_sheet(self) -> Path:
        """Render the committed Token Spec Sheet (reports/SPEC_SHEET.md, C15) from the
        current Gatekeeper ledger snapshot. Why: the ledger IS the deliverable's evidence."""
```

`ComparisonResult` carries `baseline: ArmMetrics`, `guided: ArmMetrics`, the deltas
(`token_delta`, `token_pct`, `files_delta`, `files_pct`, `iter_delta`, `time_delta`), and
`narrative_kind: Literal["large_saving", "modest_saving", "no_saving"]` so the report module picks
the right honest framing without re-deriving it.

## 6. Test plan (LLM MOCKED — no live calls; rule 6 / 17)

TDD red→green→refactor; `random` seeded; ALL Gemini/subprocess/file-read I/O mocked. Fixtures live
under `tests/unit/tokens/`. Key cases:

- **Baseline reads broadly (fixture).** With a mocked LLM and a synthetic multi-file target, assert
  the baseline enumerates and reads MANY units, and that `BaselineResult.files_read` is large.
- **Guided reads narrowly → the load-bearing assertion.** Construct a guided `ArmMetrics` fixture
  (few files, via `index → 2–3 pages → answer`) and assert
  **`files_read_baseline > files_read_guided`** — the test that encodes the thesis (not a target %).
- **Baseline respects its cap.** A mocked LLM that NEVER finds the bug must terminate at
  `max_iterations`/budget with `reached_root_cause is False` — no infinite loop.
- **`compare.py` computes correct deltas.** Given two known `ArmMetrics`, assert exact
  `token_delta`, `token_pct`, `files_delta`, `files_pct`, and the correct `narrative_kind`
  (including the `no_saving` branch when guided ≥ baseline).
- **Honest formatting never rounds up.** Feed e.g. 34.7% and assert the rendered string is not
  "35%+" / inflated — truncates toward truth.
- **`chart.py` writes a non-empty PDF.** Call `render()` on a fixture `ComparisonResult` to a temp
  path; assert the file exists, is a valid PDF (`%PDF` header), and is non-empty.
- **Gatekeeper integration.** Assert both arms' calls increment the SAME ledger and that
  `compare_tokens()` reads the guided arm from it (one source of truth — un-fudgeable).
- **Reports render.** Assert `TOKEN_COMPARISON.md` contains the table, the chart embed, and an
  explanatory sentence when `narrative_kind == "no_saving"`.

Coverage for `tokens/*` must keep the project ≥ 85%; `ruff check` clean; every `.py` ≤ 150 lines.

## 7. Acceptance-criteria mapping

| Criterion | Obligation | Where satisfied |
|-----------|-----------|-----------------|
| **C8** | Honest naive-vs-guided comparison: tokens, files/units, iterations, quality/speed to root cause on the SAME bug | `baseline.py` + `compare.py` + `report.py` → `reports/TOKEN_COMPARISON.md`; chart in `artifacts/token_comparison.pdf`; narrative explains modest/no savings |
| **C15** | Commit the Token Spec Sheet (the ledger) as a report | `SDK.spec_sheet()` → `reports/SPEC_SHEET.md` from the Gatekeeper ledger snapshot |
| RQ (f) | Advantage of graph navigation vs linear reading | side-by-side `files_read`/path contrast in `TOKEN_COMPARISON.md` |
| RQ (g) | How the guided agent saved tokens | measured baseline-vs-guided deltas, one ledger |
| NFR Honest measurement | Both arms, SAME bug, `usage_metadata`, never rounded up | §4 methodology, formatting helper in `report.py` |

## 8. Risks & mitigations

- **Temptation to fake savings (High impact).** Mitigated by ONE Gatekeeper ledger for both arms
  (ADR-005) and tests that assert `files_read_baseline > files_read_guided` and exact deltas — not
  a target percentage. The report explains modest results rather than inflating them.
- **Small target → modest or inverted savings.** `tqdm` is small and Graphify carries fixed
  semantic-extraction overhead; the guided arm may not dominate on raw tokens. Mitigation: the
  `narrative_kind` branch produces an honest "modest / no saving" narrative that names the cause;
  this is an acceptable, graded outcome (honesty > percentage).
- **Free-tier rate/quota limits during the baseline run.** Mitigated by an independent baseline cap
  (`max_iterations` + token/file budget) and `temperature=0`; a cap-hit without root cause is a
  recorded, valid result.
- **Non-determinism / flaky chart rendering in CI.** Mitigated by the headless `Agg` backend, mocked
  LLM in the suite, seeded `random`, and asserting only the PDF's existence/validity, not pixels.
- **Metric definitions drifting between arms.** Mitigated by the shared `models.py` dataclasses and
  symmetric counting rules (§4.4); both arms emit the same `ArmMetrics` shape.
- **150-line cap pressure in `baseline.py`.** Mitigated by the planned split into `_corpus.py`
  (enumeration/ordering) so the measure loop stays small.
