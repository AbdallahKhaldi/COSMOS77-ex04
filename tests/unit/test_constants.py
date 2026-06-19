"""Phase-0 smoke test: the package imports and core constants are sane."""

from __future__ import annotations

import cosmos77_ex04
from cosmos77_ex04 import constants


def test_package_version_is_one_zero():
    assert cosmos77_ex04.__version__ == "1.00"


def test_default_encoding_is_utf8():
    assert constants.DEFAULT_ENCODING == "utf-8"


def test_package_name_matches_module():
    assert constants.PACKAGE_NAME == "cosmos77_ex04"


def test_project_version_matches_package():
    assert constants.PROJECT_VERSION == cosmos77_ex04.__version__


def test_pipeline_stages_are_well_formed():
    # The CLI parser is built from these stages; building it must not raise.
    from cosmos77_ex04.cli.main import build_parser

    build_parser()
    assert "prepare-target" in constants.PIPELINE_STAGES
    assert constants.PIPELINE_STAGES[-1] == "run"


def test_evidence_tiers_and_node_kinds():
    assert constants.EVIDENCE_TIERS == ("extracted", "inferred", "ambiguous")
    assert "module" in constants.NODE_KINDS
    assert (constants.BUGGY_VERSION, constants.FIXED_VERSION) == (0, 1)
