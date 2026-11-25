"""Scoped Sailor Info bar geometry and equipment-tooltip paper styling."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.patch.sailing_no_target import Assembly
from scripts.probe_common_display_name_hook import branch_link

SOURCE = "329f18127f40788d260aca323939d05c66a76a8bca466f7a61fcd130d6d995f3"
CANONICAL = "9a79c25d4a7cf03678a8b5444c3f685a9f675be879109817adb01643141768f5"


def tail(at, target):
    return 0xEA000000 | (((target - at - 8) // 4) & 0xFFFFFF)


def width_helper():
    return struct.pack("<7I", 0xE3500000, 0xB3A00000, 0xE3500064, 0xC3A00064,
                       0xE1A000A0, 0xE5820008, 0xE12FFF1E)


def reset_helper(address, state):
    a = Assembly()
    a.load(12, "state", state)
    a.emit(0xE3A01000)
    a.emit(0xE58C1000)
    a.emit(tail(address + len(a.words)*4, BASE + 0xD393C))
    return a.finish()


def equipment_helper(address, state):
    a = Assembly()
    a.emit(0xE92D41F0)  # r4-r8/LR; copy original four stacked arguments.
    a.emit(0xE24DD010)
    a.emit(0xE1A08000)
    a.emit(0xE28DC028)
    a.emit(0xE89C00F0)
    a.emit(0xE88D00F0)
    a.emit(branch_link(address + len(a.words)*4, BASE + 0x7430))
    a.load(12, "state", state)
    a.emit(0xE58C8000)
    a.emit(0xE28DD010)
    a.emit(0xE8BD81F0)
    return a.finish()


def fill_helper(address, state):
    a = Assembly()
    a.load(12, "state", state)
    a.emit(0xE59CC000)
    a.emit(0xE150000C)
    a.branch("original", 1)
    a.emit(0xE3A020CD)  # Tan paper R=205, G=190, B=141.
    a.emit(0xE3A030BE)
    a.emit(0xE3A0C08D)
    a.emit(0xE58DC000)
    a.mark("original")
    a.emit(tail(address + len(a.words)*4, BASE + 0xD13F8))
    return a.finish()


def transform(source, canonical):
    if sha(source) != SOURCE or sha(canonical) != CANONICAL:
        raise ValueError("Exact complete V245 and canonical ARM9 required")
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    if len(before) != 4 or not cache_plan(source):
        raise ValueError("Complete inherited staging/cache required")
    packed = bytearray(before[3][:-48])
    preserved = len(packed)
    state = POOL + len(packed)
    packed.extend(bytes(4))
    entries = {}
    for name, factory in (("bar_width", lambda address: width_helper()),
                          ("tooltip_reset", lambda address: reset_helper(address, state)),
                          ("equipment_tooltip", lambda address: equipment_helper(address, state)),
                          ("tooltip_fill", lambda address: fill_helper(address, state))):
        packed.extend(bytes((-len(packed)) % 4))
        entry = POOL + len(packed)
        data = factory(entry)
        entries[name] = {"entry": entry, "bytes": len(data), "sha256": sha(data)}
        packed.extend(data)
    changes = []

    def replace(offset, expected, value):
        if struct.unpack_from("<I", source, offset)[0] != expected:
            raise ValueError(f"Native layout source changed at {offset:06X}")
        if offset not in (0x8E4, 0xE45DC) and canonical[offset:offset+4] != source[offset:offset+4]:
            raise ValueError(f"Canonical native layout source differs at {offset:06X}")
        struct.pack_into("<I", code.sections[0].data, offset, value)
        changes.append({"offset": offset, "before": expected, "after": value})

    replace(0x8039C, 0xE5820008, branch_link(BASE + 0x8039C, entries["bar_width"]["entry"]))
    replace(0x80898, branch_link(BASE + 0x80898, BASE + 0xD5404), 0xE2866002)
    replace(0x81780, branch_link(BASE + 0x81780, BASE + 0x7430),
            branch_link(BASE + 0x81780, entries["equipment_tooltip"]["entry"]))
    replace(0x770C, branch_link(BASE + 0x770C, BASE + 0xD393C),
            branch_link(BASE + 0x770C, entries["tooltip_reset"]["entry"]))
    replace(0x6BDC, branch_link(BASE + 0x6BDC, BASE + 0xD13F8),
            branch_link(BASE + 0x6BDC, entries["tooltip_fill"]["entry"]))
    for n in range(6):
        replace(0x11970C + n*16, 151, 174)
        replace(0x119714 + n*16, 100, 50)
    packed.extend(bytes((-len(packed)) % 32))
    size = len(packed) + 64
    if POOL + size > STAGE or STAGE + size + 48 > 0x023F4000:
        raise ValueError("Layout helpers exceed owned main-pool/staging bounds")
    cache_entry, copy_entry = STAGE + len(packed), STAGE + size
    packed.extend(wrapper(cache_entry, copy_entry, size, source))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack("<I", size)
    replace(0x8E4, struct.unpack_from("<I", source, 0x8E4)[0], branch_link(BASE + 0x8E4, cache_entry))
    replace(0xE45DC, struct.unpack_from("<I", source, 0xE45DC)[0], POOL + size)
    saved = bytes(code.save())
    loaded = MainCodeFile(saved, BASE)
    restored = bytearray(loaded.sections[0].data)
    for row in changes:
        restored[row["offset"]:row["offset"]+4] = before[0][row["offset"]:row["offset"]+4]
    at = code.codeSettingsOffs
    restored[at:at+12] = before[0][at:at+12]
    if (bytes(restored) != before[0] or any(bytes(loaded.sections[n].data) != before[n] for n in (1,2))
            or bytes(loaded.sections[3].data[:preserved]) != before[3][:-48]):
        raise ValueError("Layout changes unrelated code, sections or inherited pool data")
    return saved, {"source_arm9_sha256": SOURCE, "target_arm9_sha256": sha(saved),
                   "state_pointer": state, "helpers": entries, "code_changes": changes,
                   "inherited_pool_bytes_preserved": preserved, "pool_payload_bytes": size,
                   "cache": cache_plan(saved), "pool_span": [POOL, POOL + size],
                   "staging_span": [STAGE, STAGE + size + 48],
                   "original_stat_values_and_equipment_eligibility_unchanged": True,
                   "generic_tooltip_fill_preserved_unless_manager_matches_equipment_state": True}


def apply_release(source, canonical, config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-two-screen-layout-release-v1":
        raise ValueError("Unknown two-screen layout release")
    for path, digest in config["dependencies"].items():
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError("Layout dependency hash differs: " + path)
    saved, plan = transform(source, canonical)
    if sha(saved) != config["target_arm9_sha256"]:
        raise ValueError("Two-screen layout target hash differs")
    plan["changed_records"] = ["DK4_SAILOR_STATS_PLAQUES_AND_BAR_LAYOUT_V1", "DK4_SAILOR_EQUIPMENT_TOOLTIP_PAPER_V1"]
    return saved, plan
