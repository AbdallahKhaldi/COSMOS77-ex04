"""Orchestrate the honest naive-vs-guided token comparison run (C8, C15).

Both arms see the SAME buggy code: we first revert the target to its buggy state
(undo a prior fix from config), then run the graph-guided agent and the naive
baseline against it with FRESH Gatekeeper ledgers so neither arm contaminates the
other's measurement. The LLM builder + run functions are module-level names so a
test can monkeypatch them and avoid any live Gemini call. Returns the two
measured runs, their comparison, and the report paths written.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cosmos77_ex04.agent.graph import run_agent
from cosmos77_ex04.agent.llm import build_llm
from cosmos77_ex04.agent.retrieval import read_text_file
from cosmos77_ex04.agent.state import AgentDeps
from cosmos77_ex04.graphify.model import GraphModel
from cosmos77_ex04.shared.gatekeeper import Gatekeeper
from cosmos77_ex04.tokens.baseline import run_baseline
from cosmos77_ex04.tokens.chart import render_chart
from cosmos77_ex04.tokens.compare import compare, write_comparison_md
from cosmos77_ex04.tokens.spec_sheet import write_spec_sheet


def revert_to_buggy(file_path: Path, fix: dict[str, Any]) -> bool:
    """Undo a prior fix so both arms see the bug; returns True if reverted."""
    search, replace = fix.get("search", ""), fix.get("replace", "")
    if not search or not replace or not file_path.exists():
        return False
    text = file_path.read_text(encoding="utf-8")
    if replace in text and search not in text:
        file_path.write_text(text.replace(replace, search, 1), encoding="utf-8")
        return True
    return False


def run_comparison(config: Any, repo_root: Path | str) -> dict[str, Any]:
    """Run both arms on the same buggy code and write the C8/C15 deliverables."""
    root = Path(repo_root)
    target, paths, agent_cfg = config.target(), config.paths(), config.agent()
    project = target.get("project", "tqdm")
    workdir = root / target.get("workdir", "data/target")
    fix = config.get("fix", default={})
    if fix.get("file"):
        revert_to_buggy(workdir / project / fix["file"], fix)

    artifacts = root / paths.get("artifacts_dir", "artifacts")
    model = GraphModel.from_json(artifacts / "graph.json")
    test_output = read_text_file(workdir / "_test_output.txt")
    source_root = workdir / project / target.get("package_subdir", project)
    failing_test = target.get("failing_test", "")

    guided_gk = Gatekeeper()
    deps = AgentDeps(
        model=model,
        llm=build_llm(config),
        gatekeeper=guided_gk,
        vault_dir=root / paths.get("obsidian_dir", "obsidian"),
        source_root=source_root,
        test_output=test_output,
        top_k=int(agent_cfg.get("top_k", 6)),
        max_files=int(agent_cfg.get("max_files", 4)),
        max_calls=int(agent_cfg.get("max_llm_calls", 6)),
    )
    guided = run_agent(
        deps, failing_test, recursion_limit=int(agent_cfg.get("recursion_limit", 12))
    )

    baseline_gk = Gatekeeper()
    baseline = run_baseline(build_llm(config), baseline_gk, source_root, failing_test, test_output)

    comparison = compare(baseline, guided)
    reports_dir = root / paths.get("reports_dir", "reports")
    comp_md = write_comparison_md(comparison, reports_dir / "TOKEN_COMPARISON.md")
    chart_pdf = render_chart(baseline, guided, artifacts / "token_comparison.pdf")
    spec_md = write_spec_sheet(guided, baseline, reports_dir / "SPEC_SHEET.md")
    return {
        "baseline": baseline,
        "guided": guided,
        "comparison": comparison,
        "reports": [str(comp_md), str(chart_pdf), str(spec_md)],
    }
