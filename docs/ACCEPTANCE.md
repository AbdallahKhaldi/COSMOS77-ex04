# ACCEPTANCE.md — HW4 acceptance criteria C1–C15 audit

Maps each acceptance criterion (`../CLAUDE_CODE_PLAYBOOK.md` §1.5) to the file /
report / artifact / test that satisfies it, with status. Verified 2026-06-19;
CI green; 190 tests, 98.8% coverage.

| # | Criterion | Evidence | Status |
|---|---|---|---|
| **C1** | Graphify run → `graph.json` + `GRAPH_REPORT.md` | `artifacts/graph.json` (500 nodes/1071 edges/28 communities) + `artifacts/GRAPH_REPORT.md`; built by `cosmos77-rev graphify` (`graphify/run.py`); parsed by `graphify/model.py`. | ✅ |
| **C2** | Obsidian vault (active knowledge space) | `obsidian/` — `index.md` (nav hub) + `hot.md` (bug-critical) + `suspects.md` + `investigation.md` + `fix-process.md` + 43 component/community pages; **all wikilinks resolve**. `vault/`. | ✅ |
| **C3** | Architectural block diagram (from the graph) | `artifacts/block_diagram.png` (28 communities + bridges) + Mermaid `flowchart` in `reports/ARCHITECTURE.md`; `reveng/block_diagram.py`. | ✅ |
| **C4** | OOP schema (from the code) | `artifacts/oop_schema.png` (32 classes) + Mermaid `classDiagram` in `reports/ARCHITECTURE.md`; `reveng/oop_schema.py` (AST). | ✅ |
| **C5** | Graph-guided LangGraph agent (graph-first, bounded) | `agent/` (StateGraph load_context→rank_suspects→request_snippets→diagnose); reads index/hot/graph + traceback FIRST, fetches ONLY ranked suspects (tested: never bulk-reads); `reports/BUG_ANALYSIS.md`. | ✅ |
| **C6** | A real bug fixed; failing test passes | `tqdm` bug 1 `test_enumerate` **FAIL → PASS** (`cosmos77-rev fix`); one-line diff in `obsidian/fix-process.md`; honesty guard in `agent/fix.py`; re-verified `1 passed` in the venv. | ✅ |
| **C7** | Before/after (code + knowledge) | Code: the unified diff (`fix-process.md`). Knowledge: `investigation.md` + `fix-process.md` added; `BUG_ANALYSIS.md` FAIL→PASS section; the new God-Node-contract insight. | ✅ |
| **C8** | Token comparison (honest) | `reports/TOKEN_COMPARISON.md` + `artifacts/token_comparison.{pdf,png}`: baseline 68,336 tokens/31 files vs guided 40,826/2 files = **−40.3% tokens, −93.5% files**, MEASURED from `usage_metadata`. | ✅ |
| **C9** | ≥1 original extension per part | `extensions/`: centrality `suspects.md`, dynamic `hot.md` (git diff ∩ graph), orphan detection (`reports/ORPHANS.md`), impact report (`reports/IMPACT.md`, "change `tqdm`" = 135 callers). | ✅ |
| **C10** | Rich README + visuals | `README.md` (497 lines, all §8 sections, 5 images + Mermaid; self-assessment 85). | ✅ |
| **C11** | Repo structure | `src/ tests/ obsidian/ reports/ artifacts/ data/` + `config/ docs/`. | ✅ |
| **C12** | Chosen repo + justification + research questions | README §3 (justification) + §5 (the §4 research questions, each answered) + `docs/PRD.md`. | ✅ |
| **C13** | Isolated environment + run instructions | uv Python 3.8.20 + pyshim, the target's own venv (`target/isolation.py`); README §14 run instructions. | ✅ |
| **C14** | Evidence tiers + God-Node distinction | Edge `confidence` → Extracted (813) / Inferred (258) / Ambiguous (0) in `graphify/model.py`; God Node (`tqdm`) vs 9 Hubs in `reveng/godnodes.py` + `ARCHITECTURE.md`. | ✅ |
| **C15** | Token Spec Sheet (ledger) | `reports/SPEC_SHEET.md` (per-run metrics) from `shared/gatekeeper.py` (records `usage_metadata`). | ✅ |

## Cross-cutting quality

- **17 rules:** 150-line cap (enforced, 0 offenders), single `class SDK` entry,
  uv-only (target in its own venv), TDD with all I/O mocked, ≥85% coverage (98.8%),
  ruff clean, no secrets (`.env` gitignored; only `.env.example`), version 1.00,
  Conventional Commits (45, both authors), per-phase prompt logs, the Gatekeeper
  ledger, CLI-only, docstrings + type hints, deterministic tests.
- **CI:** GitHub Actions green on every push; no live Gemini/Graphify/BugsInPy in
  the test suite (mocked).
- **Reproducibility:** fresh clone + `uv sync` + `.env` + `uv run cosmos77-rev run`
  reproduces the pipeline; `data/target/*` gitignored, artifacts committed.
