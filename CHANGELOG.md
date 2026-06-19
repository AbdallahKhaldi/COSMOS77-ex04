# Changelog

All notable changes to COSMOS77-ex04 are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); the project uses a
single course-mandated version line starting at **1.00** (CLAUDE.md rule 10).

## [1.00] — 2026-06-19

### Added (Phase 0 — repo bootstrap)
- Repository scaffold: `src/cosmos77_ex04/` package skeleton (constants + CLI
  entry point + empty `sdk/`, `shared/`, `target/`, `graphify/`, `vault/`,
  `reveng/`, `agent/`, `tokens/`, `extensions/` subpackages), `tests/`,
  `docs/`, `config/`, and the deliverable directories `obsidian/`, `reports/`,
  `artifacts/`, `data/`.
- Tooling ported from `COSMOS77-ex03`: `pyproject.toml` (project `cosmos77-ex04`
  v1.00, Python `>=3.11,<3.12`, LangGraph + langchain-google-genai + networkx +
  matplotlib deps, dev group, ruff/coverage-85%/pytest config),
  `.pre-commit-config.yaml`, `.github/workflows/ci.yml`,
  `scripts/check_line_cap.py`, `scripts/generate_cover_pdf.py`.
- Configuration: `config/setup.json` (BugsInPy `tqdm` target, isolated venv,
  LangGraph agent caps), `config/providers.json` (Gemini active, provider-
  agnostic), `config/logging_config.json`. `.env.example` (no secrets).
- Governance: `CLAUDE.md` (the 17 binding rules), `CONTRIBUTING.md`, `LICENSE`
  (MIT 2026, both authors), `README.md` (placeholder, expanded in Phase 10).

[1.00]: https://github.com/AbdallahKhaldi/COSMOS77-ex04/releases/tag/v1.00
