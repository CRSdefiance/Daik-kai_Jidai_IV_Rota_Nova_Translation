"""Align generated initial guards with protected continuation indentation."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.patch.sailing_no_target import Assembly
from dk4tool.patch.two_screen_layout import tail
from scripts.probe_common_display_name_hook import branch_link

SOURCE = "1df6b503368237b5b508d91fe2177a7c0c23419d86a1e0e44a561644e59b2944"
ROOT = Path("work/analysis/common_alignment_v258")


def paint(address, spaces):
    a = Assembly()
    a.emit(0xE92D4070)  # r4-r6/LR, aligned stack
    a.emit(0xE1A04000)
    a.emit(0xE1A05001)
    a.emit(0xE3550000)
    a.branch("plain", 0)
    a.emit(0xE594C00C)
    a.emit(0xE5946004)
    a.emit(0xE04CC006)
    a.emit(0xE35C000C)
    a.branch("plain", 11)
    a.emit(0xE594C010)
    a.emit(0xE5946008)
    a.emit(0xE04CC006)
    a.emit(0xE35C0010)
    a.branch("plain", 11)
    for offset in (0, 1):
        a.emit(0xE5D5C000 | offset)
        a.emit(0xE35C0020)
        a.branch("plain", 1)
    a.emit(0xE5D5C002)
    a.emit(0xE35C0021)
    a.branch("plain", 3)
    a.emit(0xE35C007F)
    a.branch("plain", 0)
    a.emit(0xE35C0080)
    a.branch("plain", 0)
    a.emit(0xE35C00FD)
    a.branch("plain", 2)
    a.emit(0xE594601C)
    a.emit(0xE3560000)
    a.branch("plain", 1)
    # Keep both source guards, paint their empty glyph cells at half advance.
    # No LF block, source byte, clip bound or visible-letter spacing is changed.
    a.emit(0xE3E0C002)  # -3 tracking for two empty six-pixel spaces
    a.emit(0xE584C01C)
    a.load(1, "spaces", spaces)
    a.emit(branch_link(address + len(a.words) * 4, BASE + 0xD5404))
    a.emit(0xE584601C)
    a.emit(0xE1A00004)
    a.emit(0xE2851002)
    a.emit(branch_link(address + len(a.words) * 4, BASE + 0xD5404))
    a.emit(0xE8BD8070)
    a.mark("plain")
    a.emit(0xE1A00004)
    a.emit(0xE1A01005)
    a.emit(0xE8BD4070)
    a.emit(tail(address + len(a.words) * 4, BASE + 0xD5404))
    return a.finish()


def transform(source, call_site=0x54924):
    if sha(source) != SOURCE:
        raise ValueError("Exact complete V255 ARM9 required")
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    cache_plan(source)
    packed = bytearray(before[3][:-48])
    preserved = len(packed)
    spaces = POOL + len(packed)
    packed.extend(b"  \0\0")
    helper = POOL + len(packed)
    packed.extend(paint(helper, spaces))
    changes = []

    def replace(offset, expected, value):
        if struct.unpack_from("<I", source, offset)[0] != expected:
            raise ValueError("Source alignment call differs at " + hex(offset))
        struct.pack_into("<I", code.sections[0].data, offset, value)
        changes.append({"offset": offset, "before": expected, "after": value})

    if call_site not in (0x7F5C, 0x54924):
        raise ValueError("Unknown source-locked alignment caller")
    replace(call_site, branch_link(BASE + call_site, BASE + 0xD5404), branch_link(BASE + call_site, helper))
    packed.extend(bytes((-len(packed)) % 32))
    size = len(packed) + 64
    if POOL + size > STAGE or STAGE + size + 48 > 0x023F4000:
        raise ValueError("Alignment helper escapes owned storage")
    entry, copy = STAGE + len(packed), STAGE + size
    packed.extend(wrapper(entry, copy, size, source))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack("<I", size)
    replace(0x8E4, struct.unpack_from("<I", source, 0x8E4)[0], branch_link(BASE + 0x8E4, entry))
    replace(0xE45DC, struct.unpack_from("<I", source, 0xE45DC)[0], POOL + size)
    saved = bytes(code.save())
    loaded = MainCodeFile(saved, BASE)
    restored = bytearray(loaded.sections[0].data)
    for row in changes:
        o = row["offset"]
        restored[o:o + 4] = before[0][o:o + 4]
    o = code.codeSettingsOffs
    restored[o:o + 12] = before[0][o:o + 12]
    if bytes(restored) != before[0] or any(bytes(loaded.sections[n].data) != before[n] for n in (1, 2)):
        raise ValueError("Unrelated code/data changed")
    if bytes(loaded.sections[3].data[:preserved]) != before[3][:-48]:
        raise ValueError("Inherited payload differs")
    return saved, {"source_arm9_sha256": SOURCE, "target_arm9_sha256": sha(saved),
                   "helper": helper, "call_site": call_site, "changes": changes, "cache": cache_plan(saved),
                   "payload_bytes": size, "inherited_pool_bytes_preserved": preserved,
                   "only_basic_textbox_initial_two_space_generated_padding_condensed": True,
                   "source_guards_LF_handling_and_visible_glyph_advance_unchanged": True}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-common-dialogue-alignment-release-v1":
        raise ValueError("Unknown alignment release")
    for file, digest in config["dependencies"].items():
        if sha(Path(file).read_bytes()) != digest:
            raise ValueError("Alignment proof differs")
    saved, plan = transform(source, config.get("call_site", 0x7F5C))
    if sha(saved) != config["target_arm9_sha256"]:
        raise ValueError("Alignment target differs")
    plan["changed_records"] = ["DK4_BASIC_DIALOGUE_CONSISTENT_LEFT_MARGIN_V1"]
    return saved, plan
