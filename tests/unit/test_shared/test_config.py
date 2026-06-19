"""Tests for the JSON + .env config loader (rule 4)."""

from __future__ import annotations

import json

import pytest

from cosmos77_ex04.shared.config import Config


def test_get_dot_path(config):
    assert config.get("agent.max_llm_calls") == 6


def test_get_missing_returns_default(config):
    assert config.get("nope.key", default="x") == "x"


def test_get_missing_raises(config):
    with pytest.raises(KeyError):
        config.get("nope.key")


def test_section_accessors(config):
    assert config.target()["project"] == "tqdm"
    assert config.graphify()["out_dir"] == "graphify-out"
    assert config.agent()["framework"] == "langgraph"
    assert config.tokens()["baseline_mode"] == "raw_files"
    assert config.paths()["obsidian_dir"] == "obsidian"


def test_provider_helpers(config):
    assert config.active_provider() == "gemini"
    assert config.provider_config()["model"] == "gemini-2.5-flash"
    assert config.provider_config("groq")["api_key_env"] == "GROQ_API_KEY"
    assert "gemini" in config.providers()["providers"]


def test_provider_unknown_raises(config):
    with pytest.raises(KeyError):
        config.provider_config("nope")


def test_version_dir_repr_from_path(config, config_dir):
    assert config.version == "1.00"
    assert config.config_dir == config_dir
    assert "1.00" in repr(config)
    assert Config.from_path(config_dir).version == "1.00"


def test_env_reads_environment(config, monkeypatch):
    monkeypatch.setenv("FOO_BAR", "baz")
    assert config.env("FOO_BAR") == "baz"
    assert config.env("MISSING_ENV_VAR", "d") == "d"


def test_missing_config_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        Config(tmp_path)


def test_bad_version_raises(tmp_path):
    cfg = tmp_path / "config"
    cfg.mkdir()
    (cfg / "setup.json").write_text(json.dumps({"version": "0.9"}), encoding="utf-8")
    (cfg / "providers.json").write_text(json.dumps({"version": "1.00"}), encoding="utf-8")
    with pytest.raises(ValueError):
        Config(cfg)


def test_non_dict_json_raises(tmp_path):
    cfg = tmp_path / "config"
    cfg.mkdir()
    (cfg / "setup.json").write_text(json.dumps([1, 2, 3]), encoding="utf-8")
    (cfg / "providers.json").write_text(json.dumps({"version": "1.00"}), encoding="utf-8")
    with pytest.raises(ValueError):
        Config(cfg)
