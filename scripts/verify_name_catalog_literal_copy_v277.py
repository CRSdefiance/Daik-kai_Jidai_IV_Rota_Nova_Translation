"""Real copy/expander transport for catalog outputs without live-name macros."""

import json

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

from dk4tool.patch.confirmed_name_message_catalog import MACRO
from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_map_entity_tooltip_copy import STACK, STOP
from scripts.prepare_name_catalog_v277 import ROOT
from scripts.verify_ordinary_name_fidelity_research import initialized

SOURCE, OUTPUT = 0x02430020, 0x02431020
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
         UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)


def main():
    plan = json.loads((ROOT / "catalog_plan.json").read_text(encoding="utf-8"))
    arm = (ROOT / "catalog_research_only_arm9.bin").read_bytes()
    assert sha(arm) == plan["target_arm9_sha256"]
    cpu = initialized(arm)
    pool = bytes(cpu.mem_read(plan["pool_span"][0], plan["pool_payload_bytes"]))
    cases, macro_pending = [], []
    for row in plan["records"]:
        key, target = bytes.fromhex(row["key_hex"]), bytes.fromhex(row["target_hex"])
        if b"F" in target or b"I" in target:
            macro_pending.append({"key_hex": row["key_hex"], "target_hex": row["target_hex"]})
            continue
        for alignment in range(4):
            for site in plan["scoped_call_sites"]:
                pointer = SOURCE + alignment
                cpu.mem_write(SOURCE - 32, b"\xA5" * 640)
                cpu.mem_write(pointer, key + b"\0")
                source_guard = bytes(cpu.mem_read(SOURCE - 32, 640))
                cpu.mem_write(OUTPUT - 32, b"\xA5" * 576)
                saved = {reg: 0x55110000 + index for index, reg in enumerate(SAVED)}
                for reg, value in saved.items():
                    cpu.reg_write(reg, value)
                cpu.reg_write(UC_ARM_REG_R0, OUTPUT)
                cpu.reg_write(UC_ARM_REG_R1, pointer)
                cpu.reg_write(UC_ARM_REG_R2, 0)
                cpu.reg_write(UC_ARM_REG_LR, site + 4)
                cpu.reg_write(UC_ARM_REG_SP, STACK)
                calls = []

                def observe(uc, address, size, _, calls=calls):
                    if address == MACRO:
                        calls.append(address)
                        uc.reg_write(UC_ARM_REG_LR, STOP)

                handle = cpu.hook_add(UC_HOOK_CODE, observe)
                try:
                    cpu.emu_start(plan["entry"], STOP, count=200000)
                finally:
                    cpu.hook_del(handle)
                assert cpu.reg_read(UC_ARM_REG_PC) == STOP and cpu.reg_read(UC_ARM_REG_SP) == STACK
                assert all(cpu.reg_read(reg) == value for reg, value in saved.items())
                assert calls == [MACRO]
                expected = b"\xA5" * 32 + target + b"\0" + b"\xA5" * (543 - len(target))
                assert bytes(cpu.mem_read(OUTPUT - 32, 576)) == expected, row["key_hex"]
                assert bytes(cpu.mem_read(SOURCE - 32, 640)) == source_guard
                cases.append({"key_hex": row["key_hex"], "alignment": alignment, "caller": site,
                              "complete_target_bytes": len(target), "native_expander_without_getter_bridges": True})
    assert bytes(cpu.mem_read(plan["pool_span"][0], plan["pool_payload_bytes"])) == pool
    proof = {"format": "dk4-name-catalog-native-literal-copy-v277", "target_ARM9_sha256": sha(arm),
             "literal_native_copy_cases": cases, "macro_keys_still_requiring_player_state_proof": macro_pending,
             "all512byte_output_first_last_NUL_input_guards_and_ABI_preserved": True,
             "source_text_controls_and_reserved_full_width_glyph_encoding_copied_exactly": True,
             "complete_pool_unchanged": True, "native_glyph_and_actual_scene_tests_pending": True,
             "playable_ROM_modified": False, "full_goal_complete": False}
    (ROOT / "native_literal_copy_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"literal_keys": len(plan["records"]) - len(macro_pending),
                      "native_copy_cases": len(cases), "macro_keys_pending": len(macro_pending)}))


if __name__ == "__main__":
    main()
