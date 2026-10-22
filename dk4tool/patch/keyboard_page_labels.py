"""Translate only keyboard category paint labels; original page IDs stay intact."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

BASE, HOOK, DRAW = 0x02000000, 0xB0354, 0x020D5404
ENTRY, END = 0x01FFC780, 0x01FFC800
SOURCE = "869431ccc3de5436ef9b33f9f3807d28c298be57cc757c2ee4c3618fba82651e"
SOURCE_LABELS = (0x0215510C, 0x021550F4)
DISPLAY = ("EN", "#+")


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError("Keyboard labels require the exact registered V593 ARM9")
    clean_rom = NdsImage.open("work/clean.nds")
    clean = clean_rom.read_file("/__arm9__.bin")
    assert source[HOOK:HOOK + 4] == clean[HOOK:HOOK + 4] == struct.pack("<I", branch_link(BASE + HOOK, DRAW))
    assert source[0x155408:0x155408 + 49 * 4] == clean[0x155408:0x155408 + 49 * 4]
    assert tuple(struct.unpack_from("<2I", source, 0x155408 + 47 * 4)) == SOURCE_LABELS
    for pointer, text in zip(SOURCE_LABELS, ("英", "記"), strict=True):
        assert source[pointer - BASE:pointer - BASE + 3] == clean[pointer - BASE:pointer - BASE + 3] == text.encode("cp932") + b"\0"
    code = MainCodeFile(source, BASE)
    before = [bytes(section.data) for section in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000 and len(before[4]) == 4096
    offset = ENTRY - code.sections[4].ramAddress
    assert before[4][offset:END - code.sections[4].ramAddress] == bytes(END - ENTRY)
    # The old commodity helper originally ended at C77C. This aligned gap is
    # after that extent and before C800's later data. Do not use the Square
    # buffer at C1A0 or mutable resource slots at C680/C6A0.
    units = [(s.ramAddress, bytes(s.data)) for s in code.sections]
    units += [(o.ramAddress, bytes(o.data)) for o in loadOverlayTable(
        clean_rom.rom.arm9OverlayTable, lambda _, f: clean_rom.rom.files[f]).values()]
    assert not [(base + at, struct.unpack_from("<I", data, at)[0])
                for base, data in units for at in range(len(data) - 3)
                if ENTRY <= struct.unpack_from("<I", data, at)[0] < END]
    # Tail-call the original painter: preserve its return/stack contract and
    # change neither the provider's original strings nor the selection lookup.
    asm = f"""
ldr ip, english_source
cmp r1, ip
ldreq r1, english_display
ldr ip, symbols_source
cmp r1, ip
ldreq r1, symbols_display
b {DRAW}
english_source: .word {SOURCE_LABELS[0]}
symbols_source: .word {SOURCE_LABELS[1]}
english_display: .word {ENTRY + 44}
symbols_display: .word {ENTRY + 48}
"""
    body = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(asm, ENTRY)[0])
    assert len(body) == 44
    payload = body + b"EN\0\0#+\0\0"
    assert len(payload) == 52 and ENTRY + len(payload) <= END
    code.sections[4].data[offset:offset + len(payload)] = payload
    struct.pack_into("<I", code.sections[0].data, HOOK, branch_link(BASE + HOOK, ENTRY))
    target = bytes(code.save())
    parsed = MainCodeFile(target, BASE)
    assert all(len(s.data) == len(before[i]) and s.ramAddress == code.sections[i].ramAddress
               for i, s in enumerate(parsed.sections))
    restored_main = bytearray(parsed.sections[0].data)
    restored_main[HOOK:HOOK + 4] = before[0][HOOK:HOOK + 4]
    assert restored_main == before[0]
    restored_helper = bytearray(parsed.sections[4].data)
    restored_helper[offset:offset + len(payload)] = before[4][offset:offset + len(payload)]
    assert restored_helper == before[4]
    assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2, 3))
    return target, {"source_arm9_sha256": SOURCE, "target_arm9_sha256": sha(target),
                    "changed_records": ["KEYBOARD_ENGLISH_PAGE_DISPLAY", "KEYBOARD_SYMBOL_PAGE_DISPLAY"],
                    "paint_call_offset": HOOK, "original_painter": DRAW, "display_wrapper": ENTRY,
                    "owned_zero_gap": [ENTRY, END], "new_payload_bytes": len(payload),
                    "source_label_pointers": list(SOURCE_LABELS), "display_labels": list(DISPLAY),
                    "original_category_table_identifiers_provider_and_all_character_data_unchanged": True,
                    "all_other_name_and_dialogue_render_calls_unchanged": True,
                    "no_font_change_section_growth_pool_growth_heap_startup_or_cache_change": True,
                    "status": "experimental", "full_goal_complete": False}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    assert config["format"] == "dk4-keyboard-page-labels-v1"
    assert sha(source) == config["source_arm9_sha256"]
    result, report = transform(source)
    assert sha(result) == config["target_arm9_sha256"]
    return result, report
