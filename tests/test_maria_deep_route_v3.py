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
BATCH = Path("translations/maria_deep_route_v3.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_maria_v3_inventory_and_layout() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 87,
        "translated_records": 86,
        "excluded_records": 1,
        "blocks": {"252": 86},
    }
    assert set(batch["excluded_records"]) == {"DK4_MES_B252_R0037"}
    source = NdsImage.open(BASE).read_file("/data/SC3.DK4")
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    failures = []
    for row in materialize_translation_batch(batch, source):
        audit = audit_fixed_dialogue_record(
            bytes.fromhex(row["source_hex"]), row["english"], profile
        )
        errors = [issue for issue in audit["issues"] if issue["severity"] == "error"]
        if errors:
            failures.append((row["id"], errors))
    assert not failures, "\n".join(f"{row_id}: {errors}" for row_id, errors in failures)


def test_maria_v3_preserves_states_and_exact_allocations() -> None:
    batch = _load(BATCH)
    by_id = {record["id"]: record["english"] for record in batch["records"]}
    assert by_id["DK4_MES_B252_R0020"].startswith("{SPEAKER:D3}")
    assert by_id["DK4_MES_B252_R0048"].startswith("{SPEAKER:D0}")
    assert by_id["DK4_MES_B252_R0061"].startswith("{SPEAKER:03}")
    assert by_id["DK4_MES_B252_R0095"].startswith("{SPEAKER:D7}")
    assert by_id["DK4_MES_B252_R0135"].startswith("{SPEAKER:D8}")
    assert by_id["DK4_MES_B252_R0217"].startswith("{SPEAKER:0E}")
    assert by_id["DK4_MES_B252_R0277"].startswith("{SPEAKER:16}")
    assert by_id["DK4_MES_B252_R0304"].startswith("{SPEAKER:FE}")

    source = NdsImage.open(BASE).read_file("/data/SC3.DK4")
    rows = materialize_translation_batch(batch, source)
    rebuilt = rebuild_mesfile(source, rows)
    expected = {(252, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 86
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(
            parsed_source.blocks[block].split(b"\0")[index]
        )


def test_maria_v3_profile_and_release_registration() -> None:
    profile = get_dialogue_profile("maria-story-shared-events-live")
    assert {0x03, 0x0E, 0x16, 0xD0, 0xD3, 0xD7, 0xD8, 0xFE} <= (
        profile.leading_speaker_bytes
    )
    release = _load(Path("translations/release_stack.json"))
    registered = release["profiles"]["maria-deep-route-v3"]
    assert registered["status"] == "experimental"
    assert registered["batches"][-1] == BATCH.as_posix()
