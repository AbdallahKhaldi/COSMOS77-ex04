"""The page registry — the integrity layer of the vault (C2).

Every wikilink in the vault MUST resolve to a generated page; a dangling
``[[link]]`` would break the professor's "question -> index -> 2-3 pages ->
answer" guided-retrieval protocol. The :class:`PageRegistry` is how we
guarantee that: it assigns ONE unique, sanitised stem per registered key
(a node id or a ``community:<id>`` key), and callers emit a wikilink only when
``registry.has(key)`` is true. Two nodes labelled ``__init__.py`` therefore get
distinct stems (``__init__.py``, ``__init__.py-2``) and never collide on disk.
"""

from __future__ import annotations

from cosmos77_ex04.vault.wikilinks import sanitize_filename, wikilink


class PageRegistry:
    """A bijection between graph keys and unique sanitised page stems."""

    def __init__(self) -> None:
        """Start empty; keys are added via :meth:`register`."""
        self._stems: dict[str, str] = {}
        self._used: set[str] = set()

    @staticmethod
    def community_key(community_id: int) -> str:
        """The registry key for a community page (kept distinct from node ids)."""
        return f"community:{community_id}"

    def register(self, key: str, text: str) -> str:
        """Assign ``key`` a unique stem derived from ``text`` and return it.

        Why: idempotent so callers can register defensively; collisions get a
        ``-2``/``-3`` suffix so duplicate labels never overwrite each other.
        """
        if key in self._stems:
            return self._stems[key]
        base = sanitize_filename(text)
        stem = base
        counter = 2
        while stem in self._used:
            stem = f"{base}-{counter}"
            counter += 1
        self._stems[key] = stem
        self._used.add(stem)
        return stem

    def has(self, key: str) -> bool:
        """Whether ``key`` has a registered page (so a wikilink will resolve)."""
        return key in self._stems

    def stem_of(self, key: str) -> str:
        """The unique stem for ``key`` (raises ``KeyError`` if unregistered)."""
        return self._stems[key]

    def stems(self) -> list[str]:
        """Every assigned stem (used by the resolver self-check in tests)."""
        return list(self._used)

    def link(self, key: str, alias: str | None = None) -> str:
        """Render a resolving ``[[stem|alias]]`` for a registered ``key``."""
        return wikilink(self.stem_of(key), alias)
