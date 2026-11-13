"""Audit original/current Health and Mood selectors without changing game state."""

import hashlib
import json
import struct
from pathlib import Path

from unicorn import UC_ARCH_ARM, UC_MODE_ARM, Uc
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/plaque_states_v274")
ROM = Path("out/all_routes_combined_v272_candidate.nds")
BASE = 0x02000000
ACTOR = 0x023F0000
STACK = 0x023FE000
STOP = 0x023FFF00
GROUPS = [
    ("Mood", 0x1483B0, 6, 0x0207E070, 7),
    ("Health", 0x1483C8, 7, 0x0207E0BC, 6),
]


def string(data, address):
    return data[address - BASE:].split(b"\0", 1)[0].decode("cp932")


def verify_selectors(data):
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.mem_map(BASE, 0x400000)
    cpu.mem_write(BASE, data)
    cases = []
    for label, table, count, entry, field in GROUPS:
        fallback = struct.unpack_from("<I", data, 0x7E0A8 if label == "Mood" else 0x7E0F4)[0]
        for state in range(256):
            actor = bytearray(b"\xA5" * 64)
            actor[field] = state
            cpu.mem_write(ACTOR, bytes(actor))
            for register in range(UC_ARM_REG_R4, UC_ARM_REG_R4 + 9):
                cpu.reg_write(register, 0x55000000 + register)
            cpu.reg_write(UC_ARM_REG_R0, ACTOR)
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            cpu.reg_write(UC_ARM_REG_LR, STOP)
            cpu.emu_start(entry, STOP, count=100)
            expected = struct.unpack_from("<I", data, table + state * 4)[0] if state < count else fallback
            assert cpu.reg_read(UC_ARM_REG_R0) == expected, (label, state)
            assert cpu.reg_read(UC_ARM_REG_SP) == STACK
            assert cpu.mem_read(ACTOR, 64) == actor
            for register in range(UC_ARM_REG_R4, UC_ARM_REG_R4 + 9):
                assert cpu.reg_read(register) == 0x55000000 + register
            cases.append((label, state, expected))
    return cases


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    original = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    current = NdsImage.open(ROM).read_file("/__arm9__.bin")
    assert original[0x7E070:0x7E108] == current[0x7E070:0x7E108]
    assert original[0x1483B0:0x1483E4] == current[0x1483B0:0x1483E4]
    assert verify_selectors(original) == verify_selectors(current)
    font = GameAsciiFont.from_arm9(current)
    rows = []
    for label, table, count, entry, field in GROUPS:
        for state in range(count):
            pointer = struct.unpack_from("<I", original, table + 4 * state)[0]
            english = string(current, pointer)
            ink = sum(sum(bool(p) for p in font.decode(c).get_flattened_data()) for c in english)
            assert english.isascii() and ink > 0 and len(english) * 6 <= 48
            rows.append({"label": label, "state": state, "actor_byte_offset": field,
                         "native_selector": hex(entry), "string_pointer": hex(pointer),
                         "source": string(original, pointer), "english": english,
                         "font_ink_pixels": ink, "advance_width": len(english) * 6,
                         "actual_alternate_gameplay_display_verified": False})
    proof = {"format": "dk4-sailor-status-table-audit-v274", "candidate": str(ROM),
             "candidate_sha256": hashlib.sha256(ROM.read_bytes()).hexdigest(),
             "source_rom_sha256": hashlib.sha256(Path("work/clean.nds").read_bytes()).hexdigest(),
             "original_and_current_native_selector_cases": 1024,
             "all_256_byte_values_each_group_original_current_exact": True,
             "source_tables_and_selector_code_unchanged": True,
             "actor_memory_saved_registers_stack_and_fallback_exact": True,
             "rows": rows,
             "fixture_scope": "Isolated native selector calls; no live game RAM writes or savestate loads.",
             "native_font_metrics_are_not_full_alternate_scene_pixel_proof": True,
             "all18_plaque_hint_entries_remain_incomplete": True,
             "full_goal_complete": False}
    (ROOT / "status_table_proof.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"states": len(rows), "native_selector_cases": 1024, "candidate_sha256": proof["candidate_sha256"]}))


if __name__ == "__main__":
    main()
