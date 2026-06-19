"""Tests for the cover-sheet field values — exercise 4, ex04 repo (Phase 12)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_PATH = Path(__file__).resolve().parents[3] / "scripts" / "generate_cover_pdf.py"
_spec = importlib.util.spec_from_file_location("generate_cover_pdf", _PATH)
cover = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cover)


def test_field_values_target_exercise_4():
    fields = dict(cover.build_field_values(4, 85))
    assert fields["Submitting an exercise number"] == "4"
    assert fields["Group ID code"] == "COSMOS77"
    assert fields["Recommendation for self-scoring"] == "85"
    assert fields["A late submission confirmation"] == "no"


def test_repo_url_points_at_ex04():
    fields = dict(cover.build_field_values(4, 85))
    assert "COSMOS77-ex04" in fields["Link to GITHUB"]
    assert cover._REPO_URL.endswith("COSMOS77-ex04")


def test_exercise_number_and_score_pass_through():
    fields = dict(cover.build_field_values(3, 90))
    assert fields["Submitting an exercise number"] == "3"
    assert fields["Recommendation for self-scoring"] == "90"
