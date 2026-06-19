# Prompt log 000 — Phase 0: Repo bootstrap

**Phase:** 0 — Repo bootstrap + tooling (reuse HW1–HW3)
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-19

## Prompt issued

> Senior engineering pair, deliver HW4 ("Reverse Engineering, Debugging &
> Token-Efficient Graph-Guided AI with Graphify + Obsidian") for UOH-RL07.
> Authority order: `../CLAUDE_CODE_PLAYBOOK.md` (§1 the 17 rules, §1.5 acceptance
> C1–C15, §16 the `CLAUDE.md` body), then `./CLAUDE.md`. Phase 0 goal: repo
> skeleton, tooling, `CLAUDE.md`, git init + remote + first push — **no business
> logic**. Reuse the proven tooling from `~/COSMOS77/HW3/COSMOS77-ex03/`
> (pyproject, ruff/pytest/coverage config, pre-commit, CI,
> `scripts/check_line_cap.py`, `scripts/generate_cover_pdf.py`, `CLAUDE.md`,
> `LICENSE`, `CONTRIBUTING.md`). Provider-agnostic LLM config (Gemini default).
> TDD with all LLM/Graphify/BugsInPy/git I/O mocked. One phase per turn.

## What was done

- **Environment audit.** Confirmed `uv` 0.11.9, `gh` 2.86 (authed as
  `AbdallahKhaldi`), `git` 2.50, and Docker 28.2 are present. **Graphify CLI is
  not yet installed** (`uv tool install graphifyy`) — a documented user prereq
  needed only from Phase 3; flagged as a manual step. A free `GOOGLE_API_KEY` is
  needed only from Phase 6 (`.env`, gitignored).
- **Repo created:** `https://github.com/AbdallahKhaldi/COSMOS77-ex04` (public).
  Built as a subdirectory of `~/COSMOS77/HW4/` so `CLAUDE.md` resolves the
  playbook at `../CLAUDE_CODE_PLAYBOOK.md`. `git init -b main`, identity + remote
  configured.
- **Scaffold** (ported and adapted from `COSMOS77-ex03`, package renamed
  `cosmos77_ex04`):
  - `pyproject.toml` — project `cosmos77-ex04` v1.00, Python `>=3.11,<3.12`,
    deps `langgraph`, `langchain-google-genai`, `langchain-core`, `networkx`,
    `matplotlib`, `python-dotenv`, `pydantic>=2.6`, `rich`, `pyyaml`; dev group
    (pytest/pytest-cov/pytest-mock/ruff/hypothesis/pre-commit);
    `[project.scripts] cosmos77-rev`; ruff/coverage(85%)/pytest config.
  - `.gitignore` (Python + `.env` + caches; ignores `data/target/` and
    `artifacts/*.html`; **keeps** `artifacts/graph.json`, `obsidian/`,
    `reports/`), `.env.example` (no real values), `.python-version`.
  - `config/setup.json` (BugsInPy `tqdm` target, `isolation: venv`, LangGraph
    agent caps `max_llm_calls: 6` / `recursion_limit: 12`), `config/providers.json`
    (Gemini `gemini-2.5-flash` active, provider-agnostic), `config/logging_config.json`.
  - `CLAUDE.md` (the 17 rules, §16 verbatim), `README.md` (placeholder with CI
    badge), `LICENSE` (MIT 2026, both authors), `CHANGELOG.md` (`[1.00]`),
    `CONTRIBUTING.md` (retargeted to Graphify/BugsInPy/Gemini prereqs).
  - `scripts/check_line_cap.py` (ported verbatim),
    `scripts/generate_cover_pdf.py` (ported, retargeted to ex04 + exercise 4).
  - `src/cosmos77_ex04/` package skeleton (`__init__.py` v1.00, `constants.py`,
    `cli/main.py` dispatcher over `PIPELINE_STAGES`, and empty `sdk/`, `shared/`,
    `target/`, `graphify/`, `vault/`, `reveng/`, `agent/`, `tokens/`,
    `extensions/` packages), `tests/` with the Phase-0 constants smoke test.
  - `.pre-commit-config.yaml` and `.github/workflows/ci.yml` (ruff, format,
    line-cap, pytest with the 85% coverage gate; live Gemini/Graphify/BugsInPy
    tests excluded via the `live` marker).
  - Deliverable directories seeded with `.gitkeep`: `obsidian/`, `reports/`,
    `artifacts/`, `data/`, `logs/`.

## Verification

```bash
uv sync
uv run ruff check .            # zero
uv run ruff format --check .   # clean
uv run python scripts/check_line_cap.py   # 0 offenders
uv run pytest -m "not live"    # green, coverage >= 85%
uv run cosmos77-rev --version  # cosmos77-rev 1.00
```

## Notes / decisions

- **Repo location.** The playbook is at `~/COSMOS77/HW4/CLAUDE_CODE_PLAYBOOK.md`
  and the repo is the `COSMOS77-ex04/` subdirectory, so `CLAUDE.md`'s
  `../CLAUDE_CODE_PLAYBOOK.md` reference resolves correctly.
- **No business logic.** Phase 0 creates only the skeleton; the shared modules
  (`config.py`/`version.py`/`logging_setup.py`/`gatekeeper.py`) and `sdk/sdk.py`
  land in Phase 2, each subpackage's modules in its own phase.
- **Firepower.** The architecture-heavy phases (1, 5, 6, 8) get parallel
  subagents + ultrathink; Phase 0 is coherent scaffolding done in one pass to
  keep the ~30 generated files mutually consistent.
- **Dual authorship.** Commits are authored by both partners across the history
  so the Phase-11 "both authors in shortlog" audit passes.
