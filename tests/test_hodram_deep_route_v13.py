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
from scripts.materialize_hodram_deep_route_v13 import BLOCKS, EXCLUDED, LINES


BASE = Path("out/raphael_natural_v2_accepted_base.nds")
V13 = Path("translations/hodram_deep_route_v13.json")
PRIOR = [Path(f"translations/hodram_deep_route_v{i}.json") for i in (1, 2, 3)] + [
    Path("translations/hodram_deep_route_v4a.json"),
    Path("translations/hodram_deep_route_v4b.json"),
    Path("translations/hodram_deep_route_v5.json"),
    Path("translations/hodram_deep_route_v6a.json"),
    Path("translations/hodram_deep_route_v6b.json"),
    Path("translations/hodram_deep_route_v7.json"),
    Path("translations/hodram_deep_route_v8.json"),
    Path("translations/hodram_deep_route_v9.json"),
    Path("translations/hodram_deep_route_v10.json"),
    Path("translations/hodram_deep_route_v11.json"),
    Path("translations/hodram_deep_route_v12.json"),
]


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_hodram_v13_inventory_layout_and_controls() -> None:
    batch = _load(V13)
    assert len(batch["records"]) == len(LINES) == 164
    assert batch["inventory"]["identified_records"] == 166
    assert batch["excluded_records"] == EXCLUDED
    assert set(batch["inventory"]["blocks"]) == {str(block) for block in BLOCKS}
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile("hodram-story-ifa-live")
    for row in rows:
        audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
        assert not [issue for issue in audit["issues"] if issue["severity"] == "error"], (row["id"], audit)


def test_hodram_v13_cumulative_changed_records_are_exact() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    rows = []
    for path in [*PRIOR, V13]:
        rows.extend(materialize_translation_batch(_load(path), source))
    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (int(row["id"].split("_B", 1)[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 2410
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(
            parsed_source.blocks[block].split(b"\0")[index]
        )


def test_hodram_v13_release_stack_extends_v12_and_scopes_states() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["hodram-deep-route-v13"]["batches"][:-1] == profiles["hodram-deep-route-v12"]["batches"]
    assert profiles["hodram-deep-route-v13"]["batches"][-1] == V13.as_posix()
    profile = get_dialogue_profile("hodram-story-ifa-live")
    assert {0x51, 0x99, 0xB7, 0xC9, 0xCA} <= profile.leading_speaker_bytes
    assert not (set(EXCLUDED) & set(LINES))
