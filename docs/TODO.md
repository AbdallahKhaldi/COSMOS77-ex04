# TODO — COSMOS77-ex04

Single source of truth for outstanding work (CONTRIBUTING.md). Format:

`T-NNNN | phase | area | description | DoD (definition of done) | status`

Status ∈ `todo` · `doing` · `done`. Completed tasks carry the commit SHA.
Phase 1 expands this seed into the **≥ 600** granular tasks the playbook requires
(`../CLAUDE_CODE_PLAYBOOK.md` §0 / §3); this file currently tracks Phase 0 only.

## Phase 0 — Repo bootstrap

| ID | phase | area | description | DoD | status |
|----|-------|------|-------------|-----|--------|
| T-0001 | 0 | repo | Reconnaissance: tools (uv/gh/git/docker/graphify), gh auth, HW3 tooling to port | versions confirmed; port plan set | done |
| T-0002 | 0 | repo | Directory skeleton (`src/`, `tests/`, `docs/`, `config/`, `obsidian/`, `reports/`, `artifacts/`, `data/`, `logs/`) + package subpackages | tree matches playbook §2.2 task 1 | done |
| T-0003 | 0 | build | `pyproject.toml` — project `cosmos77-ex04` v1.00, py3.11, LangGraph/Gemini deps, dev group, ruff/coverage-85/pytest, `cosmos77-rev` script | `uv sync` resolves; uv.lock committed | done |
| T-0004 | 0 | build | `.python-version`, `.gitignore`, `.env.example` (no secrets) | `.env` ignored; only `.env.example` tracked | done |
| T-0005 | 0 | config | `config/setup.json` (BugsInPy tqdm target, venv isolation, agent caps) | parses; matches playbook | done |
| T-0006 | 0 | config | `config/providers.json` (Gemini active, provider-agnostic) + `config/logging_config.json` | parses; Gemini `gemini-2.5-flash` active | done |
| T-0007 | 0 | pkg | `src/cosmos77_ex04/__init__.py` (v1.00), `constants.py`, `cli/main.py` dispatcher, empty subpackages | package imports; `cosmos77-rev --version` works | done |
| T-0008 | 0 | rules | `CLAUDE.md` (17 rules verbatim, §16) | byte-matches playbook §16 body | done |
| T-0009 | 0 | docs | `README.md` placeholder, `LICENSE` (MIT 2026), `CHANGELOG.md` [1.00], `CONTRIBUTING.md` | all present; CI badge in README | done |
| T-0010 | 0 | ci | `scripts/check_line_cap.py` (port), `scripts/generate_cover_pdf.py` (port, ex04/exercise 4) | line-cap exits 0 | done |
| T-0011 | 0 | ci | `.pre-commit-config.yaml` + `.github/workflows/ci.yml` (ruff/format/line-cap/pytest-85; no live calls) | hooks installed; CI green | done |
| T-0012 | 0 | test | `tests/conftest.py` (seed) + `tests/unit/test_constants.py` smoke test | `uv run pytest` green, coverage ≥ 85% | done |
| T-0013 | 0 | qa | `uv sync`; `ruff check`/`ruff format --check` zero; `check_line_cap` 0; pytest ≥ 85% | every gate green | done |
| T-0014 | 0 | docs | `docs/prompts/000_phase0_bootstrap.md` prompt log | file present | done |
| T-0015 | 0 | git | `git init -b main`, identity + remote, conventional commits, `git push -u origin main`, CI green | Actions green on `main` | done |

## Phase 1 → 12 — placeholder

`T-0100`+ are authored in Phase 1 (PRD/PLAN/TODO + 9 mechanism PRDs), bringing the
list to ≥ 600 items distributed across P1–P12. See `../CLAUDE_CODE_PLAYBOOK.md`
§18 (phase index) for the per-phase deliverables.
