"""Command-line entry point for ``cosmos77-rev``.

A thin dispatcher over the SDK. Each subcommand (prepare-target, graphify, vault,
diagrams, agent, fix, compare, extensions, run) is wired to the SDK in its phase;
until then it prints guidance instead of crashing. No business logic lives here
(CLAUDE.md rule 2 — all logic flows through the SDK).
"""

from __future__ import annotations

import argparse
import sys

from cosmos77_ex04.constants import PIPELINE_STAGES


def build_parser() -> argparse.ArgumentParser:
    """Construct the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="cosmos77-rev",
        description=(
            "Graphify/Obsidian reverse-engineering + graph-guided debug agent for UOH-RL07 HW4."
        ),
    )
    parser.add_argument("command", nargs="?", choices=PIPELINE_STAGES, help="pipeline stage to run")
    parser.add_argument("--version", action="store_true", help="print the version and exit")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and dispatch. Returns a process exit code."""
    from cosmos77_ex04 import __version__

    args = build_parser().parse_args(argv)
    if args.version:
        print(f"cosmos77-rev {__version__}")
        return 0
    if args.command is None:
        build_parser().print_help()
        return 0
    return _dispatch(args.command)


def _dispatch(command: str) -> int:
    """Run one pipeline stage via the SDK and print a short summary."""
    from cosmos77_ex04.sdk.sdk import SDK

    sdk = SDK()
    if command == "prepare-target":
        info = sdk.prepare_target()
        verdict = "PASS" if info.test_result.passed else "FAIL (expected — that is the bug)"
        print(f"target: {info.project} bug #{info.bug_id} -> {info.project_dir}")
        print(f"python: {info.bug.python_version or 'n/a'}  test: {verdict}")
        print(f"token_ledger: {sdk.spec_sheet()}")
        return 0
    if command == "graphify":
        summary = sdk.run_graphify()
        print(
            f"graph: {summary['nodes']} nodes, {summary['edges']} edges, "
            f"{summary['communities']} communities"
        )
        print(f"tiers: {summary['tiers']}")
        print(f"god_nodes: {summary['god_nodes']}")
        return 0
    if command == "vault":
        summary = sdk.build_vault()
        print(
            f"vault: {summary['files']} files "
            f"({summary['pages']} pages, {summary['communities']} communities)"
        )
        print(f"god-node pages: {len(summary['god_nodes'])}")
        return 0
    print(f"`{command}` is not wired yet — it lands in its phase (see TODO.md).")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
