from __future__ import annotations

import json
import re
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.sjis_scan import contains_japanese
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import apply_arm9_fixed_batch

BASE = Path("out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds")
COMMON_BATCH = Path("translations/common_shipyard_complete_v1.json")
ARM9_BATCH = Path("translations/shipyard_ui_arm9_v1.json")
STACK = Path("translations/release_stack.json")

PACKED_STARTS = {
    47: [0, 21],
    48: [0, 29, 49, 117, 145],
    49: [0, 25],
    50: [0, 70, 138],
    56: [0, 57],
    61: [0, 66],
    62: [0],
    63: [0],
    64: [0, 65, 133, 197],
}


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _common_records(data: bytes) -> list[bytes]:
    return IlnkContainer.parse(data).blocks[15].split(b"\0")


def test_packed_shipyard_messages_keep_every_original_entry_point() -> None:
    source = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    rows = materialize_translation_batch(_load(COMMON_BATCH), source)
    rebuilt = rebuild_mesfile(source, rows)
    before = _common_records(source)
    after = _common_records(rebuilt)

    for index, starts in PACKED_STARTS.items():
        assert len(after[index]) == len(before[index])
        assert not contains_japanese(after[index].decode("cp932"))
        for position, start in enumerate(starts):
            assert after[index][start : start + 2] == b"  "
            end = starts[position + 1] if position + 1 < len(starts) else len(after[index])
            assert all(len(line.rstrip()) <= 31 for line in after[index][start:end].split(b"\n"))
            assert all(part.startswith(b"  ") for part in after[index][start:end].split(b"\n")[1:])

    assert after[48][117:].startswith(b"  Which ship gets renamed?")
    assert after[48][145:].startswith(b"  Give it any name you like.")
    assert after[48].count(b"%s") == 1
    assert after[48].count(b"%%") == 1
    assert b"investigated" not in b"".join(after[index].lower() for index in PACKED_STARTS)


def test_shipyard_arm9_batch_covers_reported_ui_and_all_cannon_names() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, record_ids = apply_arm9_fixed_batch(ARM9_BATCH, source)
    batch = _load(ARM9_BATCH)
    records = batch["records"]
    assert isinstance(records, list)
    assert len(record_ids) == len(records) == 36

    for record in records:
        offset = int(record["offset"])
        size = len(bytes.fromhex(str(record["source_hex"])))
        decoded = rebuilt[offset : offset + size].rstrip(b"\0").decode("cp932")
        assert not contains_japanese(decoded)

    assert rebuilt[0x1484B4 : 0x1484C8].rstrip(b"\0") == b"Ship %s"
    assert rebuilt[0x133154 : 0x133160].rstrip(b"\0") == b"Equipment"
    assert rebuilt[0x1339B0 : 0x1339BC].rstrip(b"\0") == b"Cannon Type"
    assert rebuilt[0x1339C8 : 0x1339D0].rstrip(b"\0") == b"Lateen"
    assert rebuilt[0x11B5EC : 0x11B5F8].rstrip(b"\0") == b"Reset"

    cannon_offsets = [0x13C194, 0x13C1A7, 0x13C1BA, 0x13C1CD, 0x13C1E0, 0x13C1F3]
    names = [rebuilt[offset : offset + 17].rstrip(b"\0") for offset in cannon_offsets]
    assert names == [b"Saker ", b"Culverin ", b"Pedrero ", b"Cannon ", b"Heavy Cannon ", b"Carronade "]


def test_ship_catalog_remains_complete_and_intentionally_compact() -> None:
    from dk4tool.script.arm9_profiles import SHIP_MODEL_ENTRIES

    assert len(SHIP_MODEL_ENTRIES) == 119
    translations = {entry.japanese: entry.suggested_english for entry in SHIP_MODEL_ENTRIES}
    assert translations["フリュート"] == "Fluyt"
    assert translations["ピンネース"] == "Pinnace"
    assert translations["小型ガレー"] == "Sm Galley"
    assert translations["大型ガレー"] == "Lg Galley"
    assert all(not contains_japanese(entry.suggested_english) for entry in SHIP_MODEL_ENTRIES)


def test_shipyard_profile_layers_the_complete_pass_on_v5() -> None:
    profile = _load(STACK)["profiles"]["shipyard-complete-v1"]
    assert profile["status"] == "experimental"
    assert profile["batches"][-2:] == [COMMON_BATCH.as_posix(), ARM9_BATCH.as_posix()]
    assert "translations/common_placeholder_english_v1.json" in profile["batches"]
