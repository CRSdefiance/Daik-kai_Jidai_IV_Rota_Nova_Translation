from __future__ import annotations

import csv
import json
import re
from pathlib import Path


SCRIPT = Path("work/sc2/script.csv")
DEEP_BATCHES = [Path(f"translations/lil_deep_route_v{i}.json") for i in range(1, 21)]
OPENING = Path("translations/lil_sc2_b22_intro_natural_v2.json")
OPENING_CONTROLS = {
    "DK4_MES_B22_R0077",
    "DK4_MES_B22_R0088",
    "DK4_MES_B22_R0124",
}
JAPANESE = re.compile(r"[ぁ-んァ-ヶ一-龠]")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_lil_route_japanese_inventory_is_fully_accounted_through_block_79() -> None:
    with SCRIPT.open(encoding="utf-8-sig", newline="") as stream:
        route_japanese = {
            row["id"]
            for row in csv.DictReader(stream)
            if int(row["id"].split("_B", 1)[1].split("_", 1)[0]) <= 79
            and JAPANESE.search(row["japanese"])
        }
    translated: set[str] = set()
    controls: set[str] = set()
    for path in DEEP_BATCHES:
        batch = _load(path)
        batch_ids = {record["id"] for record in batch["records"]}
        assert translated.isdisjoint(batch_ids), path
        translated.update(batch_ids)
        controls.update(batch.get("excluded_records", {}))
    opening = _load(OPENING)
    opening_ids = {record["id"] for record in opening["records"]}
    assert len(opening_ids) == 49
    assert route_japanese - translated - controls == opening_ids | OPENING_CONTROLS
    assert not route_japanese - translated - controls - opening_ids - OPENING_CONTROLS
    assert len(translated) == 1749
    assert len(route_japanese) == 1816
