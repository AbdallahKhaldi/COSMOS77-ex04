"""Tests for the naive raw-file baseline arm (C8 — LLM mocked, tokens measured)."""

from __future__ import annotations

from langchain_core.messages import AIMessage

from cosmos77_ex04.shared.gatekeeper import Gatekeeper
from cosmos77_ex04.tokens.baseline import (
    baseline_prompt,
    collect_source_files,
    run_baseline,
)


class FakeLLM:
    """Returns a canned diagnosis with usage_metadata; records the prompt."""

    def __init__(self) -> None:
        self.prompts: list[str] = []

    def invoke(self, prompt: str) -> AIMessage:
        self.prompts.append(prompt)
        return AIMessage(
            content="ROOT CAUSE: off-by-one\nFILE: mod.py",
            usage_metadata={"input_tokens": 900, "output_tokens": 40, "total_tokens": 940},
        )


def _tree(tmp_path):
    pkg = tmp_path / "pkg"
    (pkg / "sub").mkdir(parents=True)
    (pkg / "a.py").write_text("def a():\n    return 1\n", encoding="utf-8")
    (pkg / "sub" / "b.py").write_text("def b():\n    return 2\n", encoding="utf-8")
    (pkg / "README.md").write_text("not python", encoding="utf-8")
    cache = pkg / "__pycache__"
    cache.mkdir()
    (cache / "c.py").write_text("ignored", encoding="utf-8")
    return pkg


def test_collect_reads_every_python_file(tmp_path):
    pkg = _tree(tmp_path)
    files = collect_source_files(pkg)
    assert set(files) == {"a.py", "sub/b.py"}
    assert "return 1" in files["a.py"]


def test_collect_respects_max_files_cap(tmp_path):
    pkg = _tree(tmp_path)
    files = collect_source_files(pkg, max_files=1)
    assert len(files) == 1


def test_baseline_prompt_includes_all_files_and_test(tmp_path):
    pkg = _tree(tmp_path)
    files = collect_source_files(pkg)
    prompt = baseline_prompt("pkg/tests::test_x", "Traceback here", files)
    assert "pkg/tests::test_x" in prompt
    assert "Traceback here" in prompt
    assert "a.py" in prompt and "sub/b.py" in prompt


def test_run_baseline_meters_tokens_and_returns_all_files(tmp_path):
    pkg = _tree(tmp_path)
    llm = FakeLLM()
    gk = Gatekeeper()
    result = run_baseline(llm, gk, pkg, "pkg/tests::test_x", "trace")

    assert result["iterations"] == 1
    assert len(llm.prompts) == 1
    assert sorted(result["files_read"]) == ["a.py", "sub/b.py"]
    assert result["tokens"]["total_tokens"] == 940
    assert result["tokens"]["calls"] == 1
    assert "ROOT CAUSE" in result["diagnosis"]
