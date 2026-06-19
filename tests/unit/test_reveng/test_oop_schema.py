"""Tests for the OOP SCHEMA (C4): AST extraction, classDiagram, PNG render."""

from __future__ import annotations

from cosmos77_ex04.reveng.oop_schema import (
    extract_classes,
    oop_mermaid,
    render_oop_png,
)


def test_extract_classes_finds_class_base_and_method(package):
    classes = extract_classes(package)
    by_name = {c.name: c for c in classes}
    assert "Base" in by_name and "Child" in by_name
    assert by_name["Child"].bases == ["Base"]
    assert "greet" in by_name["Base"].methods
    assert by_name["Child"].file == "child.py"


def test_extract_classes_accepts_single_file(package):
    classes = extract_classes(package / "base.py")
    assert [c.name for c in classes] == ["Base"]


def test_extract_classes_skips_broken_file(package, tmp_path):
    (package / "broken.py").write_text("class : oops\n", encoding="utf-8")
    names = {c.name for c in extract_classes(package)}
    assert names == {"Base", "Child"}


def test_oop_mermaid_contains_classdiagram_and_inheritance(package):
    classes = extract_classes(package)
    text = oop_mermaid(classes)
    assert text.startswith("classDiagram")
    assert "Base <|-- Child" in text
    assert "+greet()" in text


def test_extract_classes_handles_dotted_and_subscript_bases(tmp_path):
    src = tmp_path / "mod.py"
    src.write_text(
        "import abc\n\n\nclass A(abc.ABC):\n    pass\n\n\nclass B(list[int]):\n    pass\n",
        encoding="utf-8",
    )
    by_name = {c.name: c for c in extract_classes(src)}
    assert by_name["A"].bases == ["ABC"]  # dotted base -> attr name
    assert by_name["B"].bases == []  # subscript base is dropped (best-effort)


def test_render_oop_png_writes_file(package, tmp_path):
    classes = extract_classes(package)
    out = render_oop_png(classes, tmp_path / "oop.png")
    assert out.exists()
    assert out.suffix == ".png"
    assert out.stat().st_size > 0
