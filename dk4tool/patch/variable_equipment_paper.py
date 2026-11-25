"""Tile the established native paper across variable equipment-name hints."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.patch.sailing_no_target import Assembly
from dk4tool.patch.two_screen_layout import tail
from scripts.probe_common_display_name_hook import branch_link

SOURCE = "779b9230135163e483a7ed9c7f9fb056a76dad0fc739596463161c42bb80c821"
ROOT = Path("work/analysis/variable_equipment_v269")


def paint(address, state, old, parts, period):
    a = Assembly()
    a.load(12, "state", state)
    a.emit(0xE59CC000); a.emit(0xE150000C); a.branch("original", 1)
    a.emit(0xE590C028); a.emit(0xE5901020); a.emit(0xE04CC001)
    for width in (34, 40, 88):
        a.emit(0xE35C0000 | width); a.branch("original", 0)
    a.emit(0xE35C000A); a.branch("original", 3)
    a.emit(0xE35C00F4); a.branch("original", 8)
    a.emit(0xE92D4FF0)  # r4-r11/LR
    a.emit(0xE1A0400C)
    a.emit(0xE590C02C); a.emit(0xE5901024); a.emit(0xE04CC001)
    a.emit(0xE35C0010); a.branch("restore_original", 1)
    a.emit(0xE24DD014)  # nine saved words +20 locals preserve8-byte alignment
    a.emit(0xE5907020); a.emit(0xE5908024); a.emit(0xE5909018)
    a.emit(0xE2444002)  # right-edge origin relative to left

    def runs(name):
        ptr, count = parts[name]
        a.load(5, name + "_runs", ptr); a.load(6, name + "_count", count)
        a.mark(name + "_loop")
        a.emit(0xE5950000); a.emit(0xE150000A); a.branch(name + "_skip", 2)
        a.emit(0xE5952008); a.emit(0xE04A3000); a.emit(0xE1520003)
        a.emit(0x81A02003)  # clip final interior run to remaining width
        a.emit(0xE0800007); a.emit(0xE080000B)
        a.emit(0xE5951004); a.emit(0xE0811008); a.emit(0xE3A03001)
        a.emit(0xE88D000F); a.emit(0xE5951010)
        a.emit(0xE1A00009); a.emit(0xE1A0200D); a.emit(0xE28D3008)
        a.emit(branch_link(address + len(a.words) * 4, 0x01FFAC18))
        a.mark(name + "_skip")
        a.emit(0xE2855014); a.emit(0xE2566001); a.branch(name + "_loop", 1)

    a.emit(0xE3A0B000); a.emit(0xE3A0A002); runs("left")
    a.emit(0xE3A0B002)
    a.mark("tile")
    a.emit(0xE04BA004); a.emit(0xE26AA000)  # r10 = r4-r11
    a.emit(0xE35A0000 | period); a.emit(0x83A0A000 | period)
    runs("middle")
    a.emit(0xE28BB000 | period); a.emit(0xE15B0004); a.branch("tile", 3)
    a.emit(0xE1A0B004); a.emit(0xE3A0A002); runs("right")
    a.emit(0xE28DD014); a.emit(0xE8BD8FF0)
    a.mark("restore_original"); a.emit(0xE8BD4FF0)
    a.mark("original"); a.emit(tail(address + len(a.words) * 4, old))
    return a.finish()


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError("Exact complete V267 ARM9 required")
    plan = json.loads((ROOT / "paper_data_plan.json").read_text(encoding="utf-8"))
    prior = json.loads(Path("work/analysis/plaque_coverage_v252/runtime_plan.json").read_text(encoding="utf-8"))
    old, state = prior["dispatcher_entry"], prior["state_pointer"]
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    cache_plan(source)
    packed = bytearray(before[3][:-48]); preserved = len(packed)
    parts = {}
    for name in ("left", "middle", "right"):
        blob = (ROOT / f"{name}_runs.bin").read_bytes()
        if sha(blob) != plan["parts"][name]["sha256"]:
            raise ValueError("Native paper part differs")
        parts[name] = (POOL + len(packed), len(blob) // 20)
        packed.extend(blob)
    entry = POOL + len(packed)
    packed.extend(paint(entry, state, old, parts, plan["period"]))
    changes = []

    def replace(offset, expected, value):
        if struct.unpack_from("<I", source, offset)[0] != expected:
            raise ValueError("Variable paper source differs")
        struct.pack_into("<I", code.sections[0].data, offset, value)
        changes.append({"offset": offset, "before": expected, "after": value})

    replace(0x6BDC, branch_link(BASE + 0x6BDC, old), branch_link(BASE + 0x6BDC, entry))
    packed.extend(bytes((-len(packed)) % 32)); size = len(packed) + 64
    if POOL + size > STAGE or STAGE + size + 48 > 0x023F4000:
        raise ValueError("Variable paper escapes the owned arena")
    cache_entry, copy = STAGE + len(packed), STAGE + size
    packed.extend(wrapper(cache_entry, copy, size, source))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack("<I", size)
    replace(0x8E4, struct.unpack_from("<I", source, 0x8E4)[0], branch_link(BASE + 0x8E4, cache_entry))
    replace(0xE45DC, struct.unpack_from("<I", source, 0xE45DC)[0], POOL + size)
    saved = bytes(code.save()); parsed = MainCodeFile(saved, BASE)
    restored = bytearray(parsed.sections[0].data)
    for row in changes:
        o = row["offset"]; restored[o:o + 4] = before[0][o:o + 4]
    o = code.codeSettingsOffs; restored[o:o + 12] = before[0][o:o + 12]
    assert bytes(restored) == before[0]
    assert all(bytes(parsed.sections[n].data) == before[n] for n in (1, 2))
    assert bytes(parsed.sections[3].data[:preserved]) == before[3][:-48]
    return saved, {"source_arm9_sha256": SOURCE, "target_arm9_sha256": sha(saved),
                   "entry": entry, "old_dispatcher": old, "state_pointer": state,
                   "parts": parts, "period": plan["period"], "changes": changes,
                   "payload_bytes": size, "cache": cache_plan(saved),
                   "all_widths_10_through244_height16_supported": True,
                   "known34_40_88_hints_delegate_exactly_to_prior_helpers": True}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-variable-equipment-paper-release-v1":
        raise ValueError("Unknown variable paper release")
    for file, digest in config["dependencies"].items():
        if sha(Path(file).read_bytes()) != digest:
            raise ValueError("Variable paper dependency differs")
    saved, plan = transform(source)
    if sha(saved) != config["target_arm9_sha256"]:
        raise ValueError("Variable paper target differs")
    plan["changed_records"] = ["DK4_VARIABLE_EQUIPMENT_PAPER_V1"]
    return saved, plan
