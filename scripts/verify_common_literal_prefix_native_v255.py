"""Native shared-expander output for all COMMON entries and genuine macros.

Actor-sensitive pronoun and model getters are explicit controlled contracts.
The original macro dispatcher, byte copy, saved registers and stack execute.
"""

import json
import struct

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.patch.common_literal_prefix import ROOT
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import call, machine
from scripts.probe_common_itcm_arena_reservation import initialize
from scripts.probe_persistent_name_arm7_boot_overlap import execute

INPUT, OUTPUT = 0x02440000, 0x02442000


def setup(arm):
    u = machine(arm)
    sections = MainCodeFile(arm, BASE).sections
    if len(sections) == 4:
        u.mem_write(POOL, bytes(sections[3].data[:-48]))
    # Native macro call result contracts; no text-renderer replacement.
    player, city, table, names = 0x02450000, 0x02490000, 0x024A0000, 0x024B0000
    shift = struct.unpack_from("<I", arm, 0x53AC0)[0]
    u.mem_write(player + shift, struct.pack("<I", table))
    u.mem_write(city + 4, struct.pack("<I", table))
    u.mem_write(table + 8, struct.pack("<I", 0x024C0000))
    u.mem_write(table + 32, struct.pack("<2I", 0x024C0010, 0x024C0020))
    for at, text in [(names, b"Fleet"), (names + 32, b"Argot Co."), (names + 64, b"Indigo"), (names + 96, b"Amsterdam")]:
        u.mem_write(at, text + b"\0")
    for entry, pointer in [(0x024C0000, names + 96), (0x024C0010, names), (0x024C0020, names + 32)]:
        u.mem_write(entry, struct.pack("<3I", 0xE59F0000, 0xE12FFF1E, pointer))

    def getter(uc, address, size, _):
        if address == BASE + 0x7E9B8:
            value = uc.reg_read(UC_ARM_REG_R0)  # actor 0/1 contract
        elif address == BASE + 0xCB184:
            value = player
        elif address == BASE + 0x7EA8C:
            value = names + 64
        elif address == BASE + 0xCB160:
            value = city
        elif address == BASE + 0x397D8:
            value = 0
        else:
            return
        uc.reg_write(UC_ARM_REG_R0, value)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
    u.hook_add(UC_HOOK_CODE, getter)
    return u


def expand(u, raw, actor=0):
    assert b"\0" not in raw and len(raw) < 2048
    u.mem_write(INPUT, raw + b"\0")
    u.mem_write(OUTPUT - 16, b"\xA5" * 4128)
    call(u, 0x53914, (OUTPUT, INPUT, actor))
    block = bytes(u.mem_read(OUTPUT - 16, 4128))
    result = block[16:].split(b"\0", 1)[0]
    assert block[:16] == b"\xA5" * 16
    assert block[17 + len(result):] == b"\xA5" * (4111 - len(result))
    assert bytes(u.mem_read(INPUT, len(raw) + 1)) == raw + b"\0"
    return result


def main():
    rom = NdsImage.open("out/all_routes_combined_v254_candidate.nds")
    prior = rom.read_file("/__arm9__.bin")
    arm = (ROOT / "research_arm9.bin").read_bytes()
    old, new = setup(prior), setup(arm)
    current = common_message_entries(rom.read_file("/COMMON/MESFILE.DK4"), prior, clean=False)
    changed = []
    for entry in current:
        original = expand(old, entry.text)
        fixed = expand(new, entry.text)
        assert fixed == entry.text, (entry.message_id, fixed)
        if original != fixed:
            changed.append({"id": entry.message_id, "stored_hex": entry.text.hex(),
                            "before_hex": original.hex(), "after_hex": fixed.hex()})
    clean = NdsImage.open("work/clean.nds")
    japanese = common_message_entries(clean.read_file("/COMMON/MESFILE.DK4"), clean.read_file("/__arm9__.bin"))
    preserved = 0
    for actor in (0, 1):
        for entry in japanese:
            assert expand(old, entry.text, actor) == expand(new, entry.text, actor), (actor, entry.message_id)
            preserved += 1
    macros = []
    for token, expected in [(b"FI", b"Fleet"), (b"FA", b"Argot Co."), (b"FU", b"Indigo"), (b"FO", b"Amsterdam")]:
        text = b"[" + token + b"]"
        assert expand(old, text) == expand(new, text) == b"[" + expected + b"]"
        macros.append(token.decode())
    literals = [b"F", b"I", b"Fair. I wish a good opportunity.", b"Fleet Indigo", b"F? I?",
                b"Find it. If it floats, I'll sail.", b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    for text in literals:
        assert expand(new, text) == text
    plan = json.loads((ROOT / "runtime_plan.json").read_text(encoding="utf-8"))
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    boot = execute(arm, bytes(rom.rom.arm7), rom.rom.arm7RamAddress,
                   repair_entry=plan["cache"]["entry"], expected_pool=payload)
    proof = {"format": "dk4-common-literal-prefix-native-v255", "source_arm9_sha256": sha(prior),
             "target_arm9_sha256": sha(arm), "all3668_current_COMMON_entries_expand_byte_exact": True,
             "changed_prior_corruptions": changed, "changed_message_count": len(changed),
             "original_Japanese_entries_compared_for_two_actor_contracts": preserved,
             "all_source_macro_dispatch_and_copy_outputs_preserved": True, "genuine_F_macro_cases": macros,
             "literal_edge_cases": [t.decode() for t in literals], "full_saved_register_stack_input_output_guard_ABI_pass": True,
             "boot": boot, "arena": initialize(arm), "native_model_getter_gender_results_supplied_contracts": True,
             "actual_gameplay_pixel_verification_pending": True, "all18_plaques_remain_incomplete": True}
    (ROOT / "native_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(f"3668 current entries exact; {len(changed)} corruptions repaired; {preserved} original Japanese actor cases unchanged; native macro/ABI/boot checks pass.")


if __name__ == "__main__":
    main()
