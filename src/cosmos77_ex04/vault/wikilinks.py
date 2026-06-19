"""Low-level Obsidian markdown emit primitives (C2).

These are the smallest building blocks of the knowledge vault: a filename
sanitiser that guarantees no path separator or Obsidian-forbidden character
leaks into a ``[[wikilink]]`` target, a wikilink renderer, and a YAML
frontmatter block. Keeping them pure and tiny is what lets the higher layers
GUARANTEE that every emitted wikilink resolves to a real ``.md`` file.
"""

from __future__ import annotations

import re

#: Characters Obsidian/the filesystem forbid in a note stem.
_FORBIDDEN = re.compile(r'[/\\:*?"<>|]')
#: Any run of whitespace (collapsed to a single space).
_WHITESPACE = re.compile(r"\s+")


def sanitize_filename(text: str) -> str:
    """Turn arbitrary node text into a safe, non-empty note stem.

    Why: a wikilink target IS a filename; an unescaped ``/`` or ``:`` would
    break navigation (the link would never resolve), so we strip the forbidden
    set, collapse whitespace, and never return an empty string.
    """
    cleaned = _FORBIDDEN.sub(" ", text or "")
    cleaned = _WHITESPACE.sub(" ", cleaned).strip()
    cleaned = cleaned.strip(".")
    return cleaned or "untitled"


def wikilink(stem: str, alias: str | None = None) -> str:
    """Render an Obsidian ``[[stem]]`` (or ``[[stem|alias]]``) link.

    Why: callers must emit links only through this helper so the syntax stays
    uniform and the resolver regex (``\\[\\[([^\\]|]+)``) always matches.
    """
    if alias and alias != stem:
        return f"[[{stem}|{alias}]]"
    return f"[[{stem}]]"


def frontmatter(fields: dict[str, str]) -> str:
    """Render a YAML ``---``-fenced frontmatter block for a note.

    Why: Obsidian reads frontmatter for tags/properties; emitting it
    deterministically keeps the vault diff-stable across runs.
    """
    lines = ["---"]
    for key, value in fields.items():
        lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)
