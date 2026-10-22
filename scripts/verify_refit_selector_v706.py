"""Verify all30 selected IDs and every other native COMMON ID at the new selector."""

from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_CPSR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.refit_help_release import IDS
from scripts.probe_button_prompt_native import BASE, STOP, call, machine
from scripts.trace_refit_text_v706 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    arm = (ROOT / 'target_arm9.bin').read_bytes()
    proof = read(ROOT / 'transform_proof.json')
    assert sha(arm) == proof['target_arm9_sha256']
    u = machine(arm)
    section = MainCodeFile(arm, BASE).sections[3]
    u.mem_write(POOL, bytes(section.data[:-48]))
    by_id = {r['message_id']: r for r in proof['records']}
    fallback = []

    def observe(cpu, address, size, _):
        if address == 0x0205528C:
            fallback.append(tuple(cpu.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_CPSR)))
            cpu.reg_write(UC_ARM_REG_PC, STOP)
    hook = u.hook_add(UC_HOOK_CODE, observe)
    cases = []
    try:
        for message_id in range(3668):
            regs = (message_id, 0x12345678, 0x87654321, 0x13579BDF)
            u.reg_write(UC_ARM_REG_CPSR, (u.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF) | 0xA0000000)
            flags = u.reg_read(UC_ARM_REG_CPSR)
            before = bytes(u.mem_read(BASE, 0x400000)) if message_id in by_id else None
            count = len(fallback)
            call(u, proof['helper_entry'] - BASE, regs)
            assert tuple(u.reg_read(r) for r in (UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)) == regs[1:]
            assert u.reg_read(UC_ARM_REG_CPSR) == flags
            if message_id in by_id:
                row = by_id[message_id]
                assert len(fallback) == count and u.reg_read(UC_ARM_REG_R0) == row['pointer']
                expected = bytes.fromhex(row['compiled_hex'])
                assert bytes(u.mem_read(row['pointer'], len(expected))) == expected
                assert bytes(u.mem_read(BASE, 0x400000)) == before
                cases.append({'message_id': message_id, 'returned_pointer': row['pointer'],
                    'complete_compiled_source_bytes_exact': True,
                    'all_other_volatile_arguments_flags_stack_saved_registers_and_main_RAM_exact': True})
            else:
                assert len(fallback) == count + 1 and fallback[-1] == (*regs, flags)
    finally:
        u.hook_del(hook)
    assert [r['message_id'] for r in cases] == list(IDS) and len(fallback) == 3638
    save(ROOT / 'selector_proof.json', {'all3668_native_message_IDs_exercised': True,
        'selected30_return_complete_reviewed_paragraphs': cases,
        'other3638_original_provider_entry_registers_flags_and_stack_exact': True,
        'unselected_original_provider_execution_not_bridged_as_new_IO_or_text_test': True,
        'source_to_target_arm9_sha256': [proof['source_arm9_sha256'], proof['target_arm9_sha256']],
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V706 selector:30 exact paragraphs and3638 transparent original-provider fallbacks; ABI, flags and source RAM pass.', flush=True)


if __name__ == '__main__':
    main()
