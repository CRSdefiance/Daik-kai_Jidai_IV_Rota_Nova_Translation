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
from scripts.materialize_hodram_deep_route_v20 import (
    BLOCKS_A, BLOCKS_B, EXCLUDED_A, EXCLUDED_B, LINES_A, LINES_B,
)


BASE = Path("out/raphael_natural_v2_accepted_base.nds")
V20 = [Path("translations/hodram_deep_route_v20a.json"), Path("translations/hodram_deep_route_v20b.json")]
PRIOR = [Path(f"translations/hodram_deep_route_v{i}.json") for i in (1, 2, 3)] + [
    Path("translations/hodram_deep_route_v4a.json"), Path("translations/hodram_deep_route_v4b.json"),
    Path("translations/hodram_deep_route_v5.json"), Path("translations/hodram_deep_route_v6a.json"),
    Path("translations/hodram_deep_route_v6b.json"), *[Path(f"translations/hodram_deep_route_v{i}.json") for i in range(7, 20)],
]


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_hodram_v20_inventory_layout_and_ambiguous_leads() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    specs = [
        (V20[0], LINES_A, EXCLUDED_A, BLOCKS_A, "hodram-story-quest-live", 71, 71),
        (V20[1], LINES_B, EXCLUDED_B, BLOCKS_B, "hodram-story-puzzle-live", 49, 50),
    ]
    for path, lines, excluded, blocks, profile_name, translated, identified in specs:
        batch = _load(path)
        assert len(batch["records"]) == len(lines) == translated
        assert batch["inventory"]["identified_records"] == identified
        assert batch["excluded_records"] == excluded
        assert set(batch["inventory"]["blocks"]) == {str(block) for block in blocks}
        profile = get_dialogue_profile(profile_name)
        for row in materialize_translation_batch(batch, source):
            audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
            assert not [issue for issue in audit["issues"] if issue["severity"] == "error"], (row["id"], audit)
    puzzle = get_dialogue_profile("hodram-story-puzzle-live")
    assert not ({0x82, 0x89, 0x8A, 0x8D, 0x90, 0x92, 0x93} & puzzle.leading_speaker_bytes)


def test_hodram_v20_cumulative_changed_records_are_exact() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    rows = []
    for path in [*PRIOR, *V20]:
        rows.extend(materialize_translation_batch(_load(path), source))
    rebuilt = rebuild_mesfile(source, rows)
    expected = {(int(row["id"].split("_B", 1)[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 3528
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(parsed_source.blocks[block].split(b"\0")[index])
    assert parsed_rebuilt.blocks[252].split(b"\0")[186] == parsed_source.blocks[252].split(b"\0")[186]


def test_hodram_v20_release_stack_extends_v19() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["hodram-deep-route-v20"]["batches"][:-2] == profiles["hodram-deep-route-v19"]["batches"]
    assert profiles["hodram-deep-route-v20"]["batches"][-2:] == [path.as_posix() for path in V20]
