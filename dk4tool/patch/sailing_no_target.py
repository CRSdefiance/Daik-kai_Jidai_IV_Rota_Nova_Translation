"""Complete no-attack-target notice in both native sailing presentations."""

import json
import struct
import textwrap
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.patch.sailing_panel_graphics import PRODUCER, packed_pixel_offset
from scripts.probe_common_display_name_hook import branch_link

SOURCE = "51ff802b41754ecfde5dac662cd66c5371915cd6060d8da091bd3d4ec28cd290"
GRAPHIC_POINTER = 0x02147F34
TEXT_POINTER = 0x02147808
UPLOAD_BYTES = 0x800
MAIN_OBJ_OFFSET = 0x5600
MAIN_OBJ_FIRST_TILE = MAIN_OBJ_OFFSET // 32
FIRST_DRAW = 0x6EAA4
OTHER_DRAWS = (0x6EAC4, 0x6EAE4, 0x6EB0C, 0x6EB2C, 0x6EB4C)


def mov_immediate(register, value):
    for rotation in range(16):
        n = rotation * 2
        rotated = ((value << n) | (value >> ((32 - n) % 32))) & 0xFFFFFFFF
        if rotated < 256:
            return 0xE3A00000 | register << 12 | rotation << 8 | rotated
    raise ValueError("ARM immediate is not representable")


class Assembly:
    def __init__(self):
        self.words, self.labels, self.branches, self.loads, self.literals = [], {}, [], [], {}

    def emit(self, word):
        self.words.append(word)

    def mark(self, name):
        self.labels[name] = len(self.words)

    def branch(self, name, condition=14):
        self.branches.append((len(self.words), name, condition))
        self.emit(0)

    def load(self, register, name, value):
        self.loads.append((len(self.words), register, name))
        self.literals[name] = value
        self.emit(0)

    def finish(self):
        for name, value in self.literals.items():
            self.mark(name)
            self.emit(value)
        for at, name, condition in self.branches:
            self.words[at] = condition << 28 | 0x0A000000 | ((self.labels[name] - at - 2) & 0xFFFFFF)
        for at, register, name in self.loads:
            delta = (self.labels[name] - at - 2) * 4
            if not 0 <= delta < 4096:
                raise ValueError("ARM literal exceeds its bounded helper")
            self.words[at] = 0xE59F0000 | register << 12 | delta
        return struct.pack(f"<{len(self.words)}I", *self.words)


def prepare(source, manuscript):
    records = manuscript["records"]
    if len(records) != 1:
        raise ValueError("Exactly one reviewed no-target notice required")
    record = records[0]
    if not all(record["review"].get(k) is True for k in ("source", "context", "localization", "naturalness")):
        raise ValueError("Complete source and English review required")
    english = record["english"]
    if not english.isascii() or "\n" in english or english != english.strip():
        raise ValueError("Logical English paragraph required")
    lines = textwrap.wrap(english, width=18, break_long_words=False, break_on_hyphens=False)
    if len(lines) != 2 or " ".join(lines) != english or any(len(line) > 18 for line in lines):
        raise ValueError("Whole sentence must fit two word-preserving rows")
    font = GameAsciiFont.from_arm9(source)
    packed = bytearray(UPLOAD_BYTES)
    glyphs = []
    for row, line in enumerate(lines):
        start = (128 - len(line) * 6) // 2
        for n, char in enumerate(line):
            mask = font.decode(char)
            for y in range(11):
                for x in range(6):
                    if mask.getpixel((x, y)):
                        virtual_x = row * 128 + start + n * 6 + x
                        packed[packed_pixel_offset(virtual_x, y)] |= 1 << (virtual_x % 2 * 4)
            glyphs.append({"character": char, "row": row, "origin": [80 + start + n * 6, 272 + row * 16],
                           "complete_cell": [6, 11]})
    # This is generated presentation syntax, never editable prose. A single guard
    # makes the native two-ASCII renderer overwrite the first continuation letter.
    compiled = lines[0] + "\n  " + lines[1]
    return {"id": record["id"], "english": english, "lines": lines, "compiled": compiled,
            "packed": bytes(packed), "glyphs": glyphs, "ordinary_view_dimensions": [120, 24],
            "main_sprite_dimensions": [128, 32], "main_sprite_origin": [80, 272]}


def producer(address, pixels):
    a = Assembly()
    a.emit(0xE92D403E)
    a.load(3, "key", GRAPHIC_POINTER)
    a.emit(0xE1500003)
    a.branch("selected", 0)
    a.emit(0xE8BD403E)
    at = address + len(a.words) * 4
    a.emit(0xEA000000 | ((PRODUCER - at - 8) // 4 & 0xFFFFFF))
    a.mark("selected")
    a.load(3, "pixels", pixels)
    a.emit(0xE1A04002)
    a.emit(mov_immediate(5, UPLOAD_BYTES // 4))
    a.mark("copy")
    a.emit(0xE4931004)
    a.emit(0xE4841004)
    a.emit(0xE2555001)
    a.branch("copy", 1)
    a.emit(0xE3A00001)
    a.emit(0xE8BD803E)
    return a.finish()


def draw(address):
    a = Assembly()
    a.emit(0xE92D407F)  # preserve original r0-r6/LR, plus private coordinate pair
    a.emit(0xE24DD008)
    for row in range(2):
        for column in range(4):
            a.emit(mov_immediate(4, 80 + column * 32))
            a.emit(0xE58D4000)
            a.emit(mov_immediate(4, 80 + row * 16))
            a.emit(0xE58D4004)
            a.emit(0xE3A00000)
            a.emit(0xE1A0100D)
            a.load(2, "descriptor", 0x80004000)
            a.emit(mov_immediate(3, MAIN_OBJ_FIRST_TILE + (row * 4 + column) * 8))
            a.emit(branch_link(address + len(a.words) * 4, BASE + 0x89358))
    a.emit(0xE28DD008)
    a.emit(0xE8BD807F)
    return a.finish()


def transform(source, canonical, manuscript):
    if sha(source) != SOURCE:
        raise ValueError("Exact complete V217 ARM9 required")
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    if len(before) != 4 or len(before[3]) != 50096 or not cache_plan(source):
        raise ValueError("Inherited V217 staging/cache contract changed")
    ordinary = "戦闘を仕掛ける相手がいません".encode("cp932") + b"\0"
    graphic = "戦闘を仕掛ける　相手がいません　".encode("cp932") + b"\0"
    for pointer, raw in ((TEXT_POINTER, ordinary), (GRAPHIC_POINTER, graphic)):
        offset = pointer - BASE
        if source[offset:offset + len(raw)] != raw or canonical[offset:offset + len(raw)] != raw:
            raise ValueError("Original Japanese notice source lock differs")
    panel = prepare(source, manuscript)
    packed = bytearray(before[3][:-48])
    packed.extend(bytes((-len(packed)) % 32))
    pixels = POOL + len(packed)
    packed.extend(panel["packed"])
    compiled = POOL + len(packed)
    packed.extend(panel["compiled"].encode("ascii") + b"\0")
    packed.extend(bytes((-len(packed)) % 4))
    producer_entry = POOL + len(packed)
    packed.extend(producer(producer_entry, pixels))
    draw_entry = POOL + len(packed)
    packed.extend(draw(draw_entry))
    changes = []

    def replace(offset, expected, target):
        if struct.unpack_from("<I", source, offset)[0] != expected:
            raise ValueError(f"Original notice consumer changed at {offset:06X}")
        struct.pack_into("<I", code.sections[0].data, offset, target)
        changes.append({"offset": offset, "before": expected, "after": target})

    replace(0x7007C, TEXT_POINTER, compiled)
    replace(0x70004, mov_immediate(0, 84), mov_immediate(0, 120))
    replace(0x7B928, branch_link(BASE + 0x7B928, PRODUCER), branch_link(BASE + 0x7B928, producer_entry))
    replace(0x7B930, mov_immediate(1, 0x600), mov_immediate(1, UPLOAD_BYTES))
    replace(0x7B93C, mov_immediate(1, 0x4000), mov_immediate(1, MAIN_OBJ_OFFSET))
    replace(0x7B940, mov_immediate(2, 0x600), mov_immediate(2, UPLOAD_BYTES))
    replace(FIRST_DRAW, branch_link(BASE + FIRST_DRAW, BASE + 0x89358), branch_link(BASE + FIRST_DRAW, draw_entry))
    for field in OTHER_DRAWS:
        replace(field, branch_link(BASE + field, BASE + 0x89358), 0xE1A00000)
    packed.extend(bytes((-len(packed)) % 32))
    size = len(packed) + 64
    if POOL + size >= STAGE or STAGE + size + 48 > 0x02400000:
        raise ValueError("Notice pool overlaps staging or escapes RAM")
    cache_entry, copy_entry = STAGE + len(packed), STAGE + size
    packed.extend(wrapper(cache_entry, copy_entry, size, source))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack("<I", size)
    replace(0x8E4, struct.unpack_from("<I", source, 0x8E4)[0], branch_link(BASE + 0x8E4, cache_entry))
    replace(0xE45DC, struct.unpack_from("<I", source, 0xE45DC)[0], POOL + size)
    saved = bytes(code.save())
    parsed = MainCodeFile(saved, BASE)
    restored = bytearray(parsed.sections[0].data)
    for row in changes:
        at = row["offset"]
        restored[at:at + 4] = before[0][at:at + 4]
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    if bytes(restored) != before[0] or any(bytes(parsed.sections[i].data) != before[i] for i in (1, 2)):
        raise ValueError("Notice changes unrelated native code or sections")
    if bytes(parsed.sections[3].data[:len(before[3]) - 48]) != before[3][:-48]:
        raise ValueError("Prior English graphics or helpers changed")
    return saved, {"source_arm9_sha256": sha(source), "target_arm9_sha256": sha(saved),
                   "panel": {**{k: v for k, v in panel.items() if k != "packed"},
                             "packed_sha256": sha(panel["packed"]), "packed_bytes": len(panel["packed"])},
                   "producer_entry": producer_entry, "draw_entry": draw_entry, "compiled_pointer": compiled,
                   "pixel_pointer": pixels, "code_changes": changes, "cache": cache_plan(saved),
                   "pool_span": [POOL, POOL + size], "staging_span": [STAGE, STAGE + size + 48],
                   "copy_entry": copy_entry, "inherited_pool_bytes_preserved": len(before[3]) - 48,
                   "original_font_palettes_and_Japanese_fields_preserved": True,
                   "Main_OBJ_upload_span": [MAIN_OBJ_OFFSET, MAIN_OBJ_OFFSET + UPLOAD_BYTES],
                   "native_and_cold_boot_verification_pending": True}


def apply_release(source, canonical, config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-sailing-no-target-release-v1":
        raise ValueError("Unknown no-target release format")
    def locked(key):
        path = Path(config[key])
        if sha(path.read_bytes()) != config[key + "_sha256"]:
            raise ValueError("Notice review/evidence changed: " + key)
        return json.loads(path.read_text(encoding="utf-8"))
    saved, plan = transform(source, canonical, locked("manuscript"))
    proof = locked("native_proof")
    if (sha(canonical) != config["canonical_arm9_sha256"] or sha(saved) != config["target_arm9_sha256"]
            or proof["target_arm9_sha256"] != sha(saved) or not proof["native_producer_and_eight_sprite_requests_exact"]
            or not proof["original_notice_upload_does_not_overlap_other_startup_regions"]
            or not proof["ordinary_font_first_last_glyphs_and_bounds_exact"]
            or not proof["startup"]["repaired_pool_matches_complete_payload"]
            or config.get("visual_review_complete") is not True):
        raise ValueError("Complete notice native, bounds, ownership and visual review required")
    plan["changed_records"] = [plan["panel"]["id"], "NO_TARGET_ORDINARY_BITMAP_AND_PACKED_SPRITES"]
    return saved, plan
