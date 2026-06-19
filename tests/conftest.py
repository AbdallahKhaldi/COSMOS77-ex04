"""Shared pytest fixtures and deterministic-seed setup (CLAUDE.md rule 17)."""

from __future__ import annotations

import json
import random
from pathlib import Path

import pytest

_SETUP = {
    "version": "1.00",
    "target": {
        "source": "bugsinpy",
        "project": "tqdm",
        "package_subdir": "tqdm",
        "bug_id": 1,
        "python_version": "3.8.20",
        "workdir": "data/target",
        "isolation": "venv",
    },
    "graphify": {"out_dir": "graphify-out", "obsidian": True, "wiki": True},
    "agent": {
        "framework": "langgraph",
        "max_llm_calls": 6,
        "recursion_limit": 12,
        "top_k": 6,
        "max_files": 4,
    },
    "tokens": {"baseline_mode": "raw_files", "guided_mode": "graph_guided", "measure": ["tokens"]},
    "paths": {"obsidian_dir": "obsidian", "reports_dir": "reports", "artifacts_dir": "artifacts"},
}
_PROVIDERS = {
    "version": "1.00",
    "active": "gemini",
    "providers": {
        "gemini": {"model": "gemini-2.5-flash", "api_key_env": "GOOGLE_API_KEY"},
        "groq": {"model": "groq/llama-3.3-70b-versatile", "api_key_env": "GROQ_API_KEY"},
    },
}


@pytest.fixture(autouse=True)
def _seed_random() -> None:
    """Seed `random` before every test so nothing flakes."""
    random.seed(1729)


@pytest.fixture
def config_dir(tmp_path: Path) -> Path:
    """A throwaway ``config/`` dir with valid setup.json + providers.json."""
    cfg = tmp_path / "config"
    cfg.mkdir()
    (cfg / "setup.json").write_text(json.dumps(_SETUP), encoding="utf-8")
    (cfg / "providers.json").write_text(json.dumps(_PROVIDERS), encoding="utf-8")
    return cfg


@pytest.fixture
def config(config_dir: Path):
    """A :class:`Config` loaded from the throwaway config dir."""
    from cosmos77_ex04.shared.config import Config

    return Config(config_dir)
