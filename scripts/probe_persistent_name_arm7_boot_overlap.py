"""Execute both autoloaders to test ARM7 boot-source ownership and staged repair."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_ARCH_ARM, UC_HOOK_CODE, UC_MODE_ARM, Uc
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

BASE, POOL, STAGE, STOP, STACK = 0x02000000, 0x02387A20, 0x023A7200, 0x027F0000, 0x027FF000
SOURCE147 = '33dc6e6ac7ababb513a773647edd6f93cb5c08b19fad2500e7695f95d8629d75'
SOURCE148 = 'bb637907df8e9a4334f29219cd8273ea92731992b2bc4f9852525c68f9fed6af'


def late_copy_instruction_budget(payload_bytes):
    if payload_bytes <= 0 or payload_bytes % 4:
        raise ValueError('Aligned complete late-copy payload required')
    return max(10000, payload_bytes + 6 * ((payload_bytes + 31) // 32) + 128)


def staged(source):
    code = MainCodeFile(source, BASE)
    if sha(source) != SOURCE148 or len(code.sections) != 4:
        raise ValueError('Exact saved V148 required')
    payload = bytes(code.sections[3].data)
    if len(payload) != 1504 or code.sections[3].ramAddress != POOL:
        raise ValueError('Original name section differs')
    address = STAGE + len(payload)
    # Preserve r0-r3/LR; copy the complete aligned payload after BSS clearing.
    words = [0xE92D400F, 0xE59F0018, 0xE59F1018, 0xE59F2018,
             0xE4903004, 0xE4813004, 0xE2522004, 0x1AFFFFFB,
             0xE8BD800F, STAGE, POOL, len(payload)]
    stub = struct.pack('<12I', *words)
    if struct.unpack_from('<I', source, 0x8E4)[0] != 0xEB000BD9:
        raise ValueError('Native empty startup hook differs')
    branch = 0xEB000000 | (((address - (BASE + 0x8E4 + 8)) // 4) & 0xFFFFFF)
    struct.pack_into('<I', code.sections[0].data, 0x8E4, branch)
    code.sections[3].ramAddress = STAGE
    code.sections[3].data = bytearray(payload + stub)
    saved = bytes(code.save())
    return saved, payload, address


def execute(arm9, arm7, arm7_base, repair_entry=None, expected_pool=None):
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.mem_map(BASE, 0x800000)
    uc.mem_map(0x01FF0000, 0x10000)
    uc.mem_map(0x037F0000, 0x30000)
    uc.mem_write(BASE, arm9)
    uc.mem_write(arm7_base, arm7)
    uc.reg_write(UC_ARM_REG_SP, STACK)
    uc.reg_write(UC_ARM_REG_LR, STOP)
    sdk_cache_lines = {BASE + 0xA38: [], BASE + 0xA3C: []}

    def cache(machine, address, size, _):
        if address in (BASE + 0xA34, BASE + 0xA38, BASE + 0xA3C):
            if address in sdk_cache_lines:
                sdk_cache_lines[address].append(machine.reg_read(UC_ARM_REG_R4))
            machine.reg_write(UC_ARM_REG_PC, address + 4)

    handle = uc.hook_add(UC_HOOK_CODE, cache)
    uc.emu_start(BASE + 0x9E0, STOP, count=100000)
    uc.hook_del(handle)
    if uc.reg_read(UC_ARM_REG_PC) != STOP:
        raise ValueError('ARM9 loader did not return')
    after9 = bytes(uc.mem_read(arm7_base, len(arm7)))
    changed = sum(a != b for a, b in zip(after9, arm7))
    uc.reg_write(UC_ARM_REG_LR, STOP)
    uc.emu_start(arm7_base + 0x100, STOP, count=1000000)
    if uc.reg_read(UC_ARM_REG_PC) != STOP:
        raise ValueError('ARM7 loader did not return')
    sections = MainCodeFile(arm7, arm7_base).sections[1:]
    rows = [{'address': s.ramAddress, 'length': len(s.data),
             'matches_original': bytes(uc.mem_read(s.ramAddress, len(s.data))) == bytes(s.data)}
            for s in sections]
    result = {'arm7_source_changed_bytes_after_arm9_autoload': changed,
              'arm7_native_loaded_sections': rows,
              'order_contract': 'ARM9 autoload runs before ARM7 source relocation; actual scheduling not modeled',
              'cache_contract': 'ARM9 cache-maintenance instructions skipped'}
    arm9_sections = MainCodeFile(arm9, BASE).sections
    if len(arm9_sections) == 4 and arm9_sections[3].ramAddress == STAGE:
        stage_bytes = len(arm9_sections[3].data)
        expected = set(range(STAGE, STAGE + stage_bytes, 32))
        result['SDK_staged_code_cache_line_coverage'] = {
            'stage_span': [STAGE, STAGE + stage_bytes], 'line_count': len(expected),
            'all_instruction_lines_selected': expected <= set(sdk_cache_lines[BASE + 0xA38]),
            'all_data_lines_selected': expected <= set(sdk_cache_lines[BASE + 0xA3C]),
            'physical_cache_instructions_are_explicitly_skipped': True}
    if repair_entry:
        uc.reg_write(UC_ARM_REG_LR, STOP)
        uc.emu_start(BASE + 0x88C, BASE + 0x8AC, count=3000000)
        uc.reg_write(UC_ARM_REG_LR, STOP)
        before_sp = uc.reg_read(UC_ARM_REG_SP)
        regs = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)
        before_regs = [uc.reg_read(reg) for reg in regs]
        if expected_pool is None or len(expected_pool) % 4:
            raise ValueError('Aligned complete late-copy payload required')
        # Four instructions copy each four-byte word. A fixed 10000-step cap
        # cuts off larger valid pools before POP restores the saved registers.
        instruction_budget = late_copy_instruction_budget(len(expected_pool))
        from scripts.probe_main_pool_cache_visibility import CacheMonitor
        monitor = CacheMonitor(uc, arm9)
        uc.emu_start(BASE + 0x8E4, BASE + 0x8E8, count=instruction_budget)
        result['late_copy_cache_model'] = monitor.finish()
        result['late_copy_instruction_budget'] = instruction_budget
        result['late_copy_reached_caller_continuation'] = uc.reg_read(UC_ARM_REG_PC) == BASE + 0x8E8
        if not result['late_copy_reached_caller_continuation']:
            raise ValueError('Actual startup late copy did not reach its caller continuation')
        result['repaired_pool_matches_complete_payload'] = bytes(uc.mem_read(POOL, len(expected_pool))) == expected_pool
        result['repair_returns_with_stack_preserved'] = uc.reg_read(UC_ARM_REG_PC) == BASE + 0x8E8 and uc.reg_read(UC_ARM_REG_SP) == before_sp
        result['actual_startup_call_preserves_r0_r3'] = [uc.reg_read(reg) for reg in regs] == before_regs
        if not result['actual_startup_call_preserves_r0_r3']:
            raise ValueError('Actual startup hook clobbers preserved registers')
    return result


def main():
    original = NdsImage.open('out/all_routes_combined_v147_candidate.nds')
    failed = NdsImage.open('out/all_routes_combined_v148_candidate.nds')
    s147, s148 = [i.read_file('/__arm9__.bin') for i in (original, failed)]
    if sha(s147) != SOURCE147 or sha(s148) != SOURCE148 or original.rom.arm7 != failed.rom.arm7:
        raise ValueError('Exact transition sources required')
    arm7, base7 = bytes(failed.rom.arm7), failed.rom.arm7RamAddress
    fixed, payload, entry = staged(s148)
    if STAGE < base7 + len(arm7):
        raise ValueError('Staging still overlaps ARM7 source')
    cases = {'v147': execute(s147, arm7, base7), 'v148': execute(s148, arm7, base7),
             'staged_research': execute(fixed, arm7, base7, entry, payload)}
    if (cases['v147']['arm7_source_changed_bytes_after_arm9_autoload'] != 0
            or not all(s['matches_original'] for s in cases['v147']['arm7_native_loaded_sections'])
            or cases['v148']['arm7_source_changed_bytes_after_arm9_autoload'] == 0
            or all(s['matches_original'] for s in cases['v148']['arm7_native_loaded_sections'])
            or cases['staged_research']['arm7_source_changed_bytes_after_arm9_autoload'] != 0
            or not all(s['matches_original'] for s in cases['staged_research']['arm7_native_loaded_sections'])
            or not cases['staged_research']['repaired_pool_matches_complete_payload']
            or not cases['staged_research']['repair_returns_with_stack_preserved']):
        raise ValueError('Cross-CPU ownership or staged copy evidence differs')
    report = {'arm7_source_sha256': sha(arm7), 'arm7_initial_load_span': [base7, base7 + len(arm7)],
              'failed_pool_span': [POOL, POOL + len(payload)], 'staging_address': STAGE,
              'research_sha256': sha(fixed), 'cases': cases,
              'status': 'proven-order-dependent-arm7-source-corruption-staged-repair-research',
              'limitations': ['Actual ARM9/ARM7 scheduling and full cold boot remain unverified.',
                              'Research ARM9 only; not a registered playable ROM.']}
    Path('work/analysis/persistent_name_staged_boot_research_arm9.bin').write_bytes(fixed)
    Path('work/analysis/persistent_name_arm7_boot_overlap.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
