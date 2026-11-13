"""Verify startup ownership, bounded lookup ABI and native copies for every entry."""

import argparse
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_R12,
    UC_ARM_REG_SP,
)

from dk4tool.patch.confirmed_name_message_catalog import MACRO
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import STACK, STOP
from scripts.probe_persistent_name_arm7_boot_overlap import execute
from scripts.verify_ordinary_name_fidelity_research import initialized

ROOT = Path("work/analysis/confirmed_names_v200")
SOURCE, OUTPUT = 0x02430020, 0x02431020
REGS = (UC_ARM_REG_R0, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5,
        UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10,
        UC_ARM_REG_R11, UC_ARM_REG_R12)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    root = parser.parse_args().root
    plan = json.loads((root / "catalog_plan.json").read_text(encoding="utf-8"))
    raw = (root / "catalog_research_arm9.bin").read_bytes()
    assert sha(raw) == plan["target_arm9_sha256"]
    original = NdsImage.open("out/all_routes_combined_v190_candidate.nds")
    stage = MainCodeFile(raw, 0x02000000).sections[3]
    boot = execute(raw, bytes(original.rom.arm7), original.rom.arm7RamAddress,
                   plan["copy_entry"], bytes(stage.data[:-48]))
    assert boot["arm7_source_changed_bytes_after_arm9_autoload"] == 0
    assert all(row["matches_original"] for row in boot["arm7_native_loaded_sections"])
    assert all(boot[key] for key in ("repaired_pool_matches_complete_payload", "repair_returns_with_stack_preserved", "actual_startup_call_preserves_r0_r3"))
    machine = initialized(raw)
    lookup_cases, copy_cases = [], []
    scoped = [site + 4 for site in plan["scoped_call_sites"]]
    foreign = 0x020154AC
    preserved_pool = bytes(machine.mem_read(plan["pool_span"][0], plan["pool_payload_bytes"]))
    for row in plan["records"]:
        key, target = bytes.fromhex(row["key_hex"]), bytes.fromhex(row["target_hex"])
        for alignment in range(4):
            pointer = SOURCE + alignment
            for caller in (*scoped, foreign):
                machine.mem_write(SOURCE - 32, b"\xA5" * 640)
                machine.mem_write(pointer, key + b"\0")
                before_source = bytes(machine.mem_read(SOURCE - 32, 640))
                expected_regs = {reg: 0x12345000 + index * 0x100 for index, reg in enumerate(REGS)}
                expected_regs[UC_ARM_REG_R0] = OUTPUT
                expected_regs[UC_ARM_REG_R2] = 0
                for reg, value in expected_regs.items():
                    machine.reg_write(reg, value)
                machine.reg_write(UC_ARM_REG_R1, pointer)
                machine.reg_write(UC_ARM_REG_LR, caller)
                machine.reg_write(UC_ARM_REG_SP, STACK)

                def stop(uc, address, size, _):
                    if address == MACRO:
                        uc.emu_stop()

                def writes(uc, access, address, size, value, _):
                    if not STACK - 256 <= address < address + size <= STACK:
                        raise ValueError("Catalog lookup writes outside its temporary stack")

                a, b = machine.hook_add(UC_HOOK_CODE, stop), machine.hook_add(UC_HOOK_MEM_WRITE, writes)
                machine.emu_start(plan["entry"], STOP, count=20000)
                machine.hook_del(a)
                machine.hook_del(b)
                expected_pointer = row["target_pointer"] if caller in scoped else pointer
                assert machine.reg_read(UC_ARM_REG_PC) == MACRO
                assert machine.reg_read(UC_ARM_REG_R1) == expected_pointer
                assert machine.reg_read(UC_ARM_REG_LR) == caller and machine.reg_read(UC_ARM_REG_SP) == STACK
                assert all(machine.reg_read(reg) == value for reg, value in expected_regs.items())
                assert bytes(machine.mem_read(SOURCE - 32, 640)) == before_source
                lookup_cases.append({"key_hex": key.hex(), "alignment": alignment, "caller": caller,
                                     "replacement_selected": caller in scoped, "registers_stack_source_guards_preserved": True})
        # Execute the original expander/copy, using one explicit default-given-name
        # contract where FI needs a mutable player object not initialized here.
        machine.mem_write(SOURCE, key + b"\0")
        machine.mem_write(OUTPUT - 32, b"\xA5" * 1088)
        machine.reg_write(UC_ARM_REG_R0, OUTPUT)
        machine.reg_write(UC_ARM_REG_R1, SOURCE)
        machine.reg_write(UC_ARM_REG_R2, 0)
        machine.reg_write(UC_ARM_REG_LR, scoped[0])
        machine.reg_write(UC_ARM_REG_SP, STACK)
        native_entered, bridges = [], []

        def copy(uc, address, size, _, native_entered=native_entered, bridges=bridges):
            if address == MACRO:
                native_entered.append(address)
                uc.reg_write(UC_ARM_REG_LR, STOP)
            if address == 0x020539C4:
                # Source-locked table 0 / real changed-name getter already verified.
                uc.reg_write(UC_ARM_REG_R0, struct.unpack_from("<I", raw, 0x120B80)[0])
                uc.reg_write(UC_ARM_REG_PC, 0x02053A1C)
                bridges.append("default FI getter contract: Rafael")

        handle = machine.hook_add(UC_HOOK_CODE, copy)
        machine.emu_start(plan["entry"], STOP, count=20000)
        machine.hook_del(handle)
        expected = target.replace(b"FI", b"Rafael")
        actual = bytes(machine.mem_read(OUTPUT - 32, 1088))
        assert actual == b"\xA5" * 32 + expected + b"\0" + b"\xA5" * (1055 - len(expected))
        assert native_entered == [MACRO] and machine.reg_read(UC_ARM_REG_PC) == STOP
        assert machine.reg_read(UC_ARM_REG_SP) == STACK
        copy_cases.append({"key_hex": key.hex(), "full_output_hex": expected.hex(),
                           "native_expander_executed": True, "getter_contract_bridges": bridges,
                           "output_NUL_and_1024_byte_buffer_guards_preserved": True})
    assert bytes(machine.mem_read(plan["pool_span"][0], plan["pool_payload_bytes"])) == preserved_pool
    report = {"format": "dk4-confirmed-name-catalog-native-proof-v1",
              "target_arm9_sha256": sha(raw), "boot": boot, "lookup_cases": lookup_cases,
              "native_copy_cases": copy_cases, "all_inherited_and_catalog_pool_bytes_preserved": True,
              "all25_record_entries_prepared": len(plan["prepared_records"]) == 25,
              "scope": "Native lookup ABI/startup/cache and original macro-copy with explicit FI getter contract. Native player object, dispatch/pixels/gameplay still require connected evidence.",
              "research_only": True, "goal_complete": False}
    (root / "catalog_native_proof.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"records": len(plan["prepared_records"]), "lookup_cases": len(lookup_cases),
                      "native_copies": len(copy_cases), "ARM7_and_startup_pass": True, "live_pixels_pending": True}))


if __name__ == "__main__":
    main()
