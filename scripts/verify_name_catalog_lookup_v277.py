"""Execute every current catalog key, alignment, caller and near-miss natively."""

import json

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
from scripts.prepare_name_catalog_v277 import ROOT
from scripts.probe_common_itcm_arena_reservation import initialize
from scripts.probe_persistent_name_arm7_boot_overlap import execute
from scripts.revalidate_name_migration_v276 import ROM
from scripts.verify_ordinary_name_fidelity_research import initialized

SOURCE = 0x02430020
REGS = (UC_ARM_REG_R0, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
        UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8,
        UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12)


def main():
    plan = json.loads((ROOT / "catalog_plan.json").read_text(encoding="utf-8"))
    arm = (ROOT / "catalog_research_only_arm9.bin").read_bytes()
    assert sha(arm) == plan["target_arm9_sha256"]
    rom = NdsImage.open(ROM)
    stage = MainCodeFile(arm, 0x02000000).sections[3]
    boot = execute(arm, bytes(rom.rom.arm7), rom.rom.arm7RamAddress,
                   repair_entry=plan["cache"]["entry"], expected_pool=bytes(stage.data[:-48]))
    arena = initialize(arm)
    cpu = initialized(arm)
    preserved = bytes(cpu.mem_read(plan["pool_span"][0], plan["pool_payload_bytes"]))
    scoped = [site + 4 for site in plan["scoped_call_sites"]]
    foreign = 0x020154AC
    keys = {bytes.fromhex(row["key_hex"]) for row in plan["records"]}
    cases, misses = [], []

    def test(raw, alignment, caller, expected_pointer):
        pointer = SOURCE + alignment
        cpu.mem_write(SOURCE - 32, b"\xA5" * 640)
        cpu.mem_write(pointer, raw + b"\0")
        guarded = bytes(cpu.mem_read(SOURCE - 32, 640))
        registers = {reg: 0x12345000 + index * 0x100 for index, reg in enumerate(REGS)}
        for reg, value in registers.items():
            cpu.reg_write(reg, value)
        cpu.reg_write(UC_ARM_REG_R1, pointer)
        cpu.reg_write(UC_ARM_REG_LR, caller)
        cpu.reg_write(UC_ARM_REG_SP, STACK)

        def stop(uc, address, size, _):
            if address == MACRO:
                uc.emu_stop()

        def writes(uc, access, address, size, value, _):
            assert STACK - 256 <= address < address + size <= STACK

        hook = cpu.hook_add(UC_HOOK_CODE, stop)
        write_hook = cpu.hook_add(UC_HOOK_MEM_WRITE, writes)
        try:
            cpu.emu_start(plan["entry"], STOP, count=100000)
        finally:
            cpu.hook_del(hook)
            cpu.hook_del(write_hook)
        assert cpu.reg_read(UC_ARM_REG_PC) == MACRO
        assert cpu.reg_read(UC_ARM_REG_R1) == (pointer if expected_pointer is None else expected_pointer)
        assert cpu.reg_read(UC_ARM_REG_LR) == caller and cpu.reg_read(UC_ARM_REG_SP) == STACK
        assert all(cpu.reg_read(reg) == value for reg, value in registers.items())
        assert bytes(cpu.mem_read(SOURCE - 32, 640)) == guarded

    for row in plan["records"]:
        raw = bytes.fromhex(row["key_hex"])
        for alignment in range(4):
            for caller in (*scoped, foreign):
                test(raw, alignment, caller, row["target_pointer"] if caller in scoped else None)
                cases.append({"key_hex": row["key_hex"], "alignment": alignment, "caller": caller,
                              "substitution": caller in scoped})
        for near in [raw[:-1], raw + b"x", bytes([raw[0] ^ 0x40]) + raw[1:]]:
            if not near or near in keys:
                continue
            for caller in scoped:
                test(near, 1, caller, None)
                misses.append({"key_hex": row["key_hex"], "near_miss_hex": near.hex(), "caller": caller})
    assert bytes(cpu.mem_read(plan["pool_span"][0], plan["pool_payload_bytes"])) == preserved
    before = NdsImage.open(ROM).read_file("/__arm9__.bin")
    from dk4tool.patch.main_pool_cache_visibility import POOL
    source_payload = bytes(MainCodeFile(before, 0x02000000).sections[3].data[:-48])
    assert preserved[:len(source_payload)] == source_payload
    proof = {"format": "dk4-name-catalog-native-lookup-v277", "target_ARM9_sha256": sha(arm),
             "source_ROM_sha256": plan["source_ROM_sha256"], "boot": boot, "arena": arena,
             "exact_key_alignment_and_caller_cases": cases, "negative_near_miss_cases": misses,
             "all_lookup_registers_stack_sources_NUL_and_input_guards_preserved": True,
             "lookup_only_writes_temporary_stack": True,
             "complete_inherited_pool_and_new_catalog_bytes_unchanged": True,
             "runtime_pool_base": POOL,
             "native_final_macro_copy_glyphs_and_deep_scenes_pending": True,
             "all18_plaque_hint_entries_remain_incomplete": True,
             "playable_ROM_modified": False, "full_goal_complete": False}
    (ROOT / "native_lookup_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"unique_keys": len(plan["records"]), "positive_and_foreign_cases": len(cases),
                      "negative_near_misses": len(misses), "pool_bytes": plan["pool_payload_bytes"]}))


if __name__ == "__main__":
    main()
