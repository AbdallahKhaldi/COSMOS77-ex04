"""OOP SCHEMA (C4) — class inheritance extracted by AST-walking the source.

We walk the target package's ``.py`` files with the ``ast`` module (NOT folder
listings): each ``ClassDef`` yields a class, its base classes are the
inheritance edges (``<|--``), and its function defs are the methods. Composition
is a best-effort signal (a base named after another extracted class). The
``classDiagram`` Mermaid and a networkx PNG render the inheritance graph.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless backend — set BEFORE importing pyplot.
import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402


@dataclass
class ClassInfo:
    """One class extracted from the AST: name, bases (inheritance), methods."""

    name: str
    bases: list[str] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)
    file: str = ""


def _base_name(node: ast.expr) -> str:
    """Best-effort dotted name for a base-class expression (``a.B`` -> ``B``)."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ""


def _classes_in_tree(tree: ast.AST, file: str) -> list[ClassInfo]:
    """Collect every ``ClassDef`` in one parsed module as ``ClassInfo``."""
    classes: list[ClassInfo] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        bases = [b for b in (_base_name(x) for x in node.bases) if b]
        methods = [
            child.name
            for child in node.body
            if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
        ]
        classes.append(ClassInfo(name=node.name, bases=bases, methods=methods, file=file))
    return classes


def extract_classes(source) -> list[ClassInfo]:
    """AST-walk ``source`` (a file or a directory of ``.py``) into ``ClassInfo``.

    Accepts a path to a single ``.py`` file or a package directory; syntactically
    broken files are skipped (Ambiguous — they cannot be Extracted).
    """
    root = Path(source)
    files = [root] if root.is_file() else sorted(root.rglob("*.py"))
    out: list[ClassInfo] = []
    for path in files:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        out.extend(_classes_in_tree(tree, path.name))
    return out


def oop_mermaid(classes: list[ClassInfo]) -> str:
    """Render a Mermaid ``classDiagram`` with ``<|--`` inheritance + methods."""
    names = {c.name for c in classes}
    lines = ["classDiagram"]
    for info in classes:
        lines.append(f"    class {info.name} {{")
        for method in info.methods[:8]:
            lines.append(f"        +{method}()")
        lines.append("    }")
    for info in classes:
        for base in info.bases:
            if base in names:
                lines.append(f"    {base} <|-- {info.name}")
    return "\n".join(lines)


def _inheritance_graph(classes: list[ClassInfo]) -> nx.DiGraph:
    """Build the directed inheritance graph (base -> subclass) over known classes."""
    names = {c.name for c in classes}
    graph: nx.DiGraph = nx.DiGraph()
    for info in classes:
        graph.add_node(info.name)
    for info in classes:
        for base in info.bases:
            if base in names:
                graph.add_edge(base, info.name)
    return graph


def render_oop_png(classes: list[ClassInfo], out_path):
    """Render the class-inheritance graph to ``out_path`` (a PNG ``Path``)."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    graph = _inheritance_graph(classes)
    pos = nx.spring_layout(graph, seed=77, k=1.1)
    fig, ax = plt.subplots(figsize=(12, 9))
    nx.draw_networkx_nodes(graph, pos, node_size=900, node_color="#a1d99b", ax=ax)
    nx.draw_networkx_edges(graph, pos, alpha=0.5, arrows=True, ax=ax)
    nx.draw_networkx_labels(graph, pos, font_size=7, ax=ax)
    ax.set_title("OOP Schema — Class Inheritance (<|--)")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out
