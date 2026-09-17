from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments


BASE_ROM = Path("out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds")
BATCHES = (
    Path("translations/raphael_story_natural_v2_b49_b51.json"),
    Path("translations/raphael_story_natural_v2_b54_b56.json"),
    Path("translations/raphael_story_natural_v2_b57_b59.json"),
    Path("translations/raphael_story_natural_v2_b60.json"),
    Path("translations/raphael_story_natural_v2_b61_b63.json"),
    Path("translations/raphael_story_natural_v2_b64_b67.json"),
)
SC0_SHA256 = "cd98015ebaa5016663fce63bcf2e647f33e8a7bbce9a53fcb331cea56252b8ea"


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_raphael_story_push_is_source_locked_complete_and_qa_clean() -> None:
    sc0 = NdsImage.open(BASE_ROM).read_file("/data/SC0.DK4")
    assert hashlib.sha256(sc0).hexdigest() == SC0_SHA256

    rows: list[dict[str, object]] = []
    ids: set[str] = set()
    expected_counts = (103, 30, 58, 97, 74, 204)
    for path, expected_count in zip(BATCHES, expected_counts, strict=True):
        batch = _load(path)
        assert batch["source_file_sha256"] == SC0_SHA256
        assert len(batch["records"]) == expected_count
        profile = get_dialogue_profile(str(batch["dialogue_profile"]))
        waiver_map = {
            str(record["id"]): set(record.get("qa_waivers", []))
            for record in batch["records"]
        }
        materialized = materialize_translation_batch(batch, sc0)
        for row in materialized:
            row_id = str(row["id"])
            assert row_id not in ids
            ids.add(row_id)
            audit = audit_fixed_dialogue_record(
                bytes.fromhex(str(row["source_hex"])), str(row["english"]), profile
            )
            waivers = waiver_map[row_id]
            blockers = [
                issue
                for issue in audit["issues"]
                if issue["severity"] in {"warning", "error"}
                and issue["code"] not in waivers
            ]
            assert blockers == [], row_id
        rows.extend(materialized)

    assert len(ids) == 566
    rebuilt = rebuild_mesfile(sc0, rows)
    assert len(changed_segments(sc0, rebuilt)) == 566


def test_late_printable_speaker_states_are_isolated_from_accepted_profile() -> None:
    accepted = get_dialogue_profile("raphael-story-live")
    late = get_dialogue_profile("raphael-story-late-live")
    assert accepted.leading_speaker_bytes == frozenset({0x18, 0x4B, 0x71})
    assert late.leading_speaker_bytes == frozenset(
        {0x14, 0x18, 0x25, 0x27, 0x4B, 0x50, 0x54, 0x71, 0x72, 0x74}
    )
