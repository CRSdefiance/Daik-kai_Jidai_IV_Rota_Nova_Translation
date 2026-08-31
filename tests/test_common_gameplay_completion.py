from __future__ import annotations

import json
from pathlib import Path

INVENTORY = Path("work/analysis/common_clean_inventory.json")
SAFE_BATCHES = [
    Path(f"translations/common_natural_v2_b{block}_safe.json")
    for block in range(22, 28)
] + [
    Path("translations/common_natural_v2_b28_b29_b34_safe_qa.json"),
    Path("translations/common_natural_v2_b30_b33_safe.json"),
    Path("translations/common_natural_v2_b35_safe.json"),
    Path("translations/common_natural_v2_b36_safe.json"),
    Path("translations/common_natural_v2_b38_safe.json"),
    Path("translations/common_natural_v2_b39_safe.json"),
]
BLOCKED_BATCHES = [
    Path(f"translations/common_natural_v2_b{block}_blocked.json")
    for block in range(22, 28)
] + [
    Path("translations/common_natural_v2_b28_b29_b34_blocked.json"),
    Path("translations/common_natural_v2_b28_b29_b34_qa_blocked.json"),
    Path("translations/common_natural_v2_b30_b33_blocked.json"),
    Path("translations/common_natural_v2_b35_b40_blocked.json"),
]
PADDING_ONLY = {"DK4_MES_B38_R0052", "DK4_MES_B40_R0031"}


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def ids(paths: list[Path]) -> set[str]:
    return {
        str(record["id"])
        for path in paths
        for record in load(path).get("records", [])
    }


def test_common_blocks_22_through_40_are_fully_classified() -> None:
    expected = {
        f"DK4_MES_B{int(record['block_index']):02d}_R{int(record['segment_index']):04d}"
        for record in load(INVENTORY)["records"]
        if 22 <= int(record["block_index"]) <= 40
    }
    safe = ids(SAFE_BATCHES)
    blocked = ids(BLOCKED_BATCHES)

    assert not safe & blocked
    assert not (safe | blocked) & PADDING_ONLY
    assert safe | blocked | PADDING_ONLY == expected


def test_safe_completion_batches_have_no_placeholder_filler() -> None:
    forbidden = ("see below", "another strategy", "the scheme is ready")
    for path in SAFE_BATCHES:
        for record in load(path)["records"]:
            english = str(record["english"]).lower()
            assert not any(value in english for value in forbidden)
            assert english.endswith("{pad}")
