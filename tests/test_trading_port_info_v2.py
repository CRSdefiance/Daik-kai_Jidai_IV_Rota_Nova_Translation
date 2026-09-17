from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import (
    apply_arm9_fixed_batch,
    apply_obj_label_batch,
    apply_pxl_native_label_batch,
)
from scripts.materialize_trading_dialogue_polish_v2 import RECORDS, build_record


BASE = Path("out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds")
ARM9_BATCH = Path("translations/trading_port_info_arm9_v2.json")
DIALOGUE_BATCH = Path("translations/trading_dialogue_polish_v2.json")
PXL_BATCH = Path("translations/trading_towninfo_graphics_v2.json")
OBJ_BATCH = Path("translations/port_market_header_obj_v1.json")
STACK = Path("translations/release_stack.json")
ARM9_LOAD_ADDRESS = 0x02000000


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_port_type_sailor_and_every_live_region_are_english() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, ids = apply_arm9_fixed_batch(ARM9_BATCH, source)
    assert len(ids) == 21
    assert rebuilt[0x1565E0 : 0x1565EA] == b"Port\0City\0"
    assert struct.unpack_from("<I", rebuilt, 0x0B5214)[0] == ARM9_LOAD_ADDRESS + 0x1565E5
    assert rebuilt[0x1484D4 : 0x1484DC] == b"Sailor\0\0"

    regions = []
    for index in range(19):
        pointer_offset = 0x11F880 + index * 0x100
        target = struct.unpack_from("<I", rebuilt, pointer_offset)[0] - ARM9_LOAD_ADDRESS
        regions.append(rebuilt[target : rebuilt.index(0, target)].decode("ascii"))
    assert regions == [
        "German", "Nordic", "Portugal", "Spain", "Italy", "Greece", "Turkey",
        "Egypt", "West Africa", "East Africa", "Arab", "India", "Indochina",
        "Indonesia", "China", "Korea", "Japan", "Caribbean", "Mexico",
    ]


def test_trader_polish_preserves_packed_entry_offsets_and_avoids_uppercase_i() -> None:
    common = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    batch = load(DIALOGUE_BATCH)
    rows = materialize_translation_batch(batch, common)
    assert len(rows) == 2
    blocks = IlnkContainer.parse(common).blocks
    authored = {str(row["id"]): row for row in batch["records"]}
    for record_id, spec in RECORDS.items():
        block = int(record_id.split("_B", 1)[1].split("_", 1)[0])
        record = int(record_id.rsplit("R", 1)[1])
        source = blocks[block].split(b"\0")[record]
        replacement = bytes.fromhex(str(authored[record_id]["replacement_hex"]))
        assert replacement == build_record(source, list(spec["entries"]))
    greeting = bytes.fromhex(str(authored["DK4_MES_B00_R0008"]["replacement_hex"]))
    assert greeting[2:12] == b"Need help?"
    assert b"I" not in greeting[2:14]


def test_towninfo_native_redraw_is_box_limited() -> None:
    image = NdsImage.open(BASE)
    source = image.read_file("/_pxl/towninfo.pxl")
    arm9 = image.read_file("/__arm9__.bin")
    batch = load(PXL_BATCH)
    rebuilt, ids = apply_pxl_native_label_batch(PXL_BATCH, source, arm9)
    assert len(ids) == 6
    before = PxlImage.from_bytes(source)
    after = PxlImage.from_bytes(rebuilt)
    boxes = [tuple(record["box"]) for record in batch["records"]]
    for position, (old, new) in enumerate(zip(before.indices, after.indices, strict=True)):
        if old == new:
            continue
        x = position % before.width
        y = position // before.width
        assert any(left <= x < right and top <= y < bottom for left, top, right, bottom in boxes)


def test_live_port_market_header_changes_only_its_declared_tiles() -> None:
    image = NdsImage.open(BASE)
    source = image.read_file("/GRP/DSOBJ.DK4")
    arm9 = image.read_file("/__arm9__.bin")
    rebuilt, ids = apply_obj_label_batch(OBJ_BATCH, source, arm9)
    assert ids == ["DK4_PORT_MARKET_HEADER_NATIVE"]
    changed = {index // 32 for index, (old, new) in enumerate(zip(source, rebuilt, strict=True)) if old != new}
    assert changed
    assert changed <= set(range(368, 400))


def test_raphael_story_profile_registers_complete_port_polish() -> None:
    batches = load(STACK)["profiles"]["raphael-story-push-v1"]["batches"]
    for path in (ARM9_BATCH, DIALOGUE_BATCH, PXL_BATCH, OBJ_BATCH):
        assert path.as_posix() in batches
    assert "translations/trading_towninfo_graphics_v1.json" not in batches
