# CLAUDE.md — Project rules of engagement (binding for every prompt)

HW4 (Graphify/Obsidian reverse-engineering + graph-guided debug agent) for Dr. Yoram
Segal's 203.3763 course. Every prompt inherits these rules. HW4 acceptance criteria
(C1–C15) are in ../CLAUDE_CODE_PLAYBOOK.md §1.5. We must PROVE, with honest numbers,
that graph-guided focused-context work beats naive raw-code reading.

## The 17 rules
1. 150-line hard cap per .py file. Split it.
2. SDK architecture: all business logic via class SDK in src/cosmos77_ex04/sdk/sdk.py.
3. OOP, no duplication. 2 files -> shared module; 3 -> base class/mixin.
4. Zero hardcoded config (target repo/bug, model, provider, paths, caps) -> config/*.json or .env.
5. uv only. Never pip / venv / python script.py (the project's OWN code uses uv; the
   BugsInPy TARGET runs in its own isolated venv/Docker — that's separate).
6. TDD red->green->refactor. Mock ALL LLM/graphify/BugsInPy/git/subprocess I/O. No live calls in tests.
7. Coverage >= 85%.
8. ruff check returns zero violations.
9. No secrets in repo. .env.example only; .env (GOOGLE_API_KEY) gitignored.
10. Versioning starts at 1.00 (version.py, every config, git tag v1.00).
11. Conventional Commits per task; reference TODO IDs.
12. Prompt log: every session -> docs/prompts/NNN_*.md.
13. Gatekeeper/token ledger: every LLM call routes through shared/gatekeeper.py; records
    usage_metadata tokens. This ledger IS the deliverable's evidence. Always measured.
14. CLI only (Claude Code terminal). The deliverable is a Python project that performs the
    investigation — never a hand-written walkthrough.
15. Docstrings on every public class/function/module (why, not what).
16. Type hints on every public signature. No bare Any.
17. Deterministic tests. Seed random. Mock I/O. No flakes.

## Language & vocabulary
English only. Use the professor's exact terms: Extracted/Inferred/Ambiguous edges, Context
Rot vs Overflow, Lost in the Middle, God Node vs healthy Hub, Centrality, Community, Bridge,
index.md as navigation hub, "question -> index -> 2-3 pages -> answer", guided retrieval.

## When in doubt
Less code, fewer deps, clearer docstrings. Impossible rule for a module -> ADR in
docs/PLAN.md. The honest token ledger + the verified bug fix outrank everything.
