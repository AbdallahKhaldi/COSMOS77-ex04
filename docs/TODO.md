# TODO — COSMOS77-ex04 (UOH-RL07 HW4)

Single source of truth for ALL outstanding work. Each task is ONE line that begins
literally with `T-NNNN ` (four digits) and is pipe-delimited:

`T-NNNN | <phase 0-12> | <area> | <description> | <DoD = definition of done> | <status>`

Status is one of `todo` / `doing` / `done`. Tasks are numbered contiguously starting
at one (no gaps, no duplicates). The `## Phase N` subheadings group the blocks but are
not tasks (they do not start with the task prefix).
Granularity is deliberate: red test, green impl, refactor, docstrings/types, SDK
wiring, fixtures, gate runs, vault/report updates and commits are tracked separately.
Vocabulary follows the playbook: Extracted / Inferred / Ambiguous evidence tiers,
God Node, Centrality, Community, hot.md, guided retrieval, honest measurement.


## Phase 0 — Repo bootstrap

T-0001 | 0 | repo | Reconnaissance: confirm tools (uv/gh/git/docker/graphify), gh auth, HW3 tooling to port | versions confirmed; port plan recorded | done
T-0002 | 0 | repo | Directory skeleton (src/ tests/ docs/ config/ obsidian/ reports/ artifacts/ data/ logs/) + subpackages | tree matches playbook layout | done
T-0003 | 0 | build | pyproject.toml: project cosmos77-ex04 v1.00, py3.11, LangGraph/Gemini deps, dev group, ruff/coverage-85/pytest, console script | uv sync resolves; uv.lock committed | done
T-0004 | 0 | build | .python-version, .gitignore, .env.example (no secrets) | .env ignored; only .env.example tracked | done
T-0005 | 0 | config | config/setup.json (BugsInPy target, venv isolation, agent caps) | parses; matches playbook | done
T-0006 | 0 | config | config/providers.json (Gemini active, provider-agnostic) + logging_config.json | parses; gemini-2.5-flash active | done
T-0007 | 0 | docs | CLAUDE.md house rules (evidence tiers, gates, vocabulary) | present; references gates | done
T-0008 | 0 | scripts | scripts/ bootstrap + gate runner stubs executable | chmod +x; run without error | done
T-0009 | 0 | ci | .github/workflows CI (uv sync, ruff, pytest, coverage) | workflow file valid YAML | done
T-0010 | 0 | test | Smoke test tests/test_smoke.py importing package | pytest collects + passes | done
T-0011 | 0 | build | Pre-commit config (ruff, ruff-format, trailing-whitespace) | pre-commit run --all passes | done
T-0012 | 0 | docs | LICENSE + CONTRIBUTING.md + CHANGELOG.md seeded | files present | done
T-0013 | 0 | repo | Initial commit + create GitHub repo + push main | remote main has commit | done
T-0014 | 0 | ci | Trigger CI on push; confirm green | Actions run green | done
T-0015 | 0 | repo | Tag bootstrap checkpoint; verify clean working tree | git status clean; checkpoint noted | done

## Phase 1 — Docs (PRD/PLAN/TODO + 9 mechanism PRDs)

T-0016 | 1 | docs | Write docs/PRD.md (problem, goals, non-goals, success criteria C1-C15) | PRD covers all acceptance criteria | done
T-0017 | 1 | docs | Write docs/PLAN.md (12-phase roadmap, gates, deliverables) | PLAN lists all phases + gates | done
T-0018 | 1 | docs | Seed docs/TODO.md ledger format + Phase 0 block | format documented; Phase 0 listed | done
T-0019 | 1 | docs | Define evidence tiers (Extracted / Inferred / Ambiguous) in PRD | three tiers defined w/ rules | done
T-0020 | 1 | docs | Define guided-retrieval + honest-measurement principles in PRD | principles stated | done
T-0021 | 1 | docs | PRD_target.md — scope, interfaces, inputs/outputs for BugsInPy target harness | mechanism PRD drafted | done
T-0022 | 1 | docs | PRD_target.md — DoD, gates, and test matrix for BugsInPy target harness | DoD + gates listed | done
T-0023 | 1 | docs | PRD_target.md — risks, fallbacks, and open questions for BugsInPy target harness | risks enumerated | done
T-0024 | 1 | docs | PRD_target.md — review + cross-link from PLAN/PRD for BugsInPy target harness | cross-links resolve | todo
T-0025 | 1 | docs | PRD_graphify.md — scope, interfaces, inputs/outputs for Graphify graph extraction | mechanism PRD drafted | done
T-0026 | 1 | docs | PRD_graphify.md — DoD, gates, and test matrix for Graphify graph extraction | DoD + gates listed | done
T-0027 | 1 | docs | PRD_graphify.md — risks, fallbacks, and open questions for Graphify graph extraction | risks enumerated | done
T-0028 | 1 | docs | PRD_graphify.md — review + cross-link from PLAN/PRD for Graphify graph extraction | cross-links resolve | todo
T-0029 | 1 | docs | PRD_vault.md — scope, interfaces, inputs/outputs for Obsidian knowledge vault | mechanism PRD drafted | done
T-0030 | 1 | docs | PRD_vault.md — DoD, gates, and test matrix for Obsidian knowledge vault | DoD + gates listed | done
T-0031 | 1 | docs | PRD_vault.md — risks, fallbacks, and open questions for Obsidian knowledge vault | risks enumerated | done
T-0032 | 1 | docs | PRD_vault.md — review + cross-link from PLAN/PRD for Obsidian knowledge vault | cross-links resolve | todo
T-0033 | 1 | docs | PRD_reveng.md — scope, interfaces, inputs/outputs for Reverse-engineering analysis | mechanism PRD drafted | done
T-0034 | 1 | docs | PRD_reveng.md — DoD, gates, and test matrix for Reverse-engineering analysis | DoD + gates listed | done
T-0035 | 1 | docs | PRD_reveng.md — risks, fallbacks, and open questions for Reverse-engineering analysis | risks enumerated | done
T-0036 | 1 | docs | PRD_reveng.md — review + cross-link from PLAN/PRD for Reverse-engineering analysis | cross-links resolve | todo
T-0037 | 1 | docs | PRD_agent.md — scope, interfaces, inputs/outputs for Graph-guided LangGraph agent | mechanism PRD drafted | done
T-0038 | 1 | docs | PRD_agent.md — DoD, gates, and test matrix for Graph-guided LangGraph agent | DoD + gates listed | done
T-0039 | 1 | docs | PRD_agent.md — risks, fallbacks, and open questions for Graph-guided LangGraph agent | risks enumerated | done
T-0040 | 1 | docs | PRD_agent.md — review + cross-link from PLAN/PRD for Graph-guided LangGraph agent | cross-links resolve | todo
T-0041 | 1 | docs | PRD_fix.md — scope, interfaces, inputs/outputs for Bug-fix workflow | mechanism PRD drafted | done
T-0042 | 1 | docs | PRD_fix.md — DoD, gates, and test matrix for Bug-fix workflow | DoD + gates listed | done
T-0043 | 1 | docs | PRD_fix.md — risks, fallbacks, and open questions for Bug-fix workflow | risks enumerated | done
T-0044 | 1 | docs | PRD_fix.md — review + cross-link from PLAN/PRD for Bug-fix workflow | cross-links resolve | todo
T-0045 | 1 | docs | PRD_tokens.md — scope, interfaces, inputs/outputs for Token comparison study | mechanism PRD drafted | done
T-0046 | 1 | docs | PRD_tokens.md — DoD, gates, and test matrix for Token comparison study | DoD + gates listed | done
T-0047 | 1 | docs | PRD_tokens.md — risks, fallbacks, and open questions for Token comparison study | risks enumerated | done
T-0048 | 1 | docs | PRD_tokens.md — review + cross-link from PLAN/PRD for Token comparison study | cross-links resolve | todo
T-0049 | 1 | docs | PRD_extensions.md — scope, interfaces, inputs/outputs for Centrality/hot/orphans/impact extensions | mechanism PRD drafted | done
T-0050 | 1 | docs | PRD_extensions.md — DoD, gates, and test matrix for Centrality/hot/orphans/impact extensions | DoD + gates listed | done
T-0051 | 1 | docs | PRD_extensions.md — risks, fallbacks, and open questions for Centrality/hot/orphans/impact extensions | risks enumerated | done
T-0052 | 1 | docs | PRD_extensions.md — review + cross-link from PLAN/PRD for Centrality/hot/orphans/impact extensions | cross-links resolve | todo
T-0053 | 1 | docs | PRD_report.md — scope, interfaces, inputs/outputs for Lab report + release | mechanism PRD drafted | done
T-0054 | 1 | docs | PRD_report.md — DoD, gates, and test matrix for Lab report + release | DoD + gates listed | done
T-0055 | 1 | docs | PRD_report.md — risks, fallbacks, and open questions for Lab report + release | risks enumerated | done
T-0056 | 1 | docs | PRD_report.md — review + cross-link from PLAN/PRD for Lab report + release | cross-links resolve | todo
T-0057 | 1 | docs | Phase-1 doc consistency pass #42 (terminology, links, headings) | no broken links; terms consistent | todo
T-0058 | 1 | docs | Phase-1 doc consistency pass #43 (terminology, links, headings) | no broken links; terms consistent | todo
T-0059 | 1 | docs | Phase-1 doc consistency pass #44 (terminology, links, headings) | no broken links; terms consistent | todo
T-0060 | 1 | docs | Phase-1 doc consistency pass #45 (terminology, links, headings) | no broken links; terms consistent | todo

## Phase 2 — Shared infra port + BugsInPy target harness (isolated venv)

T-0061 | 2 | infra | Port HW3 logging utility (structured JSON logs) into src/cosmos77/util/logging.py | module imports; emits JSON | todo
T-0062 | 2 | infra | Write failing test for logging util (red) | test asserts JSON keys; fails | todo
T-0063 | 2 | infra | Implement logging util to pass test (green) | test passes | todo
T-0064 | 2 | infra | Refactor logging util + add type hints/docstrings | ruff clean; mypy clean | todo
T-0065 | 2 | infra | Port config loader (setup.json/providers.json) into src/cosmos77/config.py | loads all configs | todo
T-0066 | 2 | infra | Write failing test for config loader (red) | test fails on missing key | todo
T-0067 | 2 | infra | Implement config loader (green) | test passes | todo
T-0068 | 2 | infra | Add Pydantic models for config schema + validation | invalid config raises | todo
T-0069 | 2 | infra | Port path resolver (repo-root-relative paths) util | resolves artifacts/ data/ logs/ | todo
T-0070 | 2 | infra | Write + pass test for path resolver | test passes | todo
T-0071 | 2 | infra | Port retry/backoff decorator from HW3 | decorator retries N times | todo
T-0072 | 2 | infra | Test retry decorator (red then green) | flaky-stub test passes | todo
T-0073 | 2 | infra | Port deterministic seed/RNG helper | seed reproducible | todo
T-0074 | 2 | infra | Add CLI skeleton (Typer) with sub-commands stubbed | --help lists subcommands | todo
T-0075 | 2 | infra | Test CLI --help and version | exit 0; version printed | todo
T-0076 | 2 | target | Pick BugsInPy target project + bug id; record in config/setup.json | target + bug id pinned | todo
T-0077 | 2 | target | Write src/cosmos77/target/harness.py module skeleton | module imports | todo
T-0078 | 2 | target | Write failing test: harness checkout of buggy revision (red) | test fails (no checkout) | todo
T-0079 | 2 | target | Implement BugsInPy checkout (buggy version) in harness | checkout succeeds | todo
T-0080 | 2 | target | Make checkout test pass (green) | test passes | todo
T-0081 | 2 | target | Implement isolated venv creation per target (uv venv) | venv created under data/ | todo
T-0082 | 2 | target | Test isolated venv is separate from project venv | sys.prefix differs | todo
T-0083 | 2 | target | Install target deps into isolated venv | pip list shows target deps | todo
T-0084 | 2 | target | Implement compile/import sanity check of target | target imports in venv | todo
T-0085 | 2 | target | Test import sanity check | test passes | todo
T-0086 | 2 | target | Implement run-failing-test entrypoint (subprocess into venv) | returns test result obj | todo
T-0087 | 2 | target | Write failing test for run-failing-test wrapper (red) | test fails | todo
T-0088 | 2 | target | Implement run wrapper parsing pytest output | parses pass/fail counts | todo
T-0089 | 2 | target | Make run wrapper test pass (green) | test passes | todo
T-0090 | 2 | target | Capture baseline: confirm target bug test FAILS | FAIL recorded in artifacts | todo
T-0091 | 2 | target | Implement fixed-version checkout path (reference) | fixed rev checks out | todo
T-0092 | 2 | target | Confirm fixed-version test PASSES (reference oracle) | PASS recorded | todo
T-0093 | 2 | target | Persist baseline result to artifacts/baseline.json | JSON written | todo
T-0094 | 2 | target | Test baseline persistence round-trip | load==dump | todo
T-0095 | 2 | target | Add timeout + resource caps to subprocess runner | timeout enforced | todo
T-0096 | 2 | target | Test timeout cap triggers on hang | TimeoutError raised | todo
T-0097 | 2 | target | Capture stdout/stderr/return-code into result object | fields populated | todo
T-0098 | 2 | target | Redact secrets/paths from captured output (sanitize) | no abs home paths leak | todo
T-0099 | 2 | target | Test sanitizer redaction | redacted strings absent | todo
T-0100 | 2 | infra | Wire harness into CLI subcommand `target prepare` | CLI prepares target | todo
T-0101 | 2 | infra | Wire CLI subcommand `target run-test` | CLI runs failing test | todo
T-0102 | 2 | infra | Add fixture: tmp target sandbox for tests | fixture yields sandbox | todo
T-0103 | 2 | infra | Add fixture: mocked subprocess for fast unit tests | fixture mocks Popen | todo
T-0104 | 2 | target | Snapshot target source tree into data/target_src/ (read-only copy) | tree copied | todo
T-0105 | 2 | target | Test snapshot integrity (file count/hash) | hash matches | todo
T-0106 | 2 | infra | Add error taxonomy (HarnessError, CheckoutError, TargetTestError) | exceptions defined | todo
T-0107 | 2 | infra | Test error taxonomy raised on expected failures | each raised in case | todo
T-0108 | 2 | infra | Add structured run-ledger writer (append-only JSONL) | ledger appends | todo
T-0109 | 2 | infra | Test run-ledger append + read | entries round-trip | todo
T-0110 | 2 | infra | Add docstrings + type hints across target package | ruff/mypy clean | todo
T-0111 | 2 | infra | Run coverage gate on Phase-2 modules (>=85%) | coverage gate green | todo
T-0112 | 2 | infra | Update docs/PRD_target.md with implemented interfaces | PRD matches code | todo
T-0113 | 2 | infra | Update reports/ with Phase-2 progress note | note written | todo
T-0114 | 2 | infra | Commit Phase-2 infra port | commit pushed; CI green | todo
T-0115 | 2 | infra | Phase-2 hardening task #55: edge-case test + fix (target harness) | new edge case covered | todo
T-0116 | 2 | infra | Phase-2 hardening task #56: edge-case test + fix (target harness) | new edge case covered | todo
T-0117 | 2 | infra | Phase-2 hardening task #57: edge-case test + fix (target harness) | new edge case covered | todo
T-0118 | 2 | infra | Phase-2 hardening task #58: edge-case test + fix (target harness) | new edge case covered | todo
T-0119 | 2 | infra | Phase-2 hardening task #59: edge-case test + fix (target harness) | new edge case covered | todo
T-0120 | 2 | infra | Phase-2 hardening task #60: edge-case test + fix (target harness) | new edge case covered | todo
T-0121 | 2 | infra | Phase-2 hardening task #61: edge-case test + fix (target harness) | new edge case covered | todo
T-0122 | 2 | infra | Phase-2 hardening task #62: edge-case test + fix (target harness) | new edge case covered | todo
T-0123 | 2 | infra | Phase-2 hardening task #63: edge-case test + fix (target harness) | new edge case covered | todo
T-0124 | 2 | infra | Phase-2 hardening task #64: edge-case test + fix (target harness) | new edge case covered | todo
T-0125 | 2 | infra | Phase-2 hardening task #65: edge-case test + fix (target harness) | new edge case covered | todo
T-0126 | 2 | infra | Phase-2 hardening task #66: edge-case test + fix (target harness) | new edge case covered | todo
T-0127 | 2 | infra | Phase-2 hardening task #67: edge-case test + fix (target harness) | new edge case covered | todo
T-0128 | 2 | infra | Phase-2 hardening task #68: edge-case test + fix (target harness) | new edge case covered | todo
T-0129 | 2 | infra | Phase-2 hardening task #69: edge-case test + fix (target harness) | new edge case covered | todo
T-0130 | 2 | infra | Phase-2 hardening task #70: edge-case test + fix (target harness) | new edge case covered | todo

## Phase 3 — Graphify run + graph.json parser (tiers, centrality, god_nodes)

T-0131 | 3 | graphify | Write src/cosmos77/graph/runner.py to invoke Graphify on target_src | module imports | todo
T-0132 | 3 | graphify | Write failing test: Graphify runner produces graph.json (red) | test fails | todo
T-0133 | 3 | graphify | Implement Graphify invocation (subprocess) + capture graph.json | graph.json written | todo
T-0134 | 3 | graphify | Make Graphify runner test pass (green) | test passes | todo
T-0135 | 3 | graphify | Add Graphify config (languages, include/exclude globs) | config honored | todo
T-0136 | 3 | graphify | Persist raw graph.json to artifacts/graph/raw.json | file present | todo
T-0137 | 3 | parser | Define dataclasses Node/Edge/Graph in src/cosmos77/graph/model.py | types defined | todo
T-0138 | 3 | parser | Write failing test for graph.json parser (red) | test fails | todo
T-0139 | 3 | parser | Implement graph.json parser -> Graph object (green) | parses sample | todo
T-0140 | 3 | parser | Add schema validation for graph.json (Pydantic) | bad json raises | todo
T-0141 | 3 | parser | Test parser on malformed graph.json | raises clear error | todo
T-0142 | 3 | parser | Normalize node ids + dedupe edges | no dup edges | todo
T-0143 | 3 | parser | Test edge dedupe + id normalization | counts correct | todo
T-0144 | 3 | tiers | Define evidence tiers Extracted/Inferred/Ambiguous in src/cosmos77/graph/tiers.py | enum + rules | todo
T-0145 | 3 | tiers | Write failing test for tier classification (red) | test fails | todo
T-0146 | 3 | tiers | Implement tier classifier (Extracted=in graph, Inferred=derived, Ambiguous=uncertain) | green | todo
T-0147 | 3 | tiers | Tag every node/edge with an evidence tier | all tagged | todo
T-0148 | 3 | tiers | Test tier coverage (no untagged nodes) | 100% tagged | todo
T-0149 | 3 | centrality | Add src/cosmos77/graph/centrality.py (degree centrality) | function returns dict | todo
T-0150 | 3 | centrality | Write failing test for degree centrality (red) | test fails | todo
T-0151 | 3 | centrality | Implement degree centrality (green) | test passes on toy graph | todo
T-0152 | 3 | centrality | Implement betweenness centrality | values computed | todo
T-0153 | 3 | centrality | Test betweenness on known toy graph | matches expected | todo
T-0154 | 3 | centrality | Implement pagerank/eigenvector centrality | converges | todo
T-0155 | 3 | centrality | Test pagerank sums ~1.0 | assertion holds | todo
T-0156 | 3 | centrality | Combine centralities into ranked centrality table | ranked list | todo
T-0157 | 3 | centrality | Persist centrality table to artifacts/graph/centrality.json | file present | todo
T-0158 | 3 | centrality | Test centrality persistence round-trip | load==dump | todo
T-0159 | 3 | godnode | Add src/cosmos77/graph/god_nodes.py detector | module imports | todo
T-0160 | 3 | godnode | Write failing test for God Node detection (red) | test fails | todo
T-0161 | 3 | godnode | Implement God Node detection (high centrality + high fan-in/out) | green | todo
T-0162 | 3 | godnode | Define God Node threshold heuristic + make configurable | threshold in config | todo
T-0163 | 3 | godnode | Test God Node threshold boundary cases | boundaries correct | todo
T-0164 | 3 | godnode | Rank god_nodes and persist to artifacts/graph/god_nodes.json | file present | todo
T-0165 | 3 | godnode | Test god_nodes persistence | round-trip ok | todo
T-0166 | 3 | community | Add community detection (Louvain/label-prop) module | communities returned | todo
T-0167 | 3 | community | Write failing test for community detection (red) | test fails | todo
T-0168 | 3 | community | Implement community detection (green) | >=1 community on toy | todo
T-0169 | 3 | community | Assign each node a community id | all assigned | todo
T-0170 | 3 | community | Test community assignment coverage | 100% assigned | todo
T-0171 | 3 | community | Persist communities to artifacts/graph/communities.json | file present | todo
T-0172 | 3 | parser | Add graph stats (node/edge counts, density, components) | stats dict | todo
T-0173 | 3 | parser | Test graph stats on toy graph | values match | todo
T-0174 | 3 | parser | Add orphan/leaf detection (degree-0 / sink nodes) | orphans listed | todo
T-0175 | 3 | parser | Test orphan detection | matches expected | todo
T-0176 | 3 | graphify | Add CLI subcommand `graph build` (run+parse+analyze) | CLI produces artifacts | todo
T-0177 | 3 | graphify | Test `graph build` end-to-end on fixture | artifacts created | todo
T-0178 | 3 | graphify | Add fixture: small synthetic graph.json | fixture loads | todo
T-0179 | 3 | graphify | Add fixture: real target graph.json snapshot | fixture loads | todo
T-0180 | 3 | parser | Sanitize graph (strip abs paths, secrets) before persist | no leaks | todo
T-0181 | 3 | parser | Test graph sanitizer | redactions present | todo
T-0182 | 3 | graphify | Add docstrings + type hints across graph package | ruff/mypy clean | todo
T-0183 | 3 | graphify | Run coverage gate on graph package (>=85%) | gate green | todo
T-0184 | 3 | graphify | Emit graph summary report to reports/graph_summary.md | report written | todo
T-0185 | 3 | graphify | Test graph summary report generation | file non-empty | todo
T-0186 | 3 | graphify | Update docs/PRD_graphify.md with implemented interfaces | PRD matches code | todo
T-0187 | 3 | graphify | Update PLAN gate checklist for Phase 3 | gate items checked | todo
T-0188 | 3 | graphify | Commit Phase-3 graph pipeline | commit pushed; CI green | todo
T-0189 | 3 | graphify | Cross-check god_nodes vs centrality top-K consistency | overlap reported | todo
T-0190 | 3 | graphify | Phase-3 graph robustness task #60: edge case + regression test | case covered | todo

## Phase 4 — Obsidian vault (index nav hub + hot.md + component/suspect pages)

T-0191 | 4 | vault | Add src/cosmos77/vault/builder.py skeleton (vault generator) | module imports | todo
T-0192 | 4 | vault | Define vault layout (index.md, hot.md, components/, suspects/) | layout doc | todo
T-0193 | 4 | vault | Write failing test: index.md nav hub generated (red) | test fails | todo
T-0194 | 4 | vault | Implement index.md nav hub generator (links to all pages) | green | todo
T-0195 | 4 | vault | Test index.md contains links to components+suspects | links present | todo
T-0196 | 4 | vault | Implement hot.md generator (top god_nodes + centrality) | hot.md written | todo
T-0197 | 4 | vault | Write failing test for hot.md content (red) | test fails | todo
T-0198 | 4 | vault | Make hot.md test pass (green) | top-K nodes listed | todo
T-0199 | 4 | vault | Add evidence-tier badges to hot.md entries | tiers shown | todo
T-0200 | 4 | vault | Implement component page generator (one per module/community) | pages written | todo
T-0201 | 4 | vault | Write failing test for component page (red) | test fails | todo
T-0202 | 4 | vault | Make component page test pass (green) | page has summary+links | todo
T-0203 | 4 | vault | Implement suspect page generator (per god_node/suspect) | pages written | todo
T-0204 | 4 | vault | Write failing test for suspect page (red) | test fails | todo
T-0205 | 4 | vault | Make suspect page test pass (green) | page has evidence+links | todo
T-0206 | 4 | vault | Implement wikilink helper [[Page]] with slugging | links resolve | todo
T-0207 | 4 | vault | Test wikilink slugging + dedupe | no broken links | todo
T-0208 | 4 | vault | Implement backlink section per page | backlinks listed | todo
T-0209 | 4 | vault | Test backlink generation | reciprocal links | todo
T-0210 | 4 | vault | Implement frontmatter (tags, tier, centrality) per page | YAML frontmatter valid | todo
T-0211 | 4 | vault | Test frontmatter parses as YAML | valid YAML | todo
T-0212 | 4 | vault | Implement vault sanitize (strip abs paths/secrets) | no leaks | todo
T-0213 | 4 | vault | Test vault sanitizer | redactions present | todo
T-0214 | 4 | vault | Add Mermaid mini-graph embed to component pages | mermaid block present | todo
T-0215 | 4 | vault | Test Mermaid block well-formed | parses | todo
T-0216 | 4 | vault | Add 'Extracted/Inferred/Ambiguous' legend to index.md | legend present | todo
T-0217 | 4 | vault | Implement orphans page (degree-0 nodes) | page written | todo
T-0218 | 4 | vault | Test orphans page | lists orphans | todo
T-0219 | 4 | vault | Add CLI subcommand `vault build` | CLI builds vault | todo
T-0220 | 4 | vault | Test `vault build` end-to-end on fixture | vault dir populated | todo
T-0221 | 4 | vault | Validate vault: every link target exists (link checker) | 0 broken links | todo
T-0222 | 4 | vault | Write failing test for link checker (red) | test fails | todo
T-0223 | 4 | vault | Implement link checker (green) | detects broken link | todo
T-0224 | 4 | vault | Add stable ordering (sorted) for deterministic vault output | diff stable | todo
T-0225 | 4 | vault | Test deterministic vault build (re-run equals) | byte-identical | todo
T-0226 | 4 | vault | Add per-page 'last-built' + provenance note | provenance present | todo
T-0227 | 4 | vault | Add cross-links hot.md <-> suspects <-> components | links bidirectional | todo
T-0228 | 4 | vault | Test cross-link integrity | all resolve | todo
T-0229 | 4 | vault | Add tag index page (group pages by tag) | tag index written | todo
T-0230 | 4 | vault | Test tag index | tags grouped | todo
T-0231 | 4 | vault | Embed centrality table into hot.md as markdown table | table present | todo
T-0232 | 4 | vault | Test centrality table rendering | rows match data | todo
T-0233 | 4 | vault | Add 'how to read this vault' note to index.md | note present | todo
T-0234 | 4 | vault | Snapshot generated vault to obsidian/vault/ | files present | todo
T-0235 | 4 | vault | Test vault snapshot file count | count matches pages | todo
T-0236 | 4 | vault | Add docstrings + type hints across vault package | ruff/mypy clean | todo
T-0237 | 4 | vault | Run coverage gate on vault package (>=85%) | gate green | todo
T-0238 | 4 | vault | Update docs/PRD_vault.md with implemented interfaces | PRD matches code | todo
T-0239 | 4 | vault | Update reports/ with vault build summary | summary written | todo
T-0240 | 4 | vault | Commit Phase-4 vault generator | commit pushed; CI green | todo
T-0241 | 4 | vault | Phase-4 vault polish task #51: rendering edge case + test | case covered | todo
T-0242 | 4 | vault | Phase-4 vault polish task #52: rendering edge case + test | case covered | todo
T-0243 | 4 | vault | Phase-4 vault polish task #53: rendering edge case + test | case covered | todo
T-0244 | 4 | vault | Phase-4 vault polish task #54: rendering edge case + test | case covered | todo
T-0245 | 4 | vault | Phase-4 vault polish task #55: rendering edge case + test | case covered | todo
T-0246 | 4 | vault | Phase-4 vault polish task #56: rendering edge case + test | case covered | todo
T-0247 | 4 | vault | Phase-4 vault polish task #57: rendering edge case + test | case covered | todo
T-0248 | 4 | vault | Phase-4 vault polish task #58: rendering edge case + test | case covered | todo
T-0249 | 4 | vault | Phase-4 vault polish task #59: rendering edge case + test | case covered | todo
T-0250 | 4 | vault | Phase-4 vault polish task #60: rendering edge case + test | case covered | todo

## Phase 5 — Reverse-engineering (block diagram + OOP schema + God-Node/centrality)

T-0251 | 5 | reveng | Add src/cosmos77/reveng/analyzer.py skeleton | module imports | todo
T-0252 | 5 | reveng | Write failing test: block diagram model built from graph (red) | test fails | todo
T-0253 | 5 | reveng | Implement block diagram model (components -> blocks) | green | todo
T-0254 | 5 | reveng | Render block diagram as Mermaid | mermaid emitted | todo
T-0255 | 5 | reveng | Test Mermaid block diagram well-formed | parses | todo
T-0256 | 5 | reveng | Render block diagram PNG via mermaid-cli | PNG written | todo
T-0257 | 5 | reveng | Test PNG file produced + non-empty | size>0 | todo
T-0258 | 5 | reveng | Add fallback if mermaid-cli missing (skip+warn) | graceful skip | todo
T-0259 | 5 | reveng | Build OOP schema model (classes, methods, inheritance) | schema dict | todo
T-0260 | 5 | reveng | Write failing test for OOP schema extraction (red) | test fails | todo
T-0261 | 5 | reveng | Implement OOP schema extraction from graph (green) | classes listed | todo
T-0262 | 5 | reveng | Render OOP class diagram as Mermaid | classDiagram emitted | todo
T-0263 | 5 | reveng | Test class diagram Mermaid | parses | todo
T-0264 | 5 | reveng | Render OOP class diagram PNG | PNG written | todo
T-0265 | 5 | reveng | God-Node analysis writeup (why these are god nodes) | writeup md | todo
T-0266 | 5 | reveng | Write failing test for god-node analysis section (red) | test fails | todo
T-0267 | 5 | reveng | Implement god-node analysis generator (green) | section populated | todo
T-0268 | 5 | reveng | Centrality analysis writeup (interpret rankings) | writeup md | todo
T-0269 | 5 | reveng | Test centrality analysis section | contains top-K | todo
T-0270 | 5 | reveng | Community/responsibility mapping writeup | writeup md | todo
T-0271 | 5 | reveng | Test community writeup | communities described | todo
T-0272 | 5 | reveng | Assemble reports/reverse_engineering.md (full doc) | doc assembled | todo
T-0273 | 5 | reveng | Embed block diagram + class diagram + PNG links in report | embeds present | todo
T-0274 | 5 | reveng | Test report embeds resolve | links valid | todo
T-0275 | 5 | reveng | Mark each claim with evidence tier (Extracted/Inferred/Ambiguous) | claims tiered | todo
T-0276 | 5 | reveng | Test all claims carry a tier | 100% tagged | todo
T-0277 | 5 | reveng | Add data-flow narrative (entry points -> god nodes) | narrative present | todo
T-0278 | 5 | reveng | Test data-flow section | mentions entry points | todo
T-0279 | 5 | reveng | Add CLI subcommand `reveng build` | CLI builds report | todo
T-0280 | 5 | reveng | Test `reveng build` end-to-end | report + diagrams produced | todo
T-0281 | 5 | reveng | Sanitize report (strip abs paths/secrets) | no leaks | todo
T-0282 | 5 | reveng | Test reveng sanitizer | redactions present | todo
T-0283 | 5 | reveng | Deterministic diagram ordering | stable diff | todo
T-0284 | 5 | reveng | Test deterministic reveng output | re-run equal | todo
T-0285 | 5 | reveng | Link reveng report into vault index.md | link present | todo
T-0286 | 5 | reveng | Test vault link to reveng | resolves | todo
T-0287 | 5 | reveng | Add suspect-ranking section (likely bug locations) | ranking present | todo
T-0288 | 5 | reveng | Test suspect ranking section | ordered list | todo
T-0289 | 5 | reveng | Cross-link suspects to vault suspect pages | links resolve | todo
T-0290 | 5 | reveng | Add 'honest measurement' caveats to inferred claims | caveats present | todo
T-0291 | 5 | reveng | Test caveats present on Inferred claims | each flagged | todo
T-0292 | 5 | reveng | Add diagram legend + tier color key | legend present | todo
T-0293 | 5 | reveng | Generate PNG thumbnails for embedding | thumbs written | todo
T-0294 | 5 | reveng | Test thumbnail generation | files present | todo
T-0295 | 5 | reveng | Add docstrings + type hints across reveng package | ruff/mypy clean | todo
T-0296 | 5 | reveng | Run coverage gate on reveng package (>=85%) | gate green | todo
T-0297 | 5 | reveng | Update docs/PRD_reveng.md with implemented interfaces | PRD matches code | todo
T-0298 | 5 | reveng | Peer-review pass on reverse_engineering.md | review notes addressed | todo
T-0299 | 5 | reveng | Update reports/ index with reveng artifact | index updated | todo
T-0300 | 5 | reveng | Commit Phase-5 reverse engineering | commit pushed; CI green | todo
T-0301 | 5 | reveng | Phase-5 analysis depth task #51: refine interpretation + test | refinement covered | todo
T-0302 | 5 | reveng | Phase-5 analysis depth task #52: refine interpretation + test | refinement covered | todo
T-0303 | 5 | reveng | Phase-5 analysis depth task #53: refine interpretation + test | refinement covered | todo
T-0304 | 5 | reveng | Phase-5 analysis depth task #54: refine interpretation + test | refinement covered | todo
T-0305 | 5 | reveng | Phase-5 analysis depth task #55: refine interpretation + test | refinement covered | todo
T-0306 | 5 | reveng | Phase-5 analysis depth task #56: refine interpretation + test | refinement covered | todo
T-0307 | 5 | reveng | Phase-5 analysis depth task #57: refine interpretation + test | refinement covered | todo
T-0308 | 5 | reveng | Phase-5 analysis depth task #58: refine interpretation + test | refinement covered | todo
T-0309 | 5 | reveng | Phase-5 analysis depth task #59: refine interpretation + test | refinement covered | todo
T-0310 | 5 | reveng | Phase-5 analysis depth task #60: refine interpretation + test | refinement covered | todo

## Phase 6 — Graph-guided LangGraph agent (state/nodes/graph/llm, caps, ledger)

T-0311 | 6 | agent | Add src/cosmos77/agent/ package skeleton | package imports | todo
T-0312 | 6 | agent | Define AgentState (TypedDict): task, plan, evidence, retrieved, ledger, caps | state defined | todo
T-0313 | 6 | agent | Write failing test for AgentState init (red) | test fails | todo
T-0314 | 6 | agent | Implement AgentState defaults (green) | test passes | todo
T-0315 | 6 | llm | Add src/cosmos77/agent/llm.py provider wrapper (Gemini via providers.json) | wrapper imports | todo
T-0316 | 6 | llm | Write failing test for llm wrapper (mocked) (red) | test fails | todo
T-0317 | 6 | llm | Implement llm wrapper call + response parsing (green) | mocked call passes | todo
T-0318 | 6 | llm | Add token accounting to llm wrapper (prompt/completion) | tokens recorded | todo
T-0319 | 6 | llm | Test token accounting | counts captured | todo
T-0320 | 6 | llm | Add provider-agnostic interface (swap provider via config) | interface stable | todo
T-0321 | 6 | llm | Test provider swap (mock alt provider) | swaps cleanly | todo
T-0322 | 6 | nodes | Implement node: load_graph_context (read graph artifacts) | context loaded | todo
T-0323 | 6 | nodes | Write failing test for load_graph_context (red) | test fails | todo
T-0324 | 6 | nodes | Make load_graph_context test pass (green) | context populated | todo
T-0325 | 6 | nodes | Implement node: guided_retrieval (graph-first: god_nodes+centrality) | retrieves ranked nodes | todo
T-0326 | 6 | nodes | Write failing test for guided_retrieval ordering (red) | test fails | todo
T-0327 | 6 | nodes | Make guided_retrieval test pass (green) | graph-first order | todo
T-0328 | 6 | nodes | Implement node: plan (LLM produces investigation plan) | plan produced | todo
T-0329 | 6 | nodes | Test plan node (mocked llm) | plan in state | todo
T-0330 | 6 | nodes | Implement node: inspect_code (fetch source for retrieved nodes) | code fetched | todo
T-0331 | 6 | nodes | Test inspect_code node | snippets in state | todo
T-0332 | 6 | nodes | Implement node: hypothesize (LLM bug hypothesis from evidence) | hypothesis produced | todo
T-0333 | 6 | nodes | Test hypothesize node (mocked) | hypothesis in state | todo
T-0334 | 6 | nodes | Implement node: propose_fix (LLM proposes patch) | patch proposed | todo
T-0335 | 6 | nodes | Test propose_fix node (mocked) | patch in state | todo
T-0336 | 6 | nodes | Implement node: verify (run target failing test) | verify result in state | todo
T-0337 | 6 | nodes | Test verify node (mocked harness) | result captured | todo
T-0338 | 6 | nodes | Implement node: update_ledger (append decisions/evidence) | ledger grows | todo
T-0339 | 6 | nodes | Test update_ledger node | entries appended | todo
T-0340 | 6 | graph | Build LangGraph StateGraph wiring nodes + edges | graph compiles | todo
T-0341 | 6 | graph | Write failing test: graph compiles + runs one step (red) | test fails | todo
T-0342 | 6 | graph | Make graph compile test pass (green) | compiles | todo
T-0343 | 6 | graph | Add conditional edges (retry on verify fail, stop on pass) | branches wired | todo
T-0344 | 6 | graph | Test conditional routing (pass vs fail) | routes correctly | todo
T-0345 | 6 | graph | Add graph-first protocol guard: must consult graph before code | guard enforced | todo
T-0346 | 6 | graph | Write failing test for graph-first guard (red) | test fails | todo
T-0347 | 6 | graph | Implement graph-first guard (green) | violation blocked | todo
T-0348 | 6 | caps | Add caps: max steps, max llm calls, max tokens, wall-clock | caps in state | todo
T-0349 | 6 | caps | Write failing test for step cap (red) | test fails | todo
T-0350 | 6 | caps | Implement step cap enforcement (green) | halts at cap | todo
T-0351 | 6 | caps | Implement llm-call cap enforcement | halts at cap | todo
T-0352 | 6 | caps | Test llm-call cap | halts | todo
T-0353 | 6 | caps | Implement token cap enforcement | halts at cap | todo
T-0354 | 6 | caps | Test token cap | halts | todo
T-0355 | 6 | caps | Implement wall-clock timeout | halts on time | todo
T-0356 | 6 | caps | Test wall-clock timeout | halts | todo
T-0357 | 6 | ledger | Define decision-ledger schema (step, node, action, evidence, tier) | schema defined | todo
T-0358 | 6 | ledger | Write failing test for ledger schema (red) | test fails | todo
T-0359 | 6 | ledger | Implement ledger writer JSONL (green) | ledger written | todo
T-0360 | 6 | ledger | Persist ledger to artifacts/agent/ledger.jsonl | file present | todo
T-0361 | 6 | ledger | Test ledger persistence round-trip | entries reload | todo
T-0362 | 6 | ledger | Add evidence-tier tagging to every ledger entry | tiers present | todo
T-0363 | 6 | ledger | Test ledger tier coverage | 100% tagged | todo
T-0364 | 6 | agent | Add retrieval-cache to avoid duplicate fetches | cache hits logged | todo
T-0365 | 6 | agent | Test retrieval cache | second fetch cached | todo
T-0366 | 6 | agent | Add CLI subcommand `agent run` | CLI runs agent | todo
T-0367 | 6 | agent | Test `agent run` end-to-end (mocked llm+harness) | completes | todo
T-0368 | 6 | agent | Add dry-run mode (no llm calls, deterministic) | dry-run completes | todo
T-0369 | 6 | agent | Test dry-run determinism | re-run equal | todo
T-0370 | 6 | agent | Add structured run summary (steps, tokens, result) | summary emitted | todo
T-0371 | 6 | agent | Test run summary fields | fields present | todo
T-0372 | 6 | agent | Add error handling for llm failures (retry/backoff) | retries on error | todo
T-0373 | 6 | agent | Test llm failure handling | recovers/halts | todo
T-0374 | 6 | agent | Add prompt templates (system, retrieval, hypothesis, fix) | templates loaded | todo
T-0375 | 6 | agent | Test prompt template rendering | renders w/ context | todo
T-0376 | 6 | agent | Inject vault hot.md context into retrieval prompt | hot.md cited | todo
T-0377 | 6 | agent | Test hot.md injection | context includes hot | todo
T-0378 | 6 | agent | Sanitize prompts/logs (no secrets) | no leaks | todo
T-0379 | 6 | agent | Test prompt sanitizer | redactions present | todo
T-0380 | 6 | agent | Add deterministic seed for agent reproducibility | seed honored | todo
T-0381 | 6 | agent | Test agent reproducibility | same trace | todo
T-0382 | 6 | agent | Add docstrings + type hints across agent package | ruff/mypy clean | todo
T-0383 | 6 | agent | Run coverage gate on agent package (>=85%) | gate green | todo
T-0384 | 6 | agent | Update docs/PRD_agent.md with implemented interfaces | PRD matches code | todo
T-0385 | 6 | agent | Update reports/ with agent design note | note written | todo
T-0386 | 6 | agent | Render agent graph topology diagram (Mermaid) | diagram emitted | todo
T-0387 | 6 | agent | Commit Phase-6 graph-guided agent | commit pushed; CI green | todo
T-0388 | 6 | agent | Phase-6 agent robustness task #78: scenario test + fix | scenario covered | todo
T-0389 | 6 | agent | Phase-6 agent robustness task #79: scenario test + fix | scenario covered | todo
T-0390 | 6 | agent | Phase-6 agent robustness task #80: scenario test + fix | scenario covered | todo

## Phase 7 — Fix the bug (FAIL->PASS + before/after code + knowledge)

T-0391 | 7 | fix | Confirm baseline: target bug test FAILS (red oracle) | FAIL captured | todo
T-0392 | 7 | fix | Record before-code snapshot of buggy file(s) | snapshot saved | todo
T-0393 | 7 | fix | Run agent to localize bug via graph guidance | suspect ranked | todo
T-0394 | 7 | fix | Capture agent-identified suspect + evidence tier | suspect recorded | todo
T-0395 | 7 | fix | Cross-check agent suspect vs reveng suspect ranking | agreement noted | todo
T-0396 | 7 | fix | Derive minimal fix hypothesis from evidence | hypothesis written | todo
T-0397 | 7 | fix | Implement candidate patch in isolated target copy | patch applied | todo
T-0398 | 7 | fix | Run target failing test against patched copy | result captured | todo
T-0399 | 7 | fix | If FAIL: iterate hypothesis (debug loop) | iteration logged | todo
T-0400 | 7 | fix | Achieve target test FAIL -> PASS | PASS captured | todo
T-0401 | 7 | fix | Run full target test suite (no regressions) | suite green | todo
T-0402 | 7 | fix | Capture after-code snapshot of fixed file(s) | snapshot saved | todo
T-0403 | 7 | fix | Generate unified diff (before/after code) | diff produced | todo
T-0404 | 7 | fix | Write before/after knowledge note (what changed + why) | note written | todo
T-0405 | 7 | fix | Link fix to god_node/centrality evidence in note | evidence cited | todo
T-0406 | 7 | fix | Tag fix-note claims with evidence tiers | tiers present | todo
T-0407 | 7 | fix | Persist fix artifacts to artifacts/fix/ | files present | todo
T-0408 | 7 | fix | Write failing test asserting fix harness reports PASS (red) | test fails | todo
T-0409 | 7 | fix | Implement fix-verification wrapper (green) | reports PASS | todo
T-0410 | 7 | fix | Test fix-verification wrapper | passes | todo
T-0411 | 7 | fix | Add regression guard: re-run baseline still FAILS unpatched | FAIL confirmed | todo
T-0412 | 7 | fix | Test regression guard | confirms FAIL/PASS delta | todo
T-0413 | 7 | fix | Update vault suspect page with confirmed fix | page updated | todo
T-0414 | 7 | fix | Update hot.md to mark resolved suspect | hot.md updated | todo
T-0415 | 7 | fix | Add CLI subcommand `fix apply` + `fix verify` | CLI applies+verifies | todo
T-0416 | 7 | fix | Test `fix apply`/`fix verify` end-to-end | PASS reported | todo
T-0417 | 7 | fix | Sanitize fix artifacts (no abs paths/secrets) | no leaks | todo
T-0418 | 7 | fix | Test fix-artifact sanitizer | redactions present | todo
T-0419 | 7 | fix | Write reports/fix_report.md (problem, root cause, fix, evidence) | report written | todo
T-0420 | 7 | fix | Embed before/after diff in fix_report.md | diff embedded | todo
T-0421 | 7 | fix | Embed test FAIL->PASS evidence in report | logs embedded | todo
T-0422 | 7 | fix | Document agent decision-ledger excerpt in report | excerpt present | todo
T-0423 | 7 | fix | Record token/step cost of the fix run | cost recorded | todo
T-0424 | 7 | fix | Cross-link fix_report into vault + reveng | links resolve | todo
T-0425 | 7 | fix | Test cross-links | resolve | todo
T-0426 | 7 | fix | Add 'honest measurement' note (limits of localization) | note present | todo
T-0427 | 7 | fix | Deterministic fix replay (same patch from same inputs) | replay stable | todo
T-0428 | 7 | fix | Test fix replay determinism | re-run equal | todo
T-0429 | 7 | fix | Validate diff applies cleanly to fresh checkout | apply succeeds | todo
T-0430 | 7 | fix | Test clean-apply on fresh checkout | applies+PASS | todo
T-0431 | 7 | fix | Add minimality check (no unrelated edits) | diff minimal | todo
T-0432 | 7 | fix | Test minimality (line-count bound) | within bound | todo
T-0433 | 7 | fix | Run coverage gate on fix module (>=85%) | gate green | todo
T-0434 | 7 | fix | Add docstrings + type hints across fix module | ruff/mypy clean | todo
T-0435 | 7 | fix | Update docs/PRD_fix.md with implemented interfaces | PRD matches code | todo
T-0436 | 7 | fix | Peer-review fix_report.md | review addressed | todo
T-0437 | 7 | fix | Update CHANGELOG with fix entry | entry present | todo
T-0438 | 7 | fix | Commit Phase-7 bug fix + report | commit pushed; CI green | todo
T-0439 | 7 | fix | Verify CI runs fix-verification on clean runner | CI green | todo
T-0440 | 7 | fix | Capture screenshot/log of PASS for README | artifact saved | todo
T-0441 | 7 | fix | Record before/after metrics (tests passing count) | metrics recorded | todo
T-0442 | 7 | fix | Confirm no secrets in committed fix artifacts | scan clean | todo
T-0443 | 7 | fix | Tag fix milestone note in reports/ | milestone noted | todo
T-0444 | 7 | fix | Reconcile fix suspect with Phase-3 god_nodes list | reconciled | todo
T-0445 | 7 | fix | Phase-7 fix validation task #55: extra check + test | check covered | todo

## Phase 8 — Token comparison (naive baseline vs guided, chart, honest narrative)

T-0446 | 8 | tokens | Add src/cosmos77/study/ package skeleton | package imports | todo
T-0447 | 8 | tokens | Define naive baseline agent (no graph guidance, full-context) | baseline defined | todo
T-0448 | 8 | tokens | Write failing test for naive baseline run (red) | test fails | todo
T-0449 | 8 | tokens | Implement naive baseline run (green, mocked llm) | completes | todo
T-0450 | 8 | tokens | Instrument naive baseline token counting | tokens recorded | todo
T-0451 | 8 | tokens | Test naive baseline token capture | counts present | todo
T-0452 | 8 | tokens | Define guided agent run reuse (Phase-6 agent) | reuses agent | todo
T-0453 | 8 | tokens | Instrument guided run token counting | tokens recorded | todo
T-0454 | 8 | tokens | Test guided token capture | counts present | todo
T-0455 | 8 | tokens | Implement comparison harness (run both, collect metrics) | metrics dict | todo
T-0456 | 8 | tokens | Write failing test for comparison harness (red) | test fails | todo
T-0457 | 8 | tokens | Make comparison harness test pass (green) | both runs compared | todo
T-0458 | 8 | tokens | Collect metrics: prompt tokens, completion tokens, total | metrics complete | todo
T-0459 | 8 | tokens | Collect metrics: steps, llm calls, wall-clock, result | metrics complete | todo
T-0460 | 8 | tokens | Compute deltas + reduction % (guided vs naive) | deltas computed | todo
T-0461 | 8 | tokens | Test delta computation | math correct | todo
T-0462 | 8 | tokens | Persist comparison to artifacts/study/comparison.json | file present | todo
T-0463 | 8 | tokens | Test comparison persistence | round-trip ok | todo
T-0464 | 8 | tokens | Run multiple trials (N runs) for variance | trials recorded | todo
T-0465 | 8 | tokens | Compute mean/stddev across trials | stats computed | todo
T-0466 | 8 | tokens | Test trial aggregation | stats correct | todo
T-0467 | 8 | tokens | Add chart: token usage bar chart (matplotlib) | PNG written | todo
T-0468 | 8 | tokens | Write failing test for chart generation (red) | test fails | todo
T-0469 | 8 | tokens | Make chart generation test pass (green) | PNG non-empty | todo
T-0470 | 8 | tokens | Add chart: steps/llm-calls comparison | PNG written | todo
T-0471 | 8 | tokens | Test second chart | PNG present | todo
T-0472 | 8 | tokens | Add chart: cost estimate (tokens*price) | PNG written | todo
T-0473 | 8 | tokens | Test cost chart | PNG present | todo
T-0474 | 8 | tokens | Write reports/token_comparison.md (honest narrative) | report written | todo
T-0475 | 8 | tokens | State methodology + what is measured/not measured | methodology section | todo
T-0476 | 8 | tokens | Add honest-measurement caveats (mocked vs live, variance) | caveats present | todo
T-0477 | 8 | tokens | Embed charts + table in token_comparison.md | embeds present | todo
T-0478 | 8 | tokens | Test report embeds resolve | links valid | todo
T-0479 | 8 | tokens | Tag report claims with evidence tiers | tiers present | todo
T-0480 | 8 | tokens | Add CLI subcommand `study compare` | CLI runs study | todo
T-0481 | 8 | tokens | Test `study compare` end-to-end | artifacts produced | todo
T-0482 | 8 | tokens | Add dry-run/mocked mode for deterministic study | deterministic | todo
T-0483 | 8 | tokens | Test study determinism | re-run equal | todo
T-0484 | 8 | tokens | Sanitize study artifacts (no secrets) | no leaks | todo
T-0485 | 8 | tokens | Test study sanitizer | redactions present | todo
T-0486 | 8 | tokens | Add results table (naive vs guided) to report | table present | todo
T-0487 | 8 | tokens | Test results table rendering | rows match data | todo
T-0488 | 8 | tokens | Add conclusion: when guidance helps / fails honestly | conclusion present | todo
T-0489 | 8 | tokens | Cross-link study into vault + README | links resolve | todo
T-0490 | 8 | tokens | Test cross-links | resolve | todo
T-0491 | 8 | tokens | Add reproducibility note (seeds, config, versions) | note present | todo
T-0492 | 8 | tokens | Record provider/model + token prices used | recorded | todo
T-0493 | 8 | tokens | Add sensitivity note (results depend on target/bug) | note present | todo
T-0494 | 8 | tokens | Run coverage gate on study package (>=85%) | gate green | todo
T-0495 | 8 | tokens | Add docstrings + type hints across study package | ruff/mypy clean | todo
T-0496 | 8 | tokens | Update docs/PRD_tokens.md with implemented interfaces | PRD matches code | todo
T-0497 | 8 | tokens | Peer-review token_comparison.md for honesty | review addressed | todo
T-0498 | 8 | tokens | Update reports/ index with study artifact | index updated | todo
T-0499 | 8 | tokens | Commit Phase-8 token comparison | commit pushed; CI green | todo
T-0500 | 8 | tokens | Validate charts render in README (relative paths) | render ok | todo
T-0501 | 8 | tokens | Phase-8 study rigor task #56: additional metric + test | metric covered | todo
T-0502 | 8 | tokens | Phase-8 study rigor task #57: additional metric + test | metric covered | todo
T-0503 | 8 | tokens | Phase-8 study rigor task #58: additional metric + test | metric covered | todo
T-0504 | 8 | tokens | Phase-8 study rigor task #59: additional metric + test | metric covered | todo
T-0505 | 8 | tokens | Phase-8 study rigor task #60: additional metric + test | metric covered | todo

## Phase 9 — Extensions (centrality_rank, dynamic_hot, orphans, impact_report)

T-0506 | 9 | ext | Add src/cosmos77/ext/ package skeleton | package imports | todo
T-0507 | 9 | ext | centrality_rank: design CLI/API contract | contract doc | todo
T-0508 | 9 | ext | centrality_rank: write failing test (red) | test fails | todo
T-0509 | 9 | ext | centrality_rank: implement ranked output (green) | ranks nodes | todo
T-0510 | 9 | ext | centrality_rank: add tie-breaking + stable sort | deterministic | todo
T-0511 | 9 | ext | centrality_rank: test tie-breaking | stable | todo
T-0512 | 9 | ext | centrality_rank: persist to artifacts/ext/centrality_rank.json | file present | todo
T-0513 | 9 | ext | centrality_rank: CLI subcommand + test | CLI runs | todo
T-0514 | 9 | ext | centrality_rank: docstrings + type hints | ruff/mypy clean | todo
T-0515 | 9 | ext | centrality_rank: render to vault page | page written | todo
T-0516 | 9 | ext | centrality_rank: evidence tiers on entries | tiers present | todo
T-0517 | 9 | ext | dynamic_hot: design (re-rank hot.md as fixes land) | contract doc | todo
T-0518 | 9 | ext | dynamic_hot: write failing test (red) | test fails | todo
T-0519 | 9 | ext | dynamic_hot: implement dynamic re-ranking (green) | re-ranks | todo
T-0520 | 9 | ext | dynamic_hot: incorporate recent-change signal | signal used | todo
T-0521 | 9 | ext | dynamic_hot: test re-rank after change | order updates | todo
T-0522 | 9 | ext | dynamic_hot: persist hot history | history kept | todo
T-0523 | 9 | ext | dynamic_hot: test history persistence | round-trip ok | todo
T-0524 | 9 | ext | dynamic_hot: CLI subcommand + test | CLI runs | todo
T-0525 | 9 | ext | dynamic_hot: update vault hot.md dynamically | hot.md updated | todo
T-0526 | 9 | ext | dynamic_hot: docstrings + type hints | ruff/mypy clean | todo
T-0527 | 9 | ext | orphans: design (detect dead/disconnected nodes) | contract doc | todo
T-0528 | 9 | ext | orphans: write failing test (red) | test fails | todo
T-0529 | 9 | ext | orphans: implement orphan detection (green) | orphans listed | todo
T-0530 | 9 | ext | orphans: classify orphan type (unused/unreachable) | types assigned | todo
T-0531 | 9 | ext | orphans: test classification | types correct | todo
T-0532 | 9 | ext | orphans: persist to artifacts/ext/orphans.json | file present | todo
T-0533 | 9 | ext | orphans: CLI subcommand + test | CLI runs | todo
T-0534 | 9 | ext | orphans: render orphans report/page | page written | todo
T-0535 | 9 | ext | orphans: evidence tiers on findings | tiers present | todo
T-0536 | 9 | ext | orphans: docstrings + type hints | ruff/mypy clean | todo
T-0537 | 9 | ext | impact_report: design (blast radius of a change) | contract doc | todo
T-0538 | 9 | ext | impact_report: write failing test (red) | test fails | todo
T-0539 | 9 | ext | impact_report: implement reachability/impact set (green) | impact set computed | todo
T-0540 | 9 | ext | impact_report: include centrality-weighted impact | weighted score | todo
T-0541 | 9 | ext | impact_report: test impact set on toy graph | matches expected | todo
T-0542 | 9 | ext | impact_report: apply to the Phase-7 fix (real blast radius) | report on fix | todo
T-0543 | 9 | ext | impact_report: test fix-impact report | report produced | todo
T-0544 | 9 | ext | impact_report: persist to artifacts/ext/impact.json | file present | todo
T-0545 | 9 | ext | impact_report: CLI subcommand + test | CLI runs | todo
T-0546 | 9 | ext | impact_report: render impact report/page | page written | todo
T-0547 | 9 | ext | impact_report: evidence tiers on claims | tiers present | todo
T-0548 | 9 | ext | impact_report: docstrings + type hints | ruff/mypy clean | todo
T-0549 | 9 | ext | Cross-link all extensions into vault index | links resolve | todo
T-0550 | 9 | ext | Test extension cross-links | resolve | todo
T-0551 | 9 | ext | Sanitize all extension artifacts | no leaks | todo
T-0552 | 9 | ext | Test extension sanitizers | redactions present | todo
T-0553 | 9 | ext | Run coverage gate on ext package (>=85%) | gate green | todo
T-0554 | 9 | ext | Write reports/extensions.md summarizing all four | report written | todo
T-0555 | 9 | ext | Test extensions report embeds | links valid | todo
T-0556 | 9 | ext | Update docs/PRD_extensions.md with interfaces | PRD matches code | todo
T-0557 | 9 | ext | Add honest-measurement caveats to extensions report | caveats present | todo
T-0558 | 9 | ext | Deterministic extension outputs (stable diff) | re-run equal | todo
T-0559 | 9 | ext | Commit Phase-9 extensions | commit pushed; CI green | todo
T-0560 | 9 | ext | Phase-9 extension polish task #55: edge case + test | case covered | todo

## Phase 10 — README lab report + visuals + spec sheet

T-0561 | 10 | report | Outline README lab report (problem, method, results, discussion) | outline drafted | todo
T-0562 | 10 | report | Write README intro + problem statement | section written | todo
T-0563 | 10 | report | Write method section (graph-guided pipeline overview) | section written | todo
T-0564 | 10 | report | Add architecture diagram (pipeline blocks) Mermaid+PNG | diagram embedded | todo
T-0565 | 10 | report | Test architecture diagram renders | PNG present | todo
T-0566 | 10 | report | Write graph-extraction results (god nodes, centrality) | section written | todo
T-0567 | 10 | report | Embed god_nodes + centrality tables | tables present | todo
T-0568 | 10 | report | Write reverse-engineering summary + diagrams | section written | todo
T-0569 | 10 | report | Write agent design summary + topology diagram | section written | todo
T-0570 | 10 | report | Write bug-fix results (FAIL->PASS, before/after) | section written | todo
T-0571 | 10 | report | Embed before/after diff in README | diff embedded | todo
T-0572 | 10 | report | Write token-comparison results + charts | section written | todo
T-0573 | 10 | report | Embed token charts in README | charts embedded | todo
T-0574 | 10 | report | Write extensions summary | section written | todo
T-0575 | 10 | report | Write discussion (what worked, what didn't, honest) | section written | todo
T-0576 | 10 | report | Write limitations + future work | section written | todo
T-0577 | 10 | report | Add reproducibility/quickstart (uv sync, CLI commands) | quickstart present | todo
T-0578 | 10 | report | Test quickstart commands run (smoke) | commands succeed | todo
T-0579 | 10 | report | Add spec sheet (deps, versions, models, configs) | spec sheet present | todo
T-0580 | 10 | report | Verify spec sheet matches pyproject/uv.lock | matches | todo
T-0581 | 10 | report | Add evidence-tier legend to README | legend present | todo
T-0582 | 10 | report | Tag README claims with evidence tiers where relevant | tiers present | todo
T-0583 | 10 | report | Add links to vault, reports, artifacts | links resolve | todo
T-0584 | 10 | report | Test README links resolve (link checker) | 0 broken links | todo
T-0585 | 10 | report | Add table of contents | TOC present | todo
T-0586 | 10 | report | Add badges (CI, coverage, version) | badges render | todo
T-0587 | 10 | report | Verify all images use relative paths | render on GitHub | todo
T-0588 | 10 | report | Sanitize README (no abs paths/secrets) | no leaks | todo
T-0589 | 10 | report | Test README sanitizer | redactions present | todo
T-0590 | 10 | report | Add 'honest measurement' summary box | box present | todo
T-0591 | 10 | report | Add credits/acknowledgements + license note | present | todo
T-0592 | 10 | report | Generate all visuals (run viz pipeline) | visuals produced | todo
T-0593 | 10 | report | Test visuals pipeline end-to-end | all PNGs present | todo
T-0594 | 10 | report | Optimize/compress PNGs for repo size | sizes reduced | todo
T-0595 | 10 | report | Add results-at-a-glance summary table | table present | todo
T-0596 | 10 | report | Proofread README (spelling/grammar pass) | clean | todo
T-0597 | 10 | report | Peer-review README lab report | review addressed | todo
T-0598 | 10 | report | Cross-check README claims vs artifacts (no overclaim) | claims supported | todo
T-0599 | 10 | report | Add changelog reference + version stamp | present | todo
T-0600 | 10 | report | Run markdown lint on README | lint clean | todo
T-0601 | 10 | report | Verify README renders in GitHub preview | renders | todo
T-0602 | 10 | report | Update docs/PRD_report.md with final structure | PRD matches | todo
T-0603 | 10 | report | Update reports/ index with README artifact | index updated | todo
T-0604 | 10 | report | Commit Phase-10 lab report + visuals | commit pushed; CI green | todo
T-0605 | 10 | report | Final consistency pass across all reports | consistent | todo

## Phase 11 — QA gauntlet + acceptance audit C1–C15

T-0606 | 11 | qa | Run full test suite (pytest) clean | all green | todo
T-0607 | 11 | qa | Run coverage gate project-wide (>=85%) | gate green | todo
T-0608 | 11 | qa | Run ruff lint + format check | clean | todo
T-0609 | 11 | qa | Run mypy/type check | clean | todo
T-0610 | 11 | qa | Run pre-commit on all files | passes | todo
T-0611 | 11 | qa | Run secret scan across repo | no secrets | todo
T-0612 | 11 | qa | Run link checker across all docs+vault+README | 0 broken links | todo
T-0613 | 11 | qa | Verify deterministic re-run of full pipeline | stable | todo
T-0614 | 11 | qa | Verify isolated venv not committed/leaked | clean | todo
T-0615 | 11 | qa | Verify all artifacts sanitized (no abs paths) | clean | todo
T-0616 | 11 | qa | Verify evidence tiers present across all outputs | tiers everywhere | todo
T-0617 | 11 | qa | Run CI on clean clone (fresh checkout) | CI green | todo
T-0618 | 11 | audit | Acceptance audit C1: verify criterion C1 met with evidence | C1 pass + evidence linked | todo
T-0619 | 11 | audit | Acceptance audit C2: verify criterion C2 met with evidence | C2 pass + evidence linked | todo
T-0620 | 11 | audit | Acceptance audit C3: verify criterion C3 met with evidence | C3 pass + evidence linked | todo
T-0621 | 11 | audit | Acceptance audit C4: verify criterion C4 met with evidence | C4 pass + evidence linked | todo
T-0622 | 11 | audit | Acceptance audit C5: verify criterion C5 met with evidence | C5 pass + evidence linked | todo
T-0623 | 11 | audit | Acceptance audit C6: verify criterion C6 met with evidence | C6 pass + evidence linked | todo
T-0624 | 11 | audit | Acceptance audit C7: verify criterion C7 met with evidence | C7 pass + evidence linked | todo
T-0625 | 11 | audit | Acceptance audit C8: verify criterion C8 met with evidence | C8 pass + evidence linked | todo
T-0626 | 11 | audit | Acceptance audit C9: verify criterion C9 met with evidence | C9 pass + evidence linked | todo
T-0627 | 11 | audit | Acceptance audit C10: verify criterion C10 met with evidence | C10 pass + evidence linked | todo
T-0628 | 11 | audit | Acceptance audit C11: verify criterion C11 met with evidence | C11 pass + evidence linked | todo
T-0629 | 11 | audit | Acceptance audit C12: verify criterion C12 met with evidence | C12 pass + evidence linked | todo
T-0630 | 11 | audit | Acceptance audit C13: verify criterion C13 met with evidence | C13 pass + evidence linked | todo
T-0631 | 11 | audit | Acceptance audit C14: verify criterion C14 met with evidence | C14 pass + evidence linked | todo
T-0632 | 11 | audit | Acceptance audit C15: verify criterion C15 met with evidence | C15 pass + evidence linked | todo
T-0633 | 11 | qa | Build acceptance matrix (C1-C15 status table) | matrix complete | todo
T-0634 | 11 | qa | Cross-check acceptance matrix vs PRD success criteria | aligned | todo
T-0635 | 11 | qa | Fix any audit gaps found (triage list) | gaps closed | todo
T-0636 | 11 | qa | Re-run gauntlet after gap fixes | all green | todo
T-0637 | 11 | qa | Verify token-comparison claims reproducible | reproduced | todo
T-0638 | 11 | qa | Verify bug-fix FAIL->PASS on fresh runner | PASS confirmed | todo
T-0639 | 11 | qa | Final no-overclaim review (honest measurement) | claims supported | todo
T-0640 | 11 | qa | Write reports/qa_report.md (gauntlet results) | report written | todo
T-0641 | 11 | qa | Commit Phase-11 QA + audit | commit pushed; CI green | todo
T-0642 | 11 | qa | Phase-11 QA hardening task #37: extra check + fix | check covered | todo
T-0643 | 11 | qa | Phase-11 QA hardening task #38: extra check + fix | check covered | todo
T-0644 | 11 | qa | Phase-11 QA hardening task #39: extra check + fix | check covered | todo
T-0645 | 11 | qa | Phase-11 QA hardening task #40: extra check + fix | check covered | todo

## Phase 12 — Cover PDF (exercise=4) + tag v1.00 + release + Moodle

T-0646 | 12 | release | Draft cover sheet content (course UOH-RL07, exercise=4, student) | draft ready | todo
T-0647 | 12 | release | Set exercise number = 4 on cover sheet | exercise=4 set | todo
T-0648 | 12 | release | Generate cover PDF (render to PDF) | PDF produced | todo
T-0649 | 12 | release | Verify cover PDF metadata (exercise=4, title) | metadata correct | todo
T-0650 | 12 | release | Test cover PDF non-empty + opens | valid PDF | todo
T-0651 | 12 | release | Assemble submission bundle (report+artifacts+vault refs) | bundle listed | todo
T-0652 | 12 | release | Final version stamp v1.00 across files | versions consistent | todo
T-0653 | 12 | release | Update CHANGELOG for v1.00 release | entry present | todo
T-0654 | 12 | release | Verify working tree clean before tag | git clean | todo
T-0655 | 12 | release | Run full gate one last time pre-release | all green | todo
T-0656 | 12 | release | Create annotated git tag v1.00 | tag created | todo
T-0657 | 12 | release | Push tag v1.00 to remote | tag pushed | todo
T-0658 | 12 | release | Create GitHub release v1.00 with notes | release published | todo
T-0659 | 12 | release | Attach cover PDF + key artifacts to release | assets attached | todo
T-0660 | 12 | release | Verify release assets download + open | assets valid | todo
T-0661 | 12 | release | Verify CI green on tagged commit | CI green | todo
T-0662 | 12 | release | Prepare Moodle submission (links + PDF) | submission ready | todo
T-0663 | 12 | release | Submit to Moodle (UOH-RL07 exercise 4) | submitted | todo
T-0664 | 12 | release | Confirm Moodle submission receipt | receipt saved | todo
T-0665 | 12 | release | Archive final artifacts snapshot | archive saved | todo
T-0666 | 12 | release | Write reports/release_notes.md | notes written | todo
T-0667 | 12 | release | Final repo hygiene check (no stray files) | clean | todo
T-0668 | 12 | release | Verify README links work on release tag | resolve | todo
T-0669 | 12 | release | Post-release sanity: clone tag + smoke run | smoke passes | todo
T-0670 | 12 | release | Close out TODO ledger (mark phases complete) | ledger reconciled | todo
