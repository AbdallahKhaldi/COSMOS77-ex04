# Investigation — Graph-Guided Path to the Bug

**Failing test:** `tqdm/tests/tests_contrib.py::test_enumerate`

## Path (question → index → 2-3 pages → answer)
1. **Problem** — the failing test raised a `TypeError` deep in `std.py`.
2. **Index → hot.md** — the navigation hub pointed at the bug-critical area
   (the God Node `tqdm` and the failing-test neighbourhood).
3. **Suspects (Centrality + traceback)** — ranked the central nodes and the
   files named in the traceback; read ONLY those (2 files), not the repo.
4. **Root cause** — see [[fix-process]] and `reports/BUG_ANALYSIS.md`:
   `tqdm/contrib/__init__.py` passed an int positionally where a string was expected.

## Knowledge added (before → after)
- New pages: [[investigation]], [[fix-process]].
- New insight: the central `tqdm` constructor is a Bridge whose `desc`
  contract is violated by a caller — a cross-community defect the graph
  surfaced via the traceback, not by reading the whole repository.
