"""JSON + .env config loader for COSMOS77-ex04 (CLAUDE.md rule 4).

Every module reads its tunables through :class:`Config`, so the target repo/bug,
model, provider, paths, and call/step caps are never hardcoded. ``setup.json`` and
``providers.json`` are version-checked at load; ``.env`` supplies the secret
``GOOGLE_API_KEY``. A future migration to YAML/pydantic touches only this file.
"""

from __future__ import annotations

import json
import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from cosmos77_ex04.shared.version import validate_config_version

_DEFAULT_CONFIG_DIR = Path(__file__).resolve().parents[3] / "config"
_SENTINEL: Any = object()


class Config:
    """Loads ``setup.json`` + ``providers.json`` and exposes dot-path access."""

    def __init__(self, config_dir: Path | str | None = None) -> None:
        self._config_dir = Path(config_dir) if config_dir is not None else _DEFAULT_CONFIG_DIR
        self._setup = self._load_json("setup.json")
        self._providers = self._load_json("providers.json")
        validate_config_version(str(self._setup.get("version", "")))
        load_dotenv(self._config_dir.parent / ".env", override=False)

    @classmethod
    def from_path(cls, path: Path | str) -> Config:
        """Construct from an explicit ``config/`` directory."""
        return cls(path)

    def _load_json(self, filename: str) -> dict[str, Any]:
        path = self._config_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"missing required config file: {path}")
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError(f"{path} must contain a JSON object at the top level")
        return data

    def get(self, dot_path: str, default: Any = _SENTINEL) -> Any:
        """Return the value at ``dot_path`` (e.g. ``agent.max_llm_calls``).

        Missing keys raise ``KeyError`` unless ``default`` is supplied.
        """
        node: Any = self._setup
        for part in dot_path.split("."):
            if isinstance(node, Mapping) and part in node:
                node = node[part]
            else:
                if default is _SENTINEL:
                    raise KeyError(dot_path)
                return default
        return node

    def env(self, key: str, default: str | None = None) -> str | None:
        """Read an environment variable (after ``.env`` has been loaded)."""
        return os.environ.get(key, default)

    def target(self) -> dict[str, Any]:
        """Return the ``target`` section (source, project, bug_id, workdir, isolation)."""
        return dict(self.get("target", default={}))

    def graphify(self) -> dict[str, Any]:
        """Return the ``graphify`` section (out_dir, obsidian, wiki)."""
        return dict(self.get("graphify", default={}))

    def agent(self) -> dict[str, Any]:
        """Return the ``agent`` section (framework, max_llm_calls, recursion_limit...)."""
        return dict(self.get("agent", default={}))

    def tokens(self) -> dict[str, Any]:
        """Return the ``tokens`` section (baseline_mode, guided_mode, measure)."""
        return dict(self.get("tokens", default={}))

    def paths(self) -> dict[str, str]:
        """Return the ``paths`` section (obsidian_dir, reports_dir, artifacts_dir)."""
        return dict(self.get("paths", default={}))

    def providers(self) -> dict[str, Any]:
        """Return the parsed ``providers.json`` payload."""
        return dict(self._providers)

    def active_provider(self) -> str:
        """Return the active provider name from ``providers.json``."""
        return str(self._providers.get("active", ""))

    def provider_config(self, name: str | None = None) -> dict[str, Any]:
        """Return one provider's ``{model, api_key_env}`` (defaults to the active one)."""
        key = name or self.active_provider()
        providers = self._providers.get("providers", {})
        if key not in providers:
            raise KeyError(f"unknown provider {key!r}; known: {sorted(providers)}")
        return dict(providers[key])

    @property
    def version(self) -> str:
        """The ``setup.json`` version string (e.g. ``"1.00"``)."""
        return str(self._setup.get("version", ""))

    @property
    def config_dir(self) -> Path:
        """The directory the loader was pointed at."""
        return self._config_dir

    def __repr__(self) -> str:
        return f"Config(version={self.version!r}, dir={self._config_dir})"
