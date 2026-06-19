"""Gemini provider factory + a METERED diagnose call (C5; CLAUDE.md rule 13).

Every LLM call goes through :func:`invoke_diagnose`, which records the response's
``usage_metadata`` into the Gatekeeper ledger — the measured evidence behind the
token comparison (C8). ``get_openai_callback`` does NOT work with Gemini, so we
read ``response.usage_metadata`` ({input_tokens, output_tokens, total_tokens}).
"""

from __future__ import annotations

import os
from typing import Any

from cosmos77_ex04.shared.config import Config
from cosmos77_ex04.shared.gatekeeper import Gatekeeper


def build_llm(config: Config, *, temperature: float = 0.0) -> Any:
    """Build a ``ChatGoogleGenerativeAI`` from providers.json (Gemini free tier)."""
    from langchain_google_genai import ChatGoogleGenerativeAI

    provider = config.provider_config()
    api_key = os.environ.get(provider.get("api_key_env", "GOOGLE_API_KEY"))
    return ChatGoogleGenerativeAI(
        model=provider["model"],
        temperature=temperature,
        max_output_tokens=int(config.agent().get("max_output_tokens", 4096)),
        google_api_key=api_key,
    )


def invoke_diagnose(llm: Any, prompt: str, gatekeeper: Gatekeeper, label: str = "diagnose") -> str:
    """Invoke the LLM, record its usage into the ledger, and return the text."""
    message = llm.invoke(prompt)
    gatekeeper.record(getattr(message, "usage_metadata", None), label=label)
    content = getattr(message, "content", "")
    return content if isinstance(content, str) else str(content)
