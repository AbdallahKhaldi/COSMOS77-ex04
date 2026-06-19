# Prompt log 012 — Phase 12: Cover PDF + tag + release + Moodle

**Phase:** 12 — Generate the cover PDF (exercise 4), tag, release, prep submission
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-19

## Prompt issued

> Phase 12 goal: generate `COSMOS77-ex04.pdf` from the template (exercise number =
> 4), tag, push, prep submission (`../CLAUDE_CODE_PLAYBOOK.md` §14). Reuse
> `scripts/generate_cover_pdf.py` with the verbatim field values (exercise 4,
> Group COSMOS77, self-score 85, both students, the ex04 GitHub link, late = no).
> Test asserts exercise = "4" and the ex04 repo URL. Confirm `*.pdf` gitignored;
> commit script/test only. Tag `v1.00`; release. Print the two manual steps.

## What was done

- **`tests/unit/test_scripts/test_cover.py`** — asserts the cover fields target
  **exercise 4**, Group `COSMOS77`, self-score `85`, late = `no`, and the **ex04**
  GitHub URL (`build_field_values` is pure and unit-tested).
- **Cover sheet filled** — `scripts/generate_cover_pdf.py` filled the template into
  `~/COSMOS77/HW4/COSMOS77-ex04.filled.docx` (exercise 4, both students, ex04 URL).
- **PDF render is a manual step** — `docx2pdf` needs Microsoft Word **automation
  permission** (a macOS GUI approval that cannot be granted from a non-interactive
  shell), and LibreOffice is not installed. The authors complete the one command
  below (approving the Word prompt once) — or open the filled `.docx` and export
  to PDF.
- `*.pdf` is gitignored (the cover PDF lives OUTSIDE the repo); only the script +
  test are committed.
- **Tag `v1.00`** + GitHub release.

## The command the authors run (one-time Word approval)

```bash
uvx --with python-docx --with docx2pdf python \
  ~/COSMOS77/HW4/COSMOS77-ex04/scripts/generate_cover_pdf.py \
  --template ~/COSMOS77/HW4/cover_template/uoh-rl07-ex01.docx \
  --output ~/COSMOS77/HW4/COSMOS77-ex04.pdf --self-score 85 --exercise-number 4
```

## The two things only the authors can do (§14.2)

1. **Visibility** — the repo is **public** (done) → the grader can access it.
   (Else add `rmisegal@gmail.com` at `/settings/access`.)
2. **Moodle** — Abdallah AND Tasneem each upload `~/COSMOS77/HW4/COSMOS77-ex04.pdf`
   to their own Moodle account (per-student timer).

## Status

All 13 phases complete; CI green; the failing test goes FAIL→PASS; the token
comparison is honest and reproduces (~40% fewer tokens, 2 vs 31 files).
Self-score **85**.
