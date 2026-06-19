# Contributing to COSMOS77-ex04

This document captures the working agreement for the two student contributors
(Abdallah Khaldi and Tasneem Natour) and any future maintainers. It mirrors the
17 binding rules in [CLAUDE.md](CLAUDE.md) and the master playbook
(`../CLAUDE_CODE_PLAYBOOK.md`).

## Local setup

```bash
# Install uv (one-time)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync the locked environment
uv sync

# Install pre-commit hooks
uv run pre-commit install
```

`uv sync` materialises `.venv/` and `uv.lock`. **Never** invoke `pip`,
`python -m venv`, or `python script.py` directly for OUR code — every Python
entry point goes through `uv run` (rule 5). The BugsInPy **target** project is
the one exception: it runs in its OWN isolated venv/Docker, separate from ours.

### System prerequisites (not pip dependencies)

- **Graphify CLI** — `uv tool install graphifyy` (package is `graphifyy`,
  command is `graphify`). Turns the target codebase into `graph.json` +
  `GRAPH_REPORT.md` + an Obsidian vault (Phase 3).
- A **free** `GOOGLE_API_KEY` (https://aistudio.google.com/apikey, no card). It
  lives in `.env` (gitignored) — never commit it (rule 9). Drives the
  graph-guided agent (Phase 6) and the naive baseline (Phase 8).
- **Docker** or a clean per-project **venv** to build + test the BugsInPy target
  in isolation (Phase 2).
- **Obsidian Desktop** (optional) only to *view* the generated vault for
  README screenshots.

## Branching

| Prefix      | Purpose                                                 |
|-------------|---------------------------------------------------------|
| `feat/`     | New capability (agent, parser, extractor, CLI command)  |
| `fix/`      | Bug fix that does not change the public surface         |
| `docs/`     | README, PRD, PLAN, TODO, prompt-log changes             |
| `chore/`    | Tooling, CI, configs, dependency bumps                  |
| `refactor/` | Internal restructuring with no behaviour change         |
| `test/`     | Adding or hardening tests only                          |

Always branch off `main`.

## Commits

Conventional Commits is mandatory (rule 11):

```
type(scope): short imperative summary

Optional body explaining the *why* and referencing the TODO ID.

Closes T-NNNN
```

Multiple commits per phase are encouraged; mega-commits (`wip`, `tmp`, `fixup`)
are forbidden — the grading agent flags them. This is a two-person team, so work
is authored by both partners across the commit history.

## Quality gates

Before pushing, run locally:

```bash
uv run ruff check .                 # zero issues
uv run ruff format --check .        # zero diffs
uv run python scripts/check_line_cap.py
uv run pytest -m "not live" --cov-fail-under=85
```

The same gates run in [GitHub Actions](.github/workflows/ci.yml) on every push
and pull request to `main`. **No test ever invokes the real Gemini API, the
Graphify CLI, BugsInPy, or git** — all LLM/subprocess/network I/O is mocked
(rule 6). Live end-to-end checks are marked `live` and excluded from CI.

## Test-driven development

Every public function or class lands tests **before** the implementation:

1. **Red** — write a failing test that captures the desired behaviour.
2. **Green** — write the smallest implementation that turns it green.
3. **Refactor** — clean up while keeping the tests green.

The project-wide coverage gate is ≥ 85%.

## Updating the TODO list

`docs/TODO.md` is the single source of truth for outstanding work. When you
complete a task, mark it done with the commit SHA. The list grows to ≥ 600
entries in Phase 1.

## The prompt log

Every Claude Code session writes a `docs/prompts/NNN_phase_name.md` file with the
prompt that was issued and a one-page summary of the agent's output. Treat it as
graded evidence of the vibe-coding methodology — never delete or rewrite it.

## Code of conduct

Be precise, be honest, cite sources for any external code, and never silently
disable a quality gate. The honest token ledger and the verified bug fix outrank
everything; never fabricate a token saving. If a rule genuinely cannot be
followed for a module, document the exception as an ADR in `docs/PLAN.md`.
