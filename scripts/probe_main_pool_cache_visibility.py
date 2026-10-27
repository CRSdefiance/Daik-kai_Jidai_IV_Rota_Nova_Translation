"""Execute SDK cache instructions with an explicit dirty/stale-cache model.

Unicorn does not model the ARM946 cache hardware. Only exact source-locked
MCRs are skipped; their operands and effects are checked independently here.
"""

import json
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R2

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, cache_plan, transform


class CacheMonitor:
    def __init__(self, machine, source):
        self.machine = machine
        self.plan = cache_plan(source)
        self.payload = bytes(MainCodeFile(source, BASE).sections[3].data[:-48])
        self.ram = bytearray(b'\xA5' * len(self.payload))
        self.dirty = bytearray(self.ram)
        self.pending = {}
        self.stale_instruction_lines = set(range(0, len(self.payload), 32))
        self.events = []
        self.handles = [machine.hook_add(UC_HOOK_MEM_WRITE, self.write),
                        machine.hook_add(UC_HOOK_CODE, self.code)]

    def write(self, uc, access, address, size, value, _):
        if POOL <= address < POOL + len(self.payload):
            if address + size > POOL + len(self.payload):
                raise ValueError('Pool write crosses its declared extent')
            offset = address - POOL
            self.dirty[offset:offset + size] = value.to_bytes(size, 'little')

    def code(self, uc, address, size, _):
        if not self.plan or address not in self.plan['operations']:
            return
        operation = self.plan['operations'][address]
        line = uc.reg_read(UC_ARM_REG_R0) - POOL
        if operation.startswith('drain'):
            if uc.reg_read(UC_ARM_REG_R2) != 0:
                raise ValueError('SDK write-buffer drain operand differs')
            for offset, data in self.pending.items():
                self.ram[offset:offset + 32] = data
            self.pending.clear()
        else:
            if line % 32 or not 0 <= line < len(self.payload):
                raise ValueError('Cache operation escaped an aligned payload line')
            if operation == 'invalidate_instruction':
                self.stale_instruction_lines.discard(line)
            else:
                self.pending[line] = bytes(self.dirty[line:line + 32])
        self.events.append((operation, line))
        uc.reg_write(UC_ARM_REG_PC, address + 4)

    def finish(self):
        for handle in self.handles:
            self.machine.hook_del(handle)
        if not self.plan:
            if bytes(self.dirty) != self.payload:
                raise ValueError('Legacy comparison did not copy the entire payload into dirty data')
            return {'maintenance_present': False,
                    'complete_payload_copied_into_dirty_data': True,
                    'stale_instruction_line_count': len(self.stale_instruction_lines),
                    'backing_RAM_remains_stale': bytes(self.ram) != self.payload,
                    'worst_case_dirty_data_and_stale_instruction_model_visible': (
                        bytes(self.ram) == self.payload and not self.stale_instruction_lines),
                    'physical_cache_verified': False}
        expected = [(op, line) for line in range(0, len(self.payload), 32)
                    for op in ('drain', 'invalidate_instruction', 'clean_flush_data')]
        expected.append(('drain_final', len(self.payload)))
        if (self.events != expected or self.pending or self.stale_instruction_lines
                or bytes(self.ram) != self.payload or bytes(self.dirty) != self.payload):
            raise ValueError('Incomplete cache maintenance or stale executable payload')
        return {'maintenance_present': True, 'line_count': len(self.payload) // 32,
                'native_cache_instruction_count': len(self.events),
                'complete_ordered_line_operands_and_final_drain_verified': True,
                'worst_case_dirty_data_and_stale_instruction_model_visible': True,
                'model_contract': 'All copied data starts dirty; RAM and instruction cache start stale. '
                                  'SDK clean/flush stages each line; drain commits it; I-line operation invalidates it.',
                'physical_cache_verified': False}


def main():
    from dk4tool.rom.nds import NdsImage
    from scripts.probe_common_itcm_arena_reservation import initialize as arenas
    from scripts.probe_common_itcm_arena_reservation import verify as arena_bounds
    from scripts.probe_item_source_canvas import source_canvas
    from scripts.probe_persistent_name_arm7_boot_overlap import execute
    source = Path('work/analysis/item_interface_research_arm9.bin').read_bytes()
    saved, plan = transform(source)
    if saved != Path('work/analysis/item_interface_cache_research_arm9.bin').read_bytes():
        raise ValueError('Saved cache research differs from deterministic transform')
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    results = {}
    for label, raw in (('original_data_only', source), ('cache_maintained', saved)):
        payload = bytes(MainCodeFile(raw, BASE).sections[3].data[:-48])
        results[label] = execute(raw, bytes(image.rom.arm7), image.rom.arm7RamAddress,
                                 True, payload)
        boot = results[label]
        if (boot['arm7_source_changed_bytes_after_arm9_autoload']
                or not all(r['matches_original'] for r in boot['arm7_native_loaded_sections'])
                or not all(boot[k] for k in ('repaired_pool_matches_complete_payload',
                                            'repair_returns_with_stack_preserved',
                                            'actual_startup_call_preserves_r0_r3'))):
            raise ValueError('Native cache wrapper breaks startup ownership or ABI')
        if not all(boot['SDK_staged_code_cache_line_coverage'][key]
                   for key in ('all_instruction_lines_selected', 'all_data_lines_selected')):
            raise ValueError('SDK cache maintenance does not cover all staged wrapper code')
    if (results['original_data_only']['late_copy_cache_model']['maintenance_present']
            or not results['cache_maintained']['late_copy_cache_model']['maintenance_present']):
        raise ValueError('Cache maintenance differential differs')
    allocation = arenas(saved)
    if allocation['low'][0] != plan['new_main_arena_low']:
        raise ValueError('Native arena fails to reserve complete executable payload')
    report = {'status': 'pass-native-startup-and-explicit-cache-model-research',
              'source_sha256': sha(source), 'target_sha256': sha(saved), 'plan': plan,
              'boot': results, 'canvas': source_canvas(saved),
              'native_initial_arenas': allocation,
              'resident_ITCM_arena_bounds': arena_bounds(saved, 0x01FFA000),
              'physical_cold_boot_cache_and_gameplay_verified': False}
    Path('work/analysis/item_interface_cache_native_proof.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Pass: exact item payload preserved, full copy/ABI/ARM7 ownership, '
          '612 ordered cache lines/final drain, native canvas/clear/dispatch.')


if __name__ == '__main__':
    main()
