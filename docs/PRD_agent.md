# PRD — `agent/`: The Graph-Guided LangGraph Debug Agent (THE CORE)

**Course:** UOH-RL07 — Vibe Coding & AI Agents (Dr. Yoram Segal) · **Assignment:** HW4
**Mechanism:** Graph-guided LangGraph + Gemini debug agent · **Maps to:** **C5** (and feeds C6/C8/C15)
**Authors:** Abdallah Khaldi, Tasneem Natour · **Version:** 1.00 · **Status:** Specification (Phase 1)
**Package root:** `src/cosmos77_ex04/agent/` · **Provider:** Google Gemini `gemini-2.5-flash`

---

## 1. Purpose

This is the heart of the grade. The agent must demonstrate, in running code, the thesis the whole
project defends: **graph-guided, focused-context investigation beats naive raw-file reading** on the
SAME real bug. It does this by enforcing one discipline — *"question → `index.md` → 2-3 pages →
answer"* — as an executable control flow.

The agent **consults the graph and the Obsidian vault FIRST** (`index.md` navigation hub, `hot.md`
bug-critical area, and a `graph.json` SUMMARY), ranks suspects by **Centrality** + **God Node**
status + **proximity to the failing test**, and only THEN requests the targeted source of the
**top-K suspects** — never the whole repository. A single bounded **LLM diagnose** call names the
bug and its root cause from this high-signal context. Every token is **MEASURED** through the
shared Gatekeeper ledger via `usage_metadata` — this ledger is the deliverable's evidence.

By construction the agent avoids the failure modes of naive reading: it raises **signal-to-noise**
(a few load-bearing pages, not ten raw files), it side-steps **Context Rot** (no weakly-relevant
padding), and it keeps the decisive lines out of the un-attended **Lost in the Middle** zone (the
prompt is small and ordered: suspects first). It is **graph-guided-FIRST** (`graph_guided_first=true`).

## 2. Inputs / Outputs

**Inputs**
- `obsidian/index.md` — navigation hub (read whole; it is small by design).
- `obsidian/hot.md` — God Nodes + the failing-test neighborhood (bug-critical area).
- `artifacts/graph.json` SUMMARY — top central nodes, communities, God Nodes, evidence tiers — NOT
  the full edge list, and **never** raw source files.
- `data/target/**` source files — read **lazily and selectively**, ONLY for ranked top-K suspects.
- The failing-test identifier (from `config/setup.json` → `target`), used as the proximity anchor.
- `config/setup.json` → `agent` block: `max_llm_calls=6`, `recursion_limit=12`,
  `max_output_tokens=4096`, `graph_guided_first=true`.
- `config/providers.json` → active provider (`gemini`, model `gemini-2.5-flash`, key env
  `GOOGLE_API_KEY`).

**Outputs**
- An `AgentResult` (returned by `SDK.run_agent()`): `diagnosis` (bug name + root cause), `suspects`
  (ranked, with evidence tier + why), `files_read` (the targeted snippets only), `iterations`
  (LLM-call count), and `tokens` (`{input_tokens, output_tokens, total_tokens}` from the ledger).
- `reports/BUG_ANALYSIS.md` — problem statement, suspects considered, the root cause, and **the
  path the graph led down** (index → hot.md → ranked suspects → targeted snippets → diagnosis).
- Ledger side effect: every LLM call appends `usage_metadata` to `shared/gatekeeper.py`. Phase 8
  reads this same ledger for the baseline-vs-guided comparison (C8/C15).

## 3. Module design (every `.py` ≤ 150 lines)

The package splits along single responsibilities so no file approaches the cap and each node is
unit-testable with mocked I/O.

| File | Responsibility | Cap |
|------|----------------|-----|
| `agent/state.py` | `TypedDict AgentState` + the reducer for `messages`; no logic | ≤ 60 |
| `agent/llm.py` | Provider factory: build `ChatGoogleGenerativeAI` from `providers.json` | ≤ 60 |
| `agent/nodes.py` | The five node functions (pure-ish; I/O injected/mockable) | ≤ 150 |
| `agent/graph.py` | Assemble + compile the `StateGraph`; route every LLM call via Gatekeeper | ≤ 150 |
| `agent/report.py` | Render `reports/BUG_ANALYSIS.md` from the final state | ≤ 90 |

**Split rule (CLAUDE.md #3):** if `nodes.py` nears the cap, the ranking heuristic moves to
`agent/ranking.py` (centrality + God-Node + proximity scoring) and snippet I/O to
`agent/snippets.py`; the node functions then become thin orchestrators. `graph.py` imports the
graph model from `graphify/model.py` (already typed `Node`/`Edge`, centrality, God Nodes,
communities) — the agent does **not** re-parse `graph.json`.

### 3.1 `agent/state.py` — `AgentState` (≤ 60 lines)

```python
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]  # LLM transcript (reducer-merged)
    failing_test: str                 # proximity anchor for ranking
    context_loaded: bool              # gate: True only after load_context ran
    suspects: list[Suspect]           # ranked top-K (id, file, score, tier, why)
    files_read: list[str]             # targeted snippet paths ONLY (audit trail)
    diagnosis: str | None             # set by diagnose; None until then
    step_count: int                   # LLM-call counter (hard cap)
    tokens: TokenTotals               # {input_tokens, output_tokens, total_tokens}
```

`Suspect` and `TokenTotals` are small `TypedDict`s in the same file (or imported from `constants`).
`messages` uses LangGraph's `add_messages` reducer so loop iterations append rather than overwrite.
The TypedDict carries **no source code** — only paths in `files_read` — keeping state lean.

### 3.2 `agent/nodes.py` — the five nodes

1. **`load_context`** — reads `index.md` + `hot.md` + the `graph.json` SUMMARY. **Reads NO raw
   source.** Cheap and focused: it loads the navigation hub and the bug-critical area, sets
   `context_loaded=True`, and seeds `messages` with a system prompt stating the failing test and the
   graph summary. This node makes the *graph-guided-FIRST* invariant literal.
2. **`rank_suspects`** — combines **Centrality** (betweenness/degree from the graph model), **God
   Node** flags, and **proximity to the failing test** (graph distance from the test's node) into a
   score; selects the **top-K** suspects (K from `constants.TOP_K_SUSPECTS`, default 3). Attaches each
   suspect's **evidence tier** (Extracted/Inferred/Ambiguous) and a one-line `why`. Pure function over
   the graph model — fully deterministic and unit-testable with a fixture graph.
3. **`request_snippets`** — fetches **ONLY** the source of the ranked top-K suspects (a targeted
   slice per suspect, not whole files where line ranges are known), appends each path to
   `files_read`. It **NEVER bulk-reads the repo**: it iterates over `state["suspects"]` exclusively,
   so the count of reads is bounded by K. This is the context-reduction mechanism in code.
4. **`diagnose`** — the single LLM call. Builds a focused prompt: failing test + graph summary +
   the K targeted snippets, and asks Gemini to **name the bug and its root cause**. The call goes
   **through the Gatekeeper** (Section 5); increments `step_count`; sets `diagnosis` when the model
   reports a confident root cause.
5. **`should_continue`** — conditional edge function: returns `END` when `diagnosis` is set OR
   `step_count >= max_llm_calls`; otherwise loops back to `rank_suspects` to widen K / re-rank with
   the model's feedback in `messages`.

### 3.3 `agent/graph.py` — assemble & compile

Builds the `StateGraph(AgentState)` with the linear spine and the diagnostic loop:

```
load_context → rank_suspects → request_snippets → diagnose → should_continue ─┬─ END
                     ▲────────────────────────────────────────────────────────┘ (loop)
```

`set_entry_point("load_context")`; conditional edge after `diagnose` via `should_continue`. Compiled
with `recursion_limit` from config (12) as the framework-level guard that backstops the in-state
`step_count` cap. The compiled app is invoked by `SDK.run_agent()`. **Every** LLM invocation is
wrapped so its `response.usage_metadata` is recorded in the Gatekeeper before the response is used.

### 3.4 `agent/llm.py` — provider factory (≤ 60 lines)

```python
def build_chat_model(cfg: Config) -> ChatGoogleGenerativeAI:
    p = cfg.get("providers.gemini")  # from providers.json
    return ChatGoogleGenerativeAI(
        model=p["model"],                       # gemini-2.5-flash
        temperature=0,                          # determinism
        max_output_tokens=cfg.get("agent.max_output_tokens"),  # 4096
    )  # API key read from GOOGLE_API_KEY env by the SDK
```

No hardcoded model/key (CLAUDE.md #4). In unit tests this factory is mocked; the real client is
constructed only in live runs.

## 4. The graph-guided-FIRST protocol

This is the protocol C5 grades and the reason the token ledger comes out ahead:

1. **Question → index.** The investigative question ("why does the failing test fail?") routes
   through `index.md`, the navigation hub — never through the repository tree.
2. **Index → 2-3 pages.** From `index.md` and `hot.md`, the agent reaches the bug-critical area: the
   God Nodes and the failing-test neighborhood. Still **zero raw source**.
3. **Rank, don't read.** `rank_suspects` orders nodes by Centrality + God-Node + proximity. The
   graph decides *what is worth a token*, before any code is loaded.
4. **Targeted snippets only.** `request_snippets` fetches the top-K suspects' source and nothing
   else. `files_read` is the audit trail proving the repo was never bulk-read.
5. **One focused diagnosis.** `diagnose` runs a single bounded LLM call over the high-signal
   context. If unresolved, the loop widens K — still guided, still bounded.

`graph_guided_first=true` makes step 1-2 a precondition: `diagnose` is unreachable until
`context_loaded` is True and `suspects` is non-empty. The agent **cannot** read source before the
graph.

## 5. Context-reduction mechanism (the proof, in construction)

Naive reading pays the full token cost of every file, dilutes **signal-to-noise**, invites **Context
Rot**, and buries the decisive function in the **Lost in the Middle** zone of a long dump. This agent
reduces context by three concrete levers:

- **Summaries over sources.** `load_context` reads a `graph.json` SUMMARY (top central nodes, God
  Nodes, communities, tiers) — a few hundred tokens — instead of the full graph or any file.
- **Top-K gating.** Only K suspect files reach the prompt. Token cost scales with K (≈3), not with
  repo size. `request_snippets` iterating strictly over `suspects` makes "no bulk read" a code
  invariant, not a hope.
- **Ordered, lean prompt.** The diagnose prompt puts the suspect snippets and failing test near the
  prompt's ends (high-attention positions), with the graph summary as compact framing — countering
  Lost in the Middle by construction.

**Measurement, not folklore.** Every `diagnose` call's `usage_metadata`
(`{input_tokens, output_tokens, total_tokens}`) is written to the **single** Gatekeeper ledger that
the Phase-8 baseline also writes to. The comparison reads ONE ledger, so it cannot be fudged. Note
`get_openai_callback` does **NOT** work with Gemini — tokens come from `response.usage_metadata`
directly into `shared/gatekeeper.py`.

## 6. Call / step caps

Two independent, deterministic bounds protect the free tier and make the ledger provable:

- **`max_llm_calls = 6`** — an in-`AgentState` `step_count` counter, incremented per `diagnose`
  call; `should_continue` returns `END` once `step_count >= max_llm_calls`. This is the semantic cap.
- **`recursion_limit = 12`** — the LangGraph compile-time guard backstopping the counter, so the
  graph can never spin even if a node misbehaves.
- **`max_output_tokens = 4096`** — per-call output bound on the Gemini client (`agent/llm.py`).

Because `temperature=0` and caps are deterministic, the call count and token totals are reproducible
across runs (CLAUDE.md #17) — essential for an honest comparison.

## 7. Public SDK API

All business logic flows through the single `class SDK` (CLAUDE.md #2). The agent surface is:

```python
class SDK:
    def run_agent(self) -> AgentResult:
        """Run the graph-guided investigation end to end.

        Loads index.md/hot.md/graph-summary FIRST, ranks suspects by centrality +
        God-Node + proximity, fetches ONLY top-K snippets, runs the bounded diagnose
        loop, records usage_metadata to the Gatekeeper ledger, and persists
        reports/BUG_ANALYSIS.md. Returns diagnosis, ranked suspects, files_read,
        iterations, and measured token totals.
        """
```

`AgentResult` (dataclass): `diagnosis: str`, `root_cause: str`, `suspects: list[Suspect]`,
`files_read: list[str]`, `iterations: int`, `tokens: TokenTotals`. The CLI (`cli/main.py`) exposes
`cosmos77-rev agent` which calls `SDK.run_agent()` and prints the diagnosis + counts. No other public
entry point; `agent/*` modules are internal to the SDK.

## 8. Test plan (TDD; mock LLM + file reads — CLAUDE.md #6)

Unit tests mock the Gemini client AND all file reads; **no live calls in the suite**. A small
fixture graph (a few nodes, one flagged God Node, a known failing-test node) drives ranking.

| Test | Asserts | Acceptance link |
|------|---------|-----------------|
| `test_load_context_before_any_source` | `load_context` reads index/hot/summary; `files_read == []` after it; source readers are NOT called yet | C5 (graph-first) |
| `test_graph_guided_first_invariant` | `diagnose` is unreachable while `context_loaded` is False / `suspects` empty | C5 |
| `test_rank_suspects_orders_by_score` | top-K reflects Centrality + God-Node + proximity; tiers attached; deterministic | C5/C14 |
| `test_request_snippets_only_ranked` | reads exactly the K suspect paths; **never bulk-reads the repo** (assert the bulk-read path is never called; `len(files_read) <= K`) | C5/C8 |
| `test_step_cap_halts_loop` | with a non-diagnosing mock LLM, the loop stops at `step_count == max_llm_calls` | C5 |
| `test_recursion_limit_backstop` | compiled graph honors `recursion_limit` from config | C5 |
| `test_ledger_records_tokens` | each mocked `usage_metadata` accrues into the Gatekeeper ledger; totals match | C8/C15 |
| `test_run_agent_persists_report` | `run_agent()` writes `reports/BUG_ANALYSIS.md` with problem, suspects, root cause, the graph path | C5/C6 |
| `test_llm_factory_from_config` | `build_chat_model` reads model/`max_output_tokens` from config; no hardcoding | C5 |

Coverage ≥ 85% on `agent/*`; `ruff check` zero; line-cap clean. Live Gemini is exercised only in the
Phase-6 manual verification (`uv run cosmos77-rev agent`), never in CI.

## 9. Acceptance-criteria mapping

| Criterion | How this mechanism satisfies it |
|-----------|--------------------------------|
| **C5** (primary) | Graph-guided LangGraph agent consults graph/Obsidian FIRST, ranks suspects, requests ONLY targeted snippets, bounded calls/steps, explained workflow (this PRD + `BUG_ANALYSIS.md`) |
| **C6** | Provides the diagnosis + root cause that Phase 7's fix acts on; `BUG_ANALYSIS.md` is its handoff |
| **C8** | The guided side of the comparison: its ledger entries + `files_read` + `iterations` are read by Phase 8 against the naive baseline |
| **C14** | Suspects carry Extracted/Inferred/Ambiguous tiers; God Node vs healthy Hub distinction drives ranking |
| **C15** | Every `diagnose` call records `usage_metadata` into the Gatekeeper ledger — the Token Spec Sheet's guided rows |

## 10. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Ranking misses the true suspect (top-K too small) | Medium | High | `should_continue` loop widens K with model feedback, still bounded by `max_llm_calls`; centrality extension (C9) hardens scoring; tests pin ordering on a fixture |
| `usage_metadata` absent/None on a Gemini response | Low | High | Gatekeeper treats missing metadata as a hard error (no silent zero); we never estimate tokens (NFR honest measurement) |
| Agent accidentally bulk-reads (regression) | Low | High | Code invariant: `request_snippets` iterates only `suspects`; a dedicated test asserts the bulk-read path is never called |
| Free-tier rate/quota limits during live run | Medium | Medium | `max_llm_calls=6` + `recursion_limit=12` + `temperature=0`; single diagnose call per iteration keeps usage minimal |
| `graph.json` summary too thin to rank well | Low | Medium | Summary derived from `graphify/model.py` (centrality, communities, God Nodes) — same typed model used everywhere; DIY ast+networkx fallback guarantees it exists |
| Modest measured savings on a small target (`tqdm`) | Medium | Low | Report the honest number with methodology (NFR); the *mechanism* — fewer files, fewer tokens, guided path — is the graded claim, not a target percentage |
| File approaching 150-line cap | Low | Low | Documented split: `ranking.py` + `snippets.py` peel off `nodes.py`; `report.py` already separate |
