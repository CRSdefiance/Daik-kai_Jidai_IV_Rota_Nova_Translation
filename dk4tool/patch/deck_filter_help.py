"""Source-faithful navigator filter labels and word-wrapped Deck View guidance."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from scripts.probe_common_display_name_hook import branch_link

SOURCE = "94299dc2490b3921d78fcb739e49a3148ee39599f413cc5f4fced167839efa6d"
ROOT = Path("work/analysis/deck_filter_v262")
SPECS = [(0x14F460, 0x14F344, "未配置", "未配置", "Unassigned"),
         (0x14F490, 0x14F334, "全員", "全員", "All"),
         (0x15594, 0x131F48, "甲板画面では、航海士の担当を決められます。", "Use Deck View to assign navigator duties. ", "Use Deck View to assign navigator duties."),
         (0x15598, 0x131F74, "航海士を選んで部屋に配置すると、部屋の種類によって航海士の担当が決まります。", "Choose a navigator and a room. Each room assigns a different duty. ", "Choose a navigator and a room. The room type determines their duty."),
         (0x1559C, 0x131FC4, "各担当には、必要な能力があります。能力が不足していると、担当につけません。能力が高いほど、担当を配置した効果も高くなります。", "Each duty needs certain abilities. A navigator cannot take it without them. Higher ability makes the assignment more effective.", "Each duty requires certain abilities. Navigators cannot be assigned if their ability is too low. Higher ability makes them more effective.")]


def compiled(field, english, version=1):
    if field not in (0x15598, 0x1559C):
        return english
    import textwrap
    return "\n  ".join(textwrap.wrap(english, width=41 if version == 2 else 40, break_long_words=False, break_on_hyphens=False))


def transform(source, clean, version=1):
    if version not in (1, 2):
        raise ValueError("Unknown Deck help layout version")
    if sha(source) != SOURCE:
        raise ValueError("Exact complete V261 ARM9 required")
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    cache_plan(source)
    packed = bytearray(before[3][:-48])
    preserved = len(packed)
    rows, changes = [], []
    for field, offset, japanese, previous, english in SPECS:
        if version == 2 and field == 0x1559C:
            english = "Each duty needs certain abilities. Navigators must meet its requirements. Higher ability makes them more effective."
        raw = japanese.encode("cp932") + b"\0"
        if clean[offset:offset + len(raw)] != raw or source[offset:offset + len(previous.encode("cp932")) + 1] != previous.encode("cp932") + b"\0":
            raise ValueError("Original Japanese map header label differs")
        if struct.unpack_from("<I", source, field)[0] != BASE + offset:
            raise ValueError("Map header pointer differs")
        pointer = POOL + len(packed)
        encoded = compiled(field, english, version)
        packed.extend(encoded.encode("ascii") + b"\0")
        struct.pack_into("<I", code.sections[0].data, field, pointer)
        changes.append({"offset": field, "before": BASE + offset, "after": pointer})
        rows.append({"field": field, "source_pointer": BASE + offset, "source_Japanese": japanese,
                     "English": english, "compiled": encoded, "target_pointer": pointer})
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
                   "all_five_source_filter_and_help_labels_relocated": True}


def apply_release(source, clean, path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-deck-filter-help-release-v1":
        raise ValueError("Unknown map header label release")
    saved, plan = transform(source, clean, config.get("layout_version", 1))
    if sha(saved) != config["target_arm9_sha256"]:
        raise ValueError("Map header target differs")
    for file, digest in config["dependencies"].items():
        if sha(Path(file).read_bytes()) != digest:
            raise ValueError("Map header proof differs")
    plan["changed_records"] = ["DK4_NAV_FILTER_UNASSIGNED", "DK4_NAV_FILTER_ALL", "DK4_DECK_HELP_INTRO", "DK4_DECK_HELP_ROOM_TYPE", "DK4_DECK_HELP_ABILITY_REQUIREMENTS"]
    return saved, plan
