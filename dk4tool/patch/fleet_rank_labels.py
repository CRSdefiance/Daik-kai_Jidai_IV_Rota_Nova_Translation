"""Source-locked complete fleet Admiral labels in shared native UI consumers."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from scripts.probe_common_display_name_hook import branch_link

SOURCE = "7c15fd85152518b417fb80c8f90707fee4a39c39a81d49e2ff93f12c2c816c36"
ROOT = Path("work/analysis/fleet_rank_v260")
SPECS = [(0x37E84, 0x137104, "%s提督", "%s Admiral"),
         (0x8E56C, 0x14C2BC, "%s提督", "%s Admiral"),
         (0x14F480, 0x14F354, "地方提督", "Regional Admiral")]


def transform(source, clean):
    if sha(source) != SOURCE:
        raise ValueError("Exact complete V258 ARM9 required")
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    cache_plan(source)
    packed = bytearray(before[3][:-48])
    preserved = len(packed)
    rows, changes = [], []
    for field, offset, japanese, english in SPECS:
        raw = japanese.encode("cp932") + b"\0"
        if clean[offset:offset + len(raw)] != raw or source[offset:offset + len(raw)] != raw:
            raise ValueError("Original Japanese rank label differs")
        if struct.unpack_from("<I", source, field)[0] != BASE + offset:
            raise ValueError("Rank pointer differs")
        pointer = POOL + len(packed)
        packed.extend(english.encode("ascii") + b"\0")
        struct.pack_into("<I", code.sections[0].data, field, pointer)
        changes.append({"offset": field, "before": BASE + offset, "after": pointer})
        rows.append({"field": field, "source_pointer": BASE + offset, "source_Japanese": japanese,
                     "English": english, "target_pointer": pointer})
    packed.extend(bytes((-len(packed)) % 32))
    size = len(packed) + 64
    if POOL + size > STAGE or STAGE + size + 48 > 0x023F4000:
        raise ValueError("Rank strings escape owned storage")
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
                   "all_three_exact_Japanese_rank_consumers_relocated": True}


def apply_release(source, clean, path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-fleet-rank-label-release-v1":
        raise ValueError("Unknown rank label release")
    saved, plan = transform(source, clean)
    if sha(saved) != config["target_arm9_sha256"]:
        raise ValueError("Rank target differs")
    for file, digest in config["dependencies"].items():
        if sha(Path(file).read_bytes()) != digest:
            raise ValueError("Rank proof differs")
    plan["changed_records"] = ["DK4_FLEET_ADMIRAL_FMT_1", "DK4_FLEET_ADMIRAL_FMT_2", "DK4_REGIONAL_ADMIRAL_ROLE"]
    return saved, plan
