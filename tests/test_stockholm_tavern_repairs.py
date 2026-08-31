from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch

BASE = Path("out/raphael_natural_v2_pre_common_accepted_rollback.nds")
NATURAL = Path("translations/stockholm_tavern_rumor_natural_v2.json")
PACKED = Path("translations/stockholm_tavern_interior_fixed_v1.json")
COMMON_SHA256 = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"

PACKED_ENTRIES = {
    "DK4_MES_B00_R0037": [(1, "That'll be 10 coins."), (21, "5 coins.")],
    "DK4_MES_B00_R0038": [(1, "Please serve %s.")],
    "DK4_MES_B00_R0039": [(2, "Hey, %s!"), (14, "On it!")],
    "DK4_MES_B00_R0040": [(1, "Welcome!")],
    "DK4_MES_B00_R0041": [(1, "Welcome, %s!")],
    "DK4_MES_B00_R0042": [(2, "Here, have another drink.")],
    "DK4_MES_B00_R0043": [(1, "That'll be 20 coins.")],
    "DK4_MES_B00_R0044": [(1, "Ten coins.")],
    "DK4_MES_B10_R0039": [
        (2, "Drinks aren't free."),
        (22, "%s serves %s as %s."),
    ],
    "DK4_MES_B10_R0041": [
        (0, "Have you visited the nearby town of %s?"),
        (48, "Know %s? It's nearby."),
    ],
    "DK4_MES_B10_R0043": [
        (0, "Hm?"),
        (4, "You're pretty weak."),
        (24, "Right..."),
        (32, "%s, right?"),
        (43, "A toast to our new friendship!"),
    ],
}


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _common() -> bytes:
    data = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    assert hashlib.sha256(data).hexdigest() == COMMON_SHA256
    return data


def test_natural_rumor_is_source_locked_pair_safe_and_reviewed() -> None:
    common = _common()
    batch = _load(NATURAL)
    assert batch["translation_policy"] == "natural-dialogue-v2"
    rows = materialize_translation_batch(batch, common)
    assert [row["id"] for row in rows] == ["DK4_MES_B10_R0040", "DK4_MES_B10_R0042"]
    authored = {str(record["id"]): record for record in batch["records"]}
    for row in rows:
        audit = audit_fixed_dialogue_record(
            bytes.fromhex(str(row["source_hex"])),
            str(row["english"]),
            get_dialogue_profile("shared-pair-live"),
        )
        record = authored[str(row["id"])]
        waivers = set(record["qa_waivers"])
        assert not [
            issue
            for issue in audit["issues"]
            if issue["severity"] in {"warning", "error"} and issue["code"] not in waivers
        ]
        assert waivers == {"line-break-count"}
        assert record["qa_waiver_reason"]
        assert all(record["review"].values())


def test_packed_records_preserve_all_documented_entry_offsets() -> None:
    common = _common()
    blocks = IlnkContainer.parse(common).blocks
    batch = _load(PACKED)
    authored = {str(record["id"]): record for record in batch["records"]}
    assert set(authored) == set(PACKED_ENTRIES)

    for row_id, entries in PACKED_ENTRIES.items():
        block_index = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        record_index = int(row_id.rsplit("R", 1)[1])
        source = blocks[block_index].split(b"\0")[record_index]
        replacement = bytes.fromhex(str(authored[row_id]["replacement_hex"]))
        assert len(source) == len(replacement)
        assert authored[row_id]["interior_entries"] == [
            {"offset": offset, "english": text} for offset, text in entries
        ]
        for index, (offset, text) in enumerate(entries):
            end = entries[index + 1][0] if index + 1 < len(entries) else len(source)
            encoded = text.encode("ascii")
            assert len(encoded) <= end - offset
            assert replacement[offset : offset + len(encoded)] == encoded
            assert replacement[offset + len(encoded) : end] == b" " * (
                end - offset - len(encoded)
            )
        assert all(authored[row_id]["review"].values())
