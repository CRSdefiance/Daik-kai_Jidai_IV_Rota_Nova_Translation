"""Source-locked World Map selection headers and consistent village type label."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from scripts.probe_common_display_name_hook import branch_link

SOURCE = "c84e23d6df73b37ce3d9e320048e2c6413bb887e87caba577fbe71ed60080029"
ROOT = Path("work/analysis/world_headers_v261")
SPECS = [(0x11995C, 0x14B858, "艦隊・村", "艦隊・村", "Fleets/Villages"),
         (0x119960, 0x14B840, "海域", "海域", "Sea Areas"),
         (0x8D7A8, 0x14C190, "艦隊・村", "Fleet/Town", "Fleet/Village")]


def transform(source, clean):
    if sha(source) != SOURCE:
        raise ValueError("Exact complete V260 ARM9 required")
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    cache_plan(source)
    packed = bytearray(before[3][:-48])
    preserved = len(packed)
    rows, changes = [], []
    for field, offset, japanese, previous, english in SPECS:
        raw = japanese.encode("cp932") + b"\0"
        if clean[offset:offset + len(raw)] != raw or source[offset:offset + len(previous.encode("cp932")) + 1] != previous.encode("cp932") + b"\0":
            raise ValueError("Original Japanese map header label differs")
        if struct.unpack_from("<I", source, field)[0] != BASE + offset:
            raise ValueError("Map header pointer differs")
        pointer = POOL + len(packed)
        packed.extend(english.encode("ascii") + b"\0")
        struct.pack_into("<I", code.sections[0].data, field, pointer)
        changes.append({"offset": field, "before": BASE + offset, "after": pointer})
        rows.append({"field": field, "source_pointer": BASE + offset, "source_Japanese": japanese,
                     "English": english, "target_pointer": pointer})
    packed.extend(bytes((-len(packed)) % 32))
    size = len(packed) + 64
    if POOL + size > STAGE or STAGE + size + 48 > 0x023F4000:
        raise ValueError("Map header strings escape owned storage")
    entry, copy = STAGE + len(packed), STAGE + size
    packed.extend(wrapper(entry, copy, size, source))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack("<I", size)
    for offset, value in [(0x8E4, branch_link(BASE + 0x8E4, entry)), (0xE45DC, POOL + size)]:
        old = struct.unpack_from("<I", source, offset)[0]
        struct.pack_into("<I", code.sections[0].data, offset, value)
        changes.append({"offset": offset, "before": old, "after": value})
    saved = bytes(code.save())
    parsed = MainCodeFile(saved, BASE)
    restored = bytearray(parsed.sections[0].data)
    for row in changes:
        offset = row["offset"]
        restored[offset:offset + 4] = before[0][offset:offset + 4]
    offset = code.codeSettingsOffs
    restored[offset:offset + 12] = before[0][offset:offset + 12]
    if bytes(restored) != before[0] or any(bytes(parsed.sections[n].data) != before[n] for n in (1, 2)):
        raise ValueError("Unrelated code/data changed")
    if bytes(parsed.sections[3].data[:preserved]) != before[3][:-48]:
        raise ValueError("Inherited payload differs")
    return saved, {"source_arm9_sha256": SOURCE, "target_arm9_sha256": sha(saved), "records": rows,
                   "changes": changes, "cache": cache_plan(saved), "payload_bytes": size,
                   "inherited_pool_bytes_preserved": preserved,
                   "all_three_source_world_selection_labels_relocated": True}


def apply_release(source, clean, path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-world-map-header-release-v1":
        raise ValueError("Unknown map header label release")
    saved, plan = transform(source, clean)
    if sha(saved) != config["target_arm9_sha256"]:
        raise ValueError("Map header target differs")
    for file, digest in config["dependencies"].items():
        if sha(Path(file).read_bytes()) != digest:
            raise ValueError("Map header proof differs")
    plan["changed_records"] = ["DK4_WORLD_FLEETS_VILLAGES_HEADER", "DK4_WORLD_SEA_AREAS_HEADER", "DK4_WORLD_FLEET_VILLAGE_TYPE"]
    return saved, plan
