from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments


BASE = Path("out/raphael_natural_v2_accepted_base.nds")
BATCHES = [Path(f"translations/raphael_deep_route_v{i}.json") for i in range(1, 18)] + [
    Path("translations/raphael_deep_route_v18a.json"), Path("translations/raphael_deep_route_v18b.json")
]
COUNTS = (59, 92, 57, 26, 114, 84, 120, 66, 71, 40, 58, 84, 16, 17, 46, 29, 25, 48, 22)


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_raphael_v18_inventory_layout_and_cumulative_segments() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC0.DK4")
    rows = []
    for path, count in zip(BATCHES, COUNTS, strict=True):
        batch = _load(path)
        assert len(batch["records"]) == count
        profile = get_dialogue_profile(str(batch["dialogue_profile"]))
        materialized = materialize_translation_batch(batch, source)
        for row in materialized:
            audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
            errors = [issue for issue in audit["issues"] if issue["severity"] == "error"]
            assert not errors, (row["id"], errors)
        rows.extend(materialized)
    rebuilt = rebuild_mesfile(source, rows)
    expected = {(int(row["id"].split("_B", 1)[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 1074
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(parsed_source.blocks[block].split(b"\0")[index])


def test_raphael_v18_release_stack_and_ruin_coverage() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["raphael-deep-route-v18"]["batches"][:-2] == profiles["raphael-deep-route-v17"]["batches"]
    assert profiles["raphael-deep-route-v18"]["batches"][-2:] == [path.as_posix() for path in BATCHES[-2:]]
    v18a, v18b = (_load(path) for path in BATCHES[-2:])
    assert v18a["inventory"] == {"identified_records": 49, "translated_records": 48, "blocks": {"119": 18, "121": 30}}
    assert v18b["inventory"] == {"identified_records": 22, "translated_records": 22, "blocks": {"120": 22}}
    assert len(v18a["excluded_records"]) == 1 and not v18b["excluded_records"]
    text = "\n".join(record["english"] for batch in (v18a, v18b) for record in batch["records"])
    for term in ("pour left-handed", "frozen sea", "Save my grandson"):
        assert term in text
