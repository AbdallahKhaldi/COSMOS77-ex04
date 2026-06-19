"""Tests for the Gatekeeper token ledger (rule 13)."""

from __future__ import annotations

from cosmos77_ex04.shared.gatekeeper import Gatekeeper


def test_record_dict_accumulates():
    gk = Gatekeeper()
    gk.record({"input_tokens": 10, "output_tokens": 5, "total_tokens": 15})
    gk.record({"input_tokens": 2, "output_tokens": 3, "total_tokens": 5})
    led = gk.ledger()
    assert (led["input_tokens"], led["output_tokens"], led["total_tokens"], led["calls"]) == (
        12,
        8,
        20,
        2,
    )


def test_record_none_is_noop():
    gk = Gatekeeper()
    assert gk.record(None) is None
    assert gk.ledger()["calls"] == 0


def test_alias_fields_and_total_fallback():
    gk = Gatekeeper()
    rec = gk.record({"prompt_tokens": 7, "completion_tokens": 3})  # no total_tokens
    assert rec is not None
    assert rec.total_tokens == 10
    assert gk.usage.total_tokens == 10


def test_records_carry_label():
    gk = Gatekeeper()
    gk.record({"input_tokens": 1, "output_tokens": 1, "total_tokens": 2}, label="diagnose")
    assert gk.records[0].label == "diagnose"
    assert len(gk.records) == 1


def test_record_object_with_attributes():
    class FakeMeta:
        input_tokens = 4
        output_tokens = 6
        total_tokens = 10

    gk = Gatekeeper()
    gk.record(FakeMeta())
    assert gk.ledger()["total_tokens"] == 10


def test_reset_clears_ledger():
    gk = Gatekeeper()
    gk.record({"total_tokens": 5})
    gk.reset()
    assert gk.ledger()["calls"] == 0
    assert gk.records == []


def test_ledger_accepts_extra_metrics():
    gk = Gatekeeper()
    assert gk.ledger(files_read=3)["files_read"] == 3


def test_scrub_redacts_api_key():
    scrubbed = Gatekeeper.scrub("key=AIzaSyA1234567890abcdefghijklmnopqrstuv now")
    assert "AIza" not in scrubbed
    assert "[REDACTED]" in scrubbed
