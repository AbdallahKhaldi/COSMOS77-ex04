# COSMOS77-ex04 — Graphify/Obsidian Reverse-Engineering + Graph-Guided Debug Agent

> **UOH-RL07 — Vibe Coding & AI Agents (Dr. Yoram Segal) · HW4**
> Authors: **Abdallah Khaldi** (212389712) · **Tasneem Natour** (323118794)

[![CI](https://github.com/AbdallahKhaldi/COSMOS77-ex04/actions/workflows/ci.yml/badge.svg)](https://github.com/AbdallahKhaldi/COSMOS77-ex04/actions/workflows/ci.yml)

> ⚠️ **Placeholder README — expanded into the full lab report in Phase 10.**

## What this project proves

Take an unfamiliar, **buggy** Python project (a small but real
[BugsInPy](https://github.com/soarsmu/BugsInPy) target), turn it into a knowledge
graph with **Graphify**, build a navigable **Obsidian** vault (`index.md` nav hub
+ `hot.md` bug-critical area + linked investigation pages), and run a
**graph-guided LangGraph agent** that consults the graph/Obsidian *first* and
fetches **only** the ranked suspect snippets — never bulk-loading the repo. It
finds and fixes a real bug (the failing test goes **FAIL → PASS**) and proves,
with an **honest measured token ledger**, that graph-guided focused-context work
beats naive raw-code reading.

## Status

Bootstrapped in **Phase 0**. The pipeline is built phase-by-phase per
`../CLAUDE_CODE_PLAYBOOK.md`; see [`docs/TODO.md`](docs/TODO.md) for progress and
[`CLAUDE.md`](CLAUDE.md) for the 17 binding rules.

## Prerequisites (system, not pip)

- `uv` — the only package manager for our code.
- `graphify` CLI — `uv tool install graphifyy` (Phase 3).
- A free `GOOGLE_API_KEY` — https://aistudio.google.com/apikey (Phase 6/8).
- Docker or a clean venv for the isolated BugsInPy target (Phase 2).

## Quickstart

```bash
uv sync
cp .env.example .env          # add your free GOOGLE_API_KEY
uv run cosmos77-rev --version
```

## License

[MIT](LICENSE) © 2026 Abdallah Khaldi and Tasneem Natour.
