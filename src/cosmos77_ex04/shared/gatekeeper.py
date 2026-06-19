"""Gatekeeper — the token LEDGER for the Spec Sheet (CLAUDE.md rule 13).

Every LLM call routes through here so the token comparison (C8) and the Spec
Sheet (C15) rest on MEASURED numbers, not estimates. There is NO hard cap
(Gemini free tier); we always measure. :meth:`record` accumulates one call's
``usage_metadata`` ({input_tokens, output_tokens, total_tokens} as emitted by
``ChatGoogleGenerativeAI``; prompt/completion aliases are tolerated) and keeps a
per-call record. :meth:`scrub` redacts secrets before anything is logged.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from typing import Any

_SECRET_RE = re.compile(
    r"(AIza[0-9A-Za-z_\-]{20,}|AQ\.[A-Za-z0-9_\-]{12,}|sk-[A-Za-z0-9_\-]{6,}"
    r"|gh[pousr]_[A-Za-z0-9]{16,}|Bearer\s+[A-Za-z0-9._\-]+)"
)


@dataclass
class CallRecord:
    """One metered LLM call's token usage (a row in the Spec Sheet)."""

    label: str
    input_tokens: int
    output_tokens: int
    total_tokens: int


@dataclass
class Usage:
    """Running token / call totals across every metered LLM call."""

    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    calls: int = 0


class Gatekeeper:
    """Accumulates LLM ``usage_metadata`` into a measured ledger (no hard cap)."""

    def __init__(self) -> None:
        self._usage = Usage()
        self._records: list[CallRecord] = []

    @property
    def usage(self) -> Usage:
        """The live aggregate counters."""
        return self._usage

    @property
    def records(self) -> list[CallRecord]:
        """A copy of the per-call records (the Spec Sheet rows)."""
        return list(self._records)

    @staticmethod
    def _read(src: Any, names: tuple[str, ...]) -> int:
        """Read the first present, truthy field in ``names`` from a dict or object."""
        for name in names:
            val = src.get(name) if isinstance(src, Mapping) else getattr(src, name, None)
            if val:
                return int(val)
        return 0

    def record(self, usage_metadata: Any, label: str = "llm") -> CallRecord | None:
        """Accumulate one call's usage; returns the stored :class:`CallRecord`."""
        if usage_metadata is None:
            return None
        inp = self._read(usage_metadata, ("input_tokens", "prompt_tokens"))
        out = self._read(usage_metadata, ("output_tokens", "completion_tokens"))
        total = self._read(usage_metadata, ("total_tokens",)) or (inp + out)
        self._usage.input_tokens += inp
        self._usage.output_tokens += out
        self._usage.total_tokens += total
        self._usage.calls += 1
        rec = CallRecord(label, inp, out, total)
        self._records.append(rec)
        return rec

    def ledger(self, **extra: Any) -> dict[str, Any]:
        """Return the aggregate ledger (input/output/total tokens + calls, + extras)."""
        agg = asdict(self._usage)
        agg.update(extra)
        return agg

    def reset(self) -> None:
        """Clear the ledger (e.g. between the baseline and guided runs)."""
        self._usage = Usage()
        self._records = []

    @staticmethod
    def scrub(text: str) -> str:
        """Redact anything resembling an API key/token before logging."""
        return _SECRET_RE.sub("[REDACTED]", text)
