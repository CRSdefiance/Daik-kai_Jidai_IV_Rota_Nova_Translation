"""Research escaped-name/amount coexistence in the actual native string ring."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for
from scripts.probe_common_display_name_escape import (
    CODE,
    INPUT,
    expected_display_name,
    helper_bytes,
)


def execute(source, name, index):
    if not 0 <= index < 32 or not name or len(name) > 18 or b'\0' in name:
        raise ValueError('Bounded stored name and native ring index required')
    safe = expected_display_name(name)
    root = struct.unpack_from('<I', source, 0xABFC0)[0]
    slots = root + 12
    machine = machine_for(source)
    machine.mem_write(CODE, helper_bytes())
    machine.mem_write(INPUT, name + b'\0')
    machine.mem_write(root - 32, b'\xa5' * (32 + 12 + 4096 + 32))
    machine.mem_write(root + 8, struct.pack('<I', index))

    def write(uc, access, address, size, value, _):
        if not ((address == root + 8 and size == 4)
                or (slots <= address and address + size <= slots + 4096)
                or (STACK - 0x1000 <= address and address + size <= STACK)):
            raise ValueError('Ring preparation writes outside ring/index/stack')

    machine.hook_add(UC_HOOK_MEM_WRITE, write)

    def run(offset):
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.emu_start(offset, STOP, count=10000)
        if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
            raise ValueError('Native allocator/helper/converter return or stack differs')

    machine.reg_write(UC_ARM_REG_R0, root)
    run(BASE + 0xAC000)
    name_pointer = machine.reg_read(UC_ARM_REG_R0)
    if name_pointer != slots + index * 128:
        raise ValueError('Native ring allocator selects a different name slot')
    machine.reg_write(UC_ARM_REG_R0, INPUT)
    machine.reg_write(UC_ARM_REG_R1, name_pointer)
    run(CODE)
    machine.reg_write(UC_ARM_REG_R0, 884629)
    run(BASE + 0xABF50)
    amount_pointer = machine.reg_read(UC_ARM_REG_R0)
    digits = '８８４６２９'.encode('cp932') + b'\0'
    expected_amount = slots + ((index + 1) % 32) * 128 + 128 - len(digits)
    if amount_pointer != expected_amount:
        raise ValueError('Native amount does not occupy the next distinct ring slot')
    expected = bytearray(b'\xa5' * (32 + 12 + 4096 + 32))
    struct.pack_into('<I', expected, 40, (index + 2) % 32)
    for pointer, value in ((name_pointer, safe + b'\0'), (amount_pointer, digits)):
        offset = pointer - (root - 32)
        expected[offset:offset + len(value)] = value
    if bytes(machine.mem_read(root - 32, len(expected))) != expected:
        raise ValueError('Amount allocation corrupts escaped name or ring neighbors')
    if bytes(machine.mem_read(INPUT, len(name) + 1)) != name + b'\0':
        raise ValueError('Ring helper changes original stored name')
    return {'initial_index': index, 'stored_name_hex': name.hex(),
            'display_name_hex': safe.hex(), 'name_pointer': name_pointer,
            'amount_pointer': amount_pointer, 'next_index': (index + 2) % 32,
            'distinct_slots': True, 'all_other_ring_bytes_intact': True}


def main():
    source = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    cases = [execute(source, name, index) for index in range(32)
             for name in (b'F' * 18, b'I' * 18, b'ABCDEFGHIJKLMNOPQR', 'あ'.encode('cp932') * 9)]
    report = {'status': 'pass-research-native-ring-coexistence', 'arm9_sha256': sha(source),
              'cases': cases,
              'limitations': 'Actual AC000 allocation, research escape helper and actual ABF50 run in one machine. Caller hook, COMMON loader and intervening allocations before display remain unproven; no ROM change.'}
    Path('work/analysis/common_display_name_ring_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} native ring cases preserve escaped name and amount across every index/wrap.')


if __name__ == '__main__':
    main()
