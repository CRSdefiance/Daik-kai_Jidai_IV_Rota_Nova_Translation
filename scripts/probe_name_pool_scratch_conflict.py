"""Reproduce native scratch-image writes overlapping the research DTCM name pool."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for


def main():
    source = Path('work/analysis/joint_square_shopkeeper_research_arm9.bin').read_bytes()
    proof = json.loads(Path('work/analysis/joint_square_shopkeeper_native_proof.json').read_text(encoding='utf-8'))
    if sha(source) != proof['research_arm9_sha256']:
        raise ValueError('Exact combined research source required')
    machine = machine_for(source)
    machine.mem_map(0x01FF0000, 0x10000)

    def startup(uc, address, size, _):
        if address in (BASE + 0xA34, BASE + 0xA38, BASE + 0xA3C):
            uc.reg_write(UC_ARM_REG_PC, address + 4)

    hook = machine.hook_add(UC_HOOK_CODE, startup)
    machine.emu_start(BASE + 0x9E0, STOP, count=100000)
    machine.hook_del(hook)
    machine.emu_start(BASE + 0x88C, BASE + 0x8AC, count=3000000)
    scratch, text, result, bounds, cursor = (0x02450000, 0x02451000, 0x02452000, 0x02453000, 0x02454000)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_R0, scratch)
    machine.emu_start(BASE + 0xCAA4C, STOP, count=10000)
    header = struct.unpack('<5I', machine.mem_read(scratch, 20))
    if (header[0], header[1], header[2], scratch + header[4]) != (4, 64, 12, 0x027E0000):
        raise ValueError('Actual native scratch header differs')
    before = bytes(machine.mem_read(0x027E0000, 1536))
    font = struct.unpack_from('<I', source, 0xD5088)[0]
    machine.mem_write(font + 4, struct.pack('<2I', 6, 12))
    machine.mem_write(text, b'AB\0')
    machine.mem_write(bounds, struct.pack('<I', 0xFD))
    machine.mem_write(cursor, struct.pack('<I', 0))
    machine.mem_write(STACK, struct.pack('<I', cursor))
    for reg, value in ((UC_ARM_REG_R0, scratch), (UC_ARM_REG_R1, text),
                       (UC_ARM_REG_R2, result), (UC_ARM_REG_R3, bounds)):
        machine.reg_write(reg, value)
    writes = []

    def write(uc, access, address, size, value, _):
        if 0x027E0000 <= address < 0x027E0600:
            writes.append({'address': address, 'size': size, 'value': value,
                           'native_pc': uc.reg_read(UC_ARM_REG_PC)})

    hook = machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(BASE + 0xCA780, BASE + 0xCA810, count=100000)
    machine.hook_del(hook)
    after = bytes(machine.mem_read(0x027E0000, 1536))
    changed = [index for index, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
    if not writes or not changed or machine.reg_read(UC_ARM_REG_PC) != BASE + 0xCA810:
        raise ValueError('Native scratch overwrite was not reproduced')
    report = {'status': 'confirmed-native-scratch-conflict-research-allocation-rejected',
              'research_sha256': sha(source), 'scratch_constructor': 0xCAA4C,
              'scratch_render_entry': 0xCA780, 'scratch_render_stop': 0xCA810,
              'actual_scratch_header_words': list(header),
              'scratch_runtime_range': [0x027E0000, 0x027E0600],
              'scratch_width': 256, 'scratch_height': 12, 'changed_byte_offsets': changed,
              'native_overlapping_writes': writes, 'before_sha256': sha(before), 'after_sha256': sha(after),
              'candidate_changed': False,
              'required_next_action': 'Allocate persistent name text outside the native scratch image and SDK-owned state; rerun all source/pointer/startup/consumer/raster checks.',
              'limits': ['Actual constructor and ASCII scratch rendering execute; serialized/dialogue inputs are fixtures.',
                         'Reproduction proves runtime aliasing; it is not a physical gameplay reachability count.']}
    Path('work/analysis/name_pool_scratch_conflict_proof.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Confirmed native DTCM scratch conflict: {len(writes)} writes change {len(changed)} bytes of research name storage. Allocation rejected.')


if __name__ == '__main__':
    main()
