"""Scoped English sailing panels using the game's original 32x16 sprite banks."""

import json
import struct
import textwrap
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from scripts.probe_common_display_name_hook import branch_link

SOURCE = "9c03e253a6e91231a7e6d7ee112c07c632a3cfe16b2a33d2d349cc1e45857958"
PRODUCER = 0x01FFB4BC
UPLOAD_BYTES = 0x3800
CALLS = (0x6F178, 0x6F200, 0x6F3D8)
INITIAL_INFO_CALL = 0x70284
INITIAL_INFO_POINTER = 0x02147828
POINTERS = (0x02147778, 0x02147540, 0x02147674)
# Original native parent fragments, including both Declare War selection states.
DRAW_FRAGMENTS = {
    "info": (0x6E71C, 0x6E76C),
    "search": (0x6E778, 0x6E818),
    "war_target": (0x6E9BC, 0x6EA34),
    "war_no_target": (0x6EB50, 0x6EBC8),
}


def packed_pixel_offset(x, y):
    tile = x // 32 * 8 + x % 32 // 8 + y // 8 * 4
    return tile * 32 + y % 8 * 4 + x % 8 // 2


def encode_panels(source, manuscript):
    """The formatter owns wrapping; the manuscript contains logical prose only."""
    font = GameAsciiFont.from_arm9(source)
    panels = []
    if len(manuscript["records"]) != 3:
        raise ValueError("All three sailing instructions are required")
    for pointer, record in zip(POINTERS, manuscript["records"], strict=True):
        if int(record["source_address"], 16) != pointer:
            raise ValueError("Sailing source ownership changed")
        if not all(record["review"].get(gate) is True
                   for gate in ("source", "context", "localization", "naturalness")):
            raise ValueError("Source and English review required")
        prose = record["english"]
        if not prose.isascii() or "\n" in prose or prose != prose.strip():
            raise ValueError("Complete logical ASCII paragraph required")
        lines = textwrap.wrap(prose, width=40, break_long_words=False, break_on_hyphens=False)
        if " ".join(lines) != prose or not 1 <= len(lines) <= 5 or any(len(x) > 40 for x in lines):
            raise ValueError("Complete words must fit five native rows")
        heading = record["heading"]
        if not heading.isascii() or len(heading) * 6 > 192:
            raise ValueError("Complete heading exceeds its native banks")
        packed = bytearray((6 + 8 * len(lines)) * 256)
        glyphs = []
        for row, text in enumerate([heading] + lines):
            source_x = (192 - len(text) * 6) // 2 if row == 0 else 192 + (row - 1) * 256
            screen_x = 32 + source_x if row == 0 else 8
            screen_y = 2 if row == 0 else 32 + (row - 1) * 16
            for position, char in enumerate(text):
                mask = font.decode(char)
                ink = 0
                for y in range(11):
                    for x in range(6):
                        if mask.getpixel((x, y)):
                            virtual_x = source_x + position * 6 + x
                            at = packed_pixel_offset(virtual_x, y)
                            packed[at] |= 15 << (virtual_x % 2 * 4)
                            ink += 1
                origin = [screen_x + position * 6, screen_y]
                if origin[0] + 6 > 248 or origin[1] + 11 > 176:
                    raise ValueError("Complete glyph exceeds visible bounds")
                glyphs.append({"row": row, "character": char, "origin": origin,
                               "cell": [6, 11], "ink_pixels": ink})
        panels.append({"id": record["id"], "source_pointer": pointer, "heading": heading,
                       "english": prose, "lines": lines, "packed": bytes(packed),
                       "glyphs": glyphs})
    return panels


def helper(address, panels):
    words, labels, branches, loads, literals = [], {}, [], [], {}

    def emit(word):
        words.append(word)

    def mark(name):
        labels[name] = len(words)

    def branch(name, condition=14):
        branches.append((len(words), name, condition))
        emit(0)

    def load(register, name, value):
        loads.append((len(words), register, name))
        literals[name] = value
        emit(0)

    emit(0xE92D403E)  # r1-r5,lr: preserve caller inputs and all saved registers
    for index, row in enumerate(panels):
        for alias, pointer in enumerate([row["source_pointer"]] + row.get("source_aliases", [])):
            load(3, f"key{index}_{alias}", pointer)
            emit(0xE1500003)
            branch(f"panel{index}", 0)
    emit(0xE8BD403E)
    at = address + len(words) * 4
    emit(0xEA000000 | ((PRODUCER - at - 8) // 4 & 0xFFFFFF))
    for index, row in enumerate(panels):
        mark(f"panel{index}")
        load(3, f"pixels{index}", row["packed_pointer"])
        load(0, f"words{index}", len(row["packed"]) // 4)
        branch("selected")
    mark("selected")
    emit(0xE1A04002)
    load(5, "clear_words", UPLOAD_BYTES // 4)
    emit(0xE3A01000)
    mark("clear")
    emit(0xE4841004)
    emit(0xE2555001)
    branch("clear", 1)
    emit(0xE1A04002)
    emit(0xE1A05000)
    mark("copy")
    emit(0xE4931004)
    emit(0xE4841004)
    emit(0xE2555001)
    branch("copy", 1)
    emit(0xE3A00001)
    emit(0xE8BD803E)
    for name, value in literals.items():
        mark(name)
        emit(value)
    for index, name, condition in branches:
        words[index] = condition << 28 | 0x0A000000 | ((labels[name] - index - 2) & 0xFFFFFF)
    for index, register, name in loads:
        delta = (labels[name] - index - 2) * 4
        if not 0 <= delta < 4096:
            raise ValueError("Sailing helper literal exceeds ARM range")
        words[index] = 0xE59F0000 | register << 12 | delta
    return struct.pack(f"<{len(words)}I", *words)


def parent_changes(source):
    """Change only the existing per-mode sprite origin/count/tile MOV arguments."""
    fields = []

    def change(offset, before, after):
        if struct.unpack_from("<I", source, offset)[0] != before:
            raise ValueError(f"Original sailing parent argument changed at {offset:06X}")
        if before != after:
            fields.append((offset, before, after))

    # Six centered heading banks; each body row is eight banks, with 240 ink pixels.
    for origin in (0x6E71C, 0x6E778, 0x6E9BC, 0x6EB50):
        change(origin, 0xE3A00038, 0xE3A00020)
    for count in (0x6E724, 0x6E780):
        change(count, 0xE3A02005, 0xE3A02006)
    for count, old in ((0x6E738, 6), (0x6E74C, 7), (0x6E794, 6),
                       (0x6E7A8, 7), (0x6E7BC, 6), (0x6E7D0, 7),
                       (0x6E7E4, 7), (0x6E9EC, 6), (0x6EB80, 6)):
        change(count, 0xE3A02000 | old, 0xE3A02008)
    for count, old in ((0x6E760, 6), (0x6E7F8, 7), (0x6E80C, 2)):
        change(count, 0xE3A02000 | old, 0xE3A02000)
    for offset, before, after in ((0x6E750, 0x60, 0x70), (0x6E7AC, 0x60, 0x70),
                                  (0x6E7C0, 0xA8, 0xB0), (0x6E7D4, 0xD8, 0xF0),
                                  (0x6E7E8, 0x120, 0x130), (0x6E9F0, 0x78, 0x70),
                                  (0x6EA04, 0xA8, 0xB0), (0x6EA2C, 0x138, 0x130),
                                  (0x6EB84, 0x78, 0x70), (0x6EB98, 0xA8, 0xB0),
                                  (0x6EBC0, 0x138, 0x130)):
        # Verify the decoded immediate; native ARM permits multiple encodings.
        def immediate(value):
            return value if value < 256 else 0xF00 | value // 4
        original = struct.unpack_from("<I", source, offset)[0]
        rotation = (original >> 8 & 15) * 2
        byte = original & 255
        value = (byte >> rotation | byte << ((32 - rotation) % 32)) & 0xFFFFFFFF
        if original & 0xFFFFF000 != 0xE3A03000 or value != before:
            raise ValueError("Original native tile-index MOV differs")
        change(offset, original, 0xE3A03000 | immediate(after))
    return fields


def transform(source, canonical, manuscript, include_initial_info=False):
    if sha(source) != SOURCE:
        raise ValueError("Exact complete V211 ARM9 required")
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    if len(before) != 4 or len(before[3]) != 20624 or not cache_plan(source):
        raise ValueError("Exact inherited staging/cache ownership required")
    for record in manuscript["records"]:
        offset = int(record["source_address"], 16) - BASE
        capacity = record["source_allocation_bytes_including_NUL"]
        if source[offset:offset + capacity] != canonical[offset:offset + capacity]:
            raise ValueError("Original Japanese panel source lock differs")
    panels = encode_panels(source, manuscript)
    calls = CALLS
    if include_initial_info:
        offset = INITIAL_INFO_POINTER - BASE
        primary = POINTERS[0] - BASE
        if source[offset:offset + 141] != source[primary:primary + 141] or source[offset:offset + 141] != canonical[offset:offset + 141]:
            raise ValueError("Initial Info source is not the exact same original instruction")
        panels[0]["source_aliases"] = [INITIAL_INFO_POINTER]
        calls += (INITIAL_INFO_CALL,)
    packed = bytearray(before[3][:-48])
    for row in panels:
        packed.extend(bytes((-len(packed)) % 32))
        row["packed_pointer"] = POOL + len(packed)
        packed.extend(row["packed"])
    entry = POOL + len(packed)
    implementation = helper(entry, panels)
    packed.extend(implementation)
    changes = parent_changes(source)
    for offset, _, after in changes:
        struct.pack_into("<I", code.sections[0].data, offset, after)
    for field in calls:
        if struct.unpack_from("<I", source, field)[0] != branch_link(BASE + field, PRODUCER):
            raise ValueError("Original scoped sailing producer call changed")
        struct.pack_into("<I", code.sections[0].data, field, branch_link(BASE + field, entry))
    packed.extend(bytes((-len(packed)) % 32))
    size = len(packed) + 64
    if POOL + size >= STAGE or STAGE + size + 48 > 0x02400000:
        raise ValueError("Expanded staging and runtime pool overlap or escape RAM")
    cache_entry, copy_entry = STAGE + len(packed), STAGE + size
    packed.extend(wrapper(cache_entry, copy_entry, size, source))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack("<I", size)
    struct.pack_into("<I", code.sections[0].data, 0x8E4, branch_link(BASE + 0x8E4, cache_entry))
    struct.pack_into("<I", code.sections[0].data, 0xE45DC, POOL + size)
    saved = bytes(code.save())
    parsed = MainCodeFile(saved, BASE)
    restored = bytearray(parsed.sections[0].data)
    for offset in (*calls, *(r[0] for r in changes), 0x8E4, 0xE45DC):
        restored[offset:offset + 4] = before[0][offset:offset + 4]
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    if bytes(restored) != before[0] or any(bytes(parsed.sections[i].data) != before[i] for i in (1, 2)):
        raise ValueError("Sailing patch changes unrelated native code/sections")
    if bytes(parsed.sections[3].data[:len(before[3]) - 48]) != before[3][:-48]:
        raise ValueError("Inherited runtime text, helpers or cache wrapper changed")
    return saved, {"source_arm9_sha256": sha(source), "target_arm9_sha256": sha(saved),
                   "entry": entry, "helper_bytes": len(implementation),
                   "panels": [{**{k: v for k, v in row.items() if k != "packed"},
                               "packed_bytes": len(row["packed"]), "packed_sha256": sha(row["packed"])}
                              for row in panels],
                   "parent_changes": changes, "pool_payload_bytes": size,
                   "inherited_pool_bytes_preserved": len(before[3]) - 48,
                   "pool_span": [POOL, POOL + size], "staging_span": [STAGE, STAGE + size + 48],
                   "cache": cache_plan(saved), "copy_entry": copy_entry,
                   "initial_Info_source_alias_included": include_initial_info,
                   "scoped_producer_call_sites": [BASE + field for field in calls],
                   "source_Japanese_fields_and_overlay_unchanged": True,
                   "upload_bytes": UPLOAD_BYTES, "native_and_gameplay_verification_pending": True}


def apply_release(source, canonical, config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-sailing-panel-graphics-release-v1":
        raise ValueError("Unknown sailing graphics release format")
    manuscript_path = Path(config["manuscript"])
    if sha(manuscript_path.read_bytes()) != config["manuscript_sha256"]:
        raise ValueError("Reviewed sailing manuscript changed")
    manuscript = json.loads(manuscript_path.read_text(encoding="utf-8"))
    saved, plan = transform(source, canonical, manuscript, config.get("include_initial_info", False))
    if sha(canonical) != config["canonical_arm9_sha256"] or sha(saved) != config["target_arm9_sha256"]:
        raise ValueError("Sailing graphics input/output identity differs")
    proof_path = Path(config["native_proof"])
    if sha(proof_path.read_bytes()) != config["native_proof_sha256"]:
        raise ValueError("Sailing native evidence changed")
    proof = json.loads(proof_path.read_text(encoding="utf-8"))
    if (proof["plan"]["target_arm9_sha256"] != sha(saved)
            or len(proof["producer_cases"]) != (4 if config.get("include_initial_info") else 3)
            or len(proof["native_parent_layouts"]) != 4
            or not proof["unknown_source_pointer_fallback_matches_original_overlay"]
            or not all(row["first_last_glyphs_complete"] for row in proof["native_parent_layouts"])
            or not proof["startup"]["repaired_pool_matches_complete_payload"]
            or proof["startup"]["arm7_source_changed_bytes_after_arm9_autoload"]):
        raise ValueError("Complete sailing producer/parent/startup evidence required")
    for row in proof["native_parent_layouts"]:
        if sha(Path(row["preview"]).read_bytes()) != row["preview_sha256"]:
            raise ValueError("Reviewed sailing layout changed")
    if config.get("native_layout_visual_review_complete") is not True:
        raise ValueError("All native English layouts require visual review")
    plan["changed_records"] = [row["id"] for row in plan["panels"]]
    return saved, plan
