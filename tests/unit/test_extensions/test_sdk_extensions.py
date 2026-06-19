"""SDK-level test for run_extensions writing all four C9 deliverables."""

from __future__ import annotations

import json

from cosmos77_ex04.sdk.sdk import SDK


def test_run_extensions_writes_all_four(config):
    repo_root = config.config_dir.parent
    artifacts = repo_root / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    graph = {
        "nodes": [
            {
                "id": "a",
                "label": "tqdm",
                "source_file": "std.py",
                "file_type": "code",
                "community": 0,
                "community_name": "C0",
            },
            {
                "id": "b",
                "label": "helper",
                "source_file": "utils.py",
                "file_type": "code",
                "community": 1,
                "community_name": "C1",
            },
            {
                "id": "orphan",
                "label": "lonely",
                "source_file": "x.py",
                "file_type": "code",
                "community": 2,
                "community_name": "C2",
            },
        ],
        "links": [
            {
                "source": "a",
                "target": "b",
                "relation": "calls",
                "confidence": "EXTRACTED",
                "confidence_score": 1.0,
            }
        ],
    }
    (artifacts / "graph.json").write_text(json.dumps(graph), encoding="utf-8")
    out = SDK(config=config).run_extensions()
    assert out["suspects"].exists()
    assert out["hot"].exists()
    assert out["orphans"].exists()
    assert out["impact"].exists()
    assert out["orphan_count"] >= 1
