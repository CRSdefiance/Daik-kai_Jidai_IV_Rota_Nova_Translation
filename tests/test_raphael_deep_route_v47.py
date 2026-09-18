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
    Path("translations/raphael_deep_route_v18a.json"), Path("translations/raphael_deep_route_v18b.json"),
    *[Path(f"translations/raphael_deep_route_v{i}.json") for i in range(19, 39)],
    Path("translations/raphael_deep_route_v39a.json"), Path("translations/raphael_deep_route_v39b.json"),
    *[Path(f"translations/raphael_deep_route_v{i}.json") for i in range(40, 48)],
]
COUNTS = (59, 92, 57, 26, 114, 84, 120, 66, 71, 40, 58, 84, 16, 17, 46, 29, 25, 48, 22, 36, 43, 79, 40, 15, 52, 6, 85, 24, 53, 19, 14, 37, 7, 18, 42, 46, 11, 33, 31, 20, 1, 51, 39, 43, 25, 48, 56, 48, 106)


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_raphael_v47_inventory_layout_and_cumulative_segments() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC0.DK4")
    rows = []
    for path, count in zip(BATCHES, COUNTS, strict=True):
        batch = _load(path)
        assert len(batch["records"]) == count
        profile = get_dialogue_profile(str(batch["dialogue_profile"]))
        materialized = materialize_translation_batch(batch, source)
        for row in materialized:
            audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
            assert not [issue for issue in audit["issues"] if issue["severity"] == "error"], row["id"]
        rows.extend(materialized)
    rebuilt = rebuild_mesfile(source, rows)
    expected = {(int(row["id"].split("_B", 1)[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 2202
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(parsed_source.blocks[block].split(b"\0")[index])


def test_raphael_v47_release_stack_and_recruitment_coverage() -> None:
    batch = _load(BATCHES[-1])
    assert batch["inventory"] == {"identified_records": 107, "translated_records": 106, "blocks": {"168": 45, "169": 61}}
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["raphael-deep-route-v47"]["batches"][:-1] == profiles["raphael-deep-route-v46"]["batches"]
    assert profiles["raphael-deep-route-v47"]["batches"][-1] == BATCHES[-1].as_posix()
    text = "\n".join(record["english"] for record in batch["records"])
    for term in ("Angelo Puccini", "powder monkey", "New World", "Dukov", "join your ship"):
        assert term.lower() in text.lower()
