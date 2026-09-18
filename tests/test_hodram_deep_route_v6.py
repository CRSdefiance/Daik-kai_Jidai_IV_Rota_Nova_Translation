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
from scripts.materialize_hodram_deep_route_v6 import BLOCKS, EXCLUDED, LINES

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
V6 = [
    Path("translations/hodram_deep_route_v6a.json"),
    Path("translations/hodram_deep_route_v6b.json"),
]
PRIOR = [
    Path("translations/hodram_deep_route_v1.json"),
    Path("translations/hodram_deep_route_v2.json"),
    Path("translations/hodram_deep_route_v3.json"),
    Path("translations/hodram_deep_route_v4a.json"),
    Path("translations/hodram_deep_route_v4b.json"),
    Path("translations/hodram_deep_route_v5.json"),
]


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_hodram_v6_inventory_layout_and_controls() -> None:
    batches = [_load(path) for path in V6]
    assert sum(len(batch["records"]) for batch in batches) == len(LINES) == 142
    assert sum(batch["inventory"]["identified_records"] for batch in batches) == 145
    assert {key: value for batch in batches for key, value in batch["excluded_records"].items()} == EXCLUDED
    assert {key for batch in batches for key in batch["inventory"]["blocks"]} == {str(block) for block in BLOCKS}
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    for batch in batches:
        rows = materialize_translation_batch(batch, source)
        profile = get_dialogue_profile(batch["dialogue_profile"])
        for row in rows:
            audit = audit_fixed_dialogue_record(
                bytes.fromhex(row["source_hex"]), row["english"], profile
            )
            assert not [issue for issue in audit["issues"] if issue["severity"] == "error"], (row["id"], audit)


def test_hodram_v6_cumulative_changed_records_are_exact() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    rows = []
    for path in [*PRIOR, *V6]:
        rows.extend(materialize_translation_batch(_load(path), source))
    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (
            int(row["id"].split("_B", 1)[1].split("_", 1)[0]),
            int(row["id"].rsplit("R", 1)[1]),
        )
        for row in rows
    }
    assert len(expected) == 1106
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(
            parsed_source.blocks[block].split(b"\0")[index]
        )


def test_hodram_v6_release_stack_extends_v5_and_states_are_mapped() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["hodram-deep-route-v6"]["batches"][:-2] == profiles["hodram-deep-route-v5"]["batches"]
    assert profiles["hodram-deep-route-v6"]["batches"][-2:] == [path.as_posix() for path in V6]
    profile = get_dialogue_profile("hodram-story-live")
    assert {0x89, 0x97, 0xA0, 0xB1, 0xB2, 0xCF} <= profile.leading_speaker_bytes
    proof_profile = get_dialogue_profile("hodram-story-proof-live")
    assert 0x89 not in proof_profile.leading_speaker_bytes
    assert 0x8D not in proof_profile.leading_speaker_bytes
