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
BATCH = Path("translations/lil_deep_route_v1.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_lil_v1_inventory_layout_and_exact_segments() -> None:
    batch = _load(BATCH)
    assert len(batch["records"]) == 61
    assert batch["inventory"]["identified_records"] == 61
    source = NdsImage.open(BASE).read_file("/data/SC2.DK4")
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    rows = materialize_translation_batch(batch, source)
    failures = []
    for row in rows:
        audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
        errors = [issue for issue in audit["issues"] if issue["severity"] == "error"]
        if errors:
            failures.append((row["id"], errors))
    assert not failures, "\n".join(f"{row_id}: {errors}" for row_id, errors in failures)
    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (int(row["id"].split("_B", 1)[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 61
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(
            parsed_source.blocks[block].split(b"\0")[index]
        )


def test_lil_v1_macros_profile_and_release_stack() -> None:
    batch = _load(BATCH)
    by_id = {record["id"]: record["english"] for record in batch["records"]}
    assert "{MACRO:FO}" in by_id["DK4_MES_B03_R0006"]
    assert "{MACRO:FI}" in by_id["DK4_MES_B11_R0018"]
    profile = get_dialogue_profile("lil-story-deep-route-live")
    assert {0x02, 0x09, 0x17, 0x1B, 0x22, 0x40, 0x41, 0x43, 0x44, 0x46, 0x99, 0xB7, 0xB8, 0xB9} <= profile.leading_speaker_bytes
    release = _load(Path("translations/release_stack.json"))["profiles"]["lil-deep-route-v1"]
    assert release["batches"][-1] == BATCH.as_posix()
    assert release["require_screen_entry_layout"] is True
