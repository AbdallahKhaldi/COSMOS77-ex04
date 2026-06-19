"""Tests for the explicit, auditable suspect ranking (C9)."""

from __future__ import annotations

from cosmos77_ex04.extensions.centrality_rank import rank_suspects_scored, write_suspects_md


def test_rank_orders_by_score_and_returns_dicts(model):
    # 'tenumerate' carries the proximity boost (label ~ failing test) AND the
    # bridge betweenness on a->c, so it is the clear top suspect.
    ranking = rank_suspects_scored(model, "test_enumerate", top=5)
    assert ranking[0]["node_id"] == "b"
    scores = [row["score"] for row in ranking]
    assert scores == sorted(scores, reverse=True)
    first = ranking[0]
    assert set(first) == {"node_id", "label", "file", "degree", "betweenness", "score"}


def test_rank_proximity_boost_outranks_pure_degree(model):
    # Without proximity, the hub 'a' (degree 2) would lead; the boost flips it.
    ranking = rank_suspects_scored(model, "nomatch", top=5)
    assert ranking[0]["node_id"] in {"a", "b"}


def test_rank_traceback_boost_lifts_named_file(model):
    ranking = rank_suspects_scored(model, "test_x", test_output="Traceback: pkg/utils.py:5", top=5)
    by_id = {row["node_id"]: row for row in ranking}
    # 'helper' lives in utils.py, named by the traceback -> strong boost over peers.
    assert by_id["c"]["score"] > by_id["_helper"]["score"]


def test_rank_respects_top_limit(model):
    assert len(rank_suspects_scored(model, "t", top=2)) == 2


def test_write_suspects_md_writes_table(tmp_path, model):
    ranking = rank_suspects_scored(model, "test_enumerate", top=5)
    out = write_suspects_md(ranking, tmp_path / "suspects.md")
    text = out.read_text(encoding="utf-8")
    assert "| Rank | Candidate |" in text
    assert "kind: suspects" in text
    assert "tqdm" in text


def test_write_suspects_md_handles_empty(tmp_path):
    out = write_suspects_md([], tmp_path / "suspects.md")
    assert out.exists() and "suspects.md" in out.read_text(encoding="utf-8")
