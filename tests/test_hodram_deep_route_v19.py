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
from scripts.materialize_hodram_deep_route_v19 import BLOCKS, EXCLUDED, LINES


BASE = Path("out/raphael_natural_v2_accepted_base.nds")
V19 = Path("translations/hodram_deep_route_v19.json")
PRIOR = [Path(f"translations/hodram_deep_route_v{i}.json") for i in (1, 2, 3)] + [
    Path("translations/hodram_deep_route_v4a.json"), Path("translations/hodram_deep_route_v4b.json"),
    Path("translations/hodram_deep_route_v5.json"), Path("translations/hodram_deep_route_v6a.json"),
    Path("translations/hodram_deep_route_v6b.json"), Path("translations/hodram_deep_route_v7.json"),
    Path("translations/hodram_deep_route_v8.json"), Path("translations/hodram_deep_route_v9.json"),
    Path("translations/hodram_deep_route_v10.json"), Path("translations/hodram_deep_route_v11.json"),
    Path("translations/hodram_deep_route_v12.json"), Path("translations/hodram_deep_route_v13.json"),
    Path("translations/hodram_deep_route_v14.json"), Path("translations/hodram_deep_route_v15.json"),
    Path("translations/hodram_deep_route_v16.json"), Path("translations/hodram_deep_route_v17.json"),
    Path("translations/hodram_deep_route_v18.json"),
]


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_hodram_v19_inventory_layout_and_controls() -> None:
    batch = _load(V19)
    assert len(batch["records"]) == len(LINES) == 111
    assert batch["inventory"]["identified_records"] == 112
    assert batch["excluded_records"] == EXCLUDED == {
        "DK4_MES_B243_R0100": "Raw two-byte event-control payload; not dialogue."
    }
    assert set(batch["inventory"]["blocks"]) == {str(block) for block in BLOCKS}
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile("hodram-story-relic-live")
    for row in rows:
        audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
        assert not [issue for issue in audit["issues"] if issue["severity"] == "error"], (row["id"], audit)
    assert {0x93, 0xBA, 0xC1, 0xC3, 0xC4} <= profile.leading_speaker_bytes
    assert 0x82 not in profile.leading_speaker_bytes


def test_hodram_v19_cumulative_changed_records_are_exact() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    rows = []
    for path in [*PRIOR, V19]:
        rows.extend(materialize_translation_batch(_load(path), source))
    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (int(row["id"].split("_B", 1)[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 3408
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(
            parsed_source.blocks[block].split(b"\0")[index]
        )
    assert parsed_rebuilt.blocks[243].split(b"\0")[100] == parsed_source.blocks[243].split(b"\0")[100]


def test_hodram_v19_release_stack_extends_v18() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["hodram-deep-route-v19"]["batches"][:-1] == profiles["hodram-deep-route-v18"]["batches"]
    assert profiles["hodram-deep-route-v19"]["batches"][-1] == V19.as_posix()
    assert not (set(EXCLUDED) & set(LINES))
