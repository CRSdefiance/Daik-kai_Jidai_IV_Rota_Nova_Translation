"""Keep the newline guard adjustment from rewinding a visible glyph cell."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.patch.sailing_no_target import Assembly
from dk4tool.patch.two_screen_layout import tail
from scripts.probe_common_display_name_hook import branch_link

SOURCE = "c0a46d2f726008eb4619ef5220fc96ba1ba8e8f891e2335d81ecb96a19171b30"
ROOT = Path("work/analysis/modal_cursor_v271")
OFFSET, END = 0xD5544, 0xD556C


def transform(source, version=1):
    if sha(source) != SOURCE:
        raise ValueError("Exact complete V270 ARM9 required")
    before = struct.pack("<10I", 0xE5592002, 0xE352000A, 0x05592001, 0x03520020,
                         0x059A3024, 0x03530006, 0x058A5024, 0xEAFFFFE2, 0xE1A00000, 0xE1A00000)
    if source[OFFSET:END] != before:
        raise ValueError("Existing newline cursor adjustment differs")
    if version == 2:
        return buffered_transform(source)
    if version != 1:
        raise ValueError("Unknown cursor predicate version")
    branch = 0xEA000000 | (((0xD54F0 - (0xD5568 + 8)) // 4) & 0xFFFFFF)
    after = struct.pack("<10I", 0xE5592002, 0xE352000A, 0x05592001, 0x03520020,
                        0x05D92000, 0x03520020, 0x059A3024, 0x03530006, 0x058A5024, branch)
    target = source[:OFFSET] + after + source[END:]
    return target, {"source_arm9_sha256": SOURCE, "target_arm9_sha256": sha(target),
                    "offset": OFFSET, "before_hex": before.hex(), "after_hex": after.hex(),
                    "cursor_adjustment_requires_current_guard_space": True,
                    "no_stored_text_controls_macros_allocation_or_font_changed": True,
                    "changed_records": ["DK4_MODAL_CURSOR_GUARD_VISIBLE_GLYPHS_V1"]}


def buffered_helper(entry):
    a = Assembly()
    a.emit(0xE5592002); a.emit(0xE352000A); a.branch("loop", 1)
    a.emit(0xE5592001); a.emit(0xE3520020); a.branch("loop", 1)
    a.emit(0xE59A3024); a.emit(0xE3530006); a.branch("loop", 1)
    a.emit(0xE5D92000); a.emit(0xE3520020); a.branch("rewind", 0)
    a.emit(0xE59A2044); a.emit(0xE3520000); a.branch("loop", 1)
    a.mark("rewind"); a.emit(0xE58A5024)
    a.mark("loop"); a.emit(tail(entry + len(a.words) * 4, BASE + 0xD54F0))
    return a.finish()


def buffered_transform(source):
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    cache_plan(source)
    packed = bytearray(before[3][:-48]); preserved = len(packed)
    entry = POOL + len(packed)
    packed.extend(buffered_helper(entry))
    changes = []
    def replace(offset, value):
        old = struct.unpack_from("<I", source, offset)[0]
        struct.pack_into("<I", code.sections[0].data, offset, value)
        changes.append({"offset": offset, "before": old, "after": value})
    replace(OFFSET, tail(BASE + OFFSET, entry))
    packed.extend(bytes((-len(packed)) % 32)); size = len(packed) + 64
    if POOL + size > STAGE or STAGE + size + 48 > 0x023F4000:
        raise ValueError("Cursor helper escapes the owned arena")
    cache_entry, copy = STAGE + len(packed), STAGE + size
    packed.extend(wrapper(cache_entry, copy, size, source))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack("<I", size)
    replace(0x8E4, branch_link(BASE + 0x8E4, cache_entry))
    replace(0xE45DC, POOL + size)
    target = bytes(code.save()); parsed = MainCodeFile(target, BASE)
    restored = bytearray(parsed.sections[0].data)
    for row in changes:
        o = row["offset"]; restored[o:o + 4] = before[0][o:o + 4]
    o = code.codeSettingsOffs; restored[o:o + 12] = before[0][o:o + 12]
    assert bytes(restored) == before[0] and all(bytes(parsed.sections[n].data) == before[n] for n in (1, 2))
    assert bytes(parsed.sections[3].data[:preserved]) == before[3][:-48]
    return target, {"source_arm9_sha256": SOURCE, "target_arm9_sha256": sha(target), "entry": entry,
                    "version": 2, "changes": changes, "payload_bytes": size, "cache": cache_plan(target),
                    "rewind_allowed_for_blank_or_empty_pending_buffer_only": True,
                    "no_text_controls_macros_record_allocations_or_font_changed": True,
                    "changed_records": ["DK4_MODAL_BUFFERED_CURSOR_GUARD_V2"]}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-modal-cursor-guard-release-v1":
        raise ValueError("Unknown modal cursor repair")
    target, plan = transform(source, config.get("predicate_version", 1))
    if sha(target) != config["target_arm9_sha256"]:
        raise ValueError("Modal cursor target differs")
    for file, digest in config["dependencies"].items():
        if sha(Path(file).read_bytes()) != digest:
            raise ValueError("Modal cursor evidence differs")
    return target, plan
