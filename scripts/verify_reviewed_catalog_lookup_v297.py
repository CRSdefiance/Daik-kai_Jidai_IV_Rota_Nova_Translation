"""All reviewed keys: route/caller scope, four input alignments and guards."""

import json
import struct

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
    UC_ARM_REG_R12,
    UC_ARM_REG_SP,
)

from dk4tool.patch.confirmed_name_message_catalog import CALLS, MACRO
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.reviewed_name_catalog import ROUTE
from scripts.prepare_reviewed_names_v297 import ROOT
from scripts.verify_ordinary_name_fidelity_research import initialized

REGS = (UC_ARM_REG_R0, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
        UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R12)


def main(*, root=ROOT):
    plan = json.loads((root / 'catalog_plan.json').read_text(encoding='utf-8'))
    arm = (root / 'catalog_arm9_research_only.bin').read_bytes()
    assert sha(arm) == plan['target_arm9_sha256']
    cpu = initialized(arm)
    original_sp = 0x027F0000
    cases, invalid = [], []

    def test(row, route, alignment, caller, key=None):
        raw = bytes.fromhex(row['key_hex']) if key is None else key
        pointer = 0x02468020 + alignment
        cpu.mem_write(pointer - 16, b'\xA5' * (len(raw) + 33))
        cpu.mem_write(pointer, raw + b'\0')
        before = bytes(cpu.mem_read(pointer - 16, len(raw) + 33))
        cpu.mem_write(ROUTE, struct.pack('<I', route))
        values = {reg: 0xBAD00100 + number for number, reg in enumerate(REGS)}
        for reg, value in values.items():
            cpu.reg_write(reg, value)
        cpu.reg_write(UC_ARM_REG_R1, pointer)
        cpu.reg_write(UC_ARM_REG_LR, caller)
        cpu.reg_write(UC_ARM_REG_SP, original_sp)
        cpu.emu_start(plan['entry'], MACRO, count=500000)
        assert cpu.reg_read(UC_ARM_REG_PC) == MACRO
        assert cpu.reg_read(UC_ARM_REG_SP) == original_sp and cpu.reg_read(UC_ARM_REG_LR) == caller
        assert all(cpu.reg_read(reg) == value for reg, value in values.items())
        hit = (key is None and route < 4 and row['route_mask'] & (1 << route)
               and caller in [0x02000000 + field + 4 for field in CALLS])
        expected = row['target_pointer'] if hit else pointer
        assert cpu.reg_read(UC_ARM_REG_R1) == expected
        assert bytes(cpu.mem_read(pointer - 16, len(raw) + 33)) == before
        if hit:
            target = bytes.fromhex(row['target_hex'])
            assert bytes(cpu.mem_read(expected, len(target) + 1)) == target + b'\0'
        return bool(hit)

    for index, row in enumerate(plan['records']):
        own = next(route for route in range(4) if row['route_mask'] & (1 << route))
        for alignment in range(4):
            for field in CALLS:
                assert test(row, own, alignment, 0x02000000 + field + 4)
                cases.append([index, own, alignment, field])
        for route in range(4):
            hit = test(row, route, 0, 0x02000000 + CALLS[0] + 4)
            assert hit == bool(row['route_mask'] & (1 << route))
            invalid.append([index, route, 'native-route-mask'])
        assert not test(row, own, 0, 0x02024204)
        assert not test(row, 255, 0, 0x02000000 + CALLS[0] + 4)
        raw = bytes.fromhex(row['key_hex']) + b'!'
        assert not test(row, own, 0, 0x02000000 + CALLS[0] + 4, raw)
    proof = {'format': 'dk4-full-reviewed-native-catalog-lookup-v297',
             'target_arm9_sha256': sha(arm), 'keys': len(plan['records']),
             'all_key_four_alignment_three_caller_cases': cases,
             'all_key_four_route_mask_cases': invalid,
             'foreign_caller_invalid_route_and_exact_NUL_near_miss_cases': len(plan['records']) * 3,
             'all_saved_registers_stack_LR_input_and_complete_target_guards_pass': True,
             'actual_native_macro_expansion_and_full_glyphs_pending': True,
             'playable_ROM_modified': False, 'full_goal_complete': False}
    (root / 'native_lookup_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} aligned scoped lookups; {len(invalid)} route cases; {len(plan["records"]) * 3} fallbacks/near misses pass.')


if __name__ == '__main__':
    main()
