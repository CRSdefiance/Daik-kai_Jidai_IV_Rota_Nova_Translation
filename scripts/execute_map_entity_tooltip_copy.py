"""Execute native map label selection and tooltip printf, without raster approval."""

import json
import struct
from pathlib import Path

from unicorn import UC_ARCH_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_MODE_ARM, Uc
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R8,
    UC_ARM_REG_SP,
)

BASE, STACK, STOP = 0x02000000, 0x027F0000, 0x027E0000
OUTPUT, ARGUMENTS, ACTOR = 0x02410000, 0x02411000, 0x02412000


def machine_for(source):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(BASE, 0x800000)
    machine.mem_write(BASE, source)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    return machine


def select(source, case, machine=None):
    if case not in ('pirates', 'monster', 'unknown', 'named'):
        raise ValueError('Unmapped map entity selection case')
    machine = machine_for(source) if machine is None else machine
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.mem_write(ACTOR + 8, bytes([0xB5 if case == 'monster' else 1]))
    machine.reg_write(UC_ARM_REG_R8, ACTOR)
    machine.mem_write(ACTOR, struct.pack('<I', ACTOR + 0x40))
    machine.mem_write(ACTOR + 0x48, struct.pack('<I', ACTOR + 0x80))
    machine.mem_write(ARGUMENTS, b'Named faction\0')
    contracts = []

    def code(uc, address, size, _):
        if address in (BASE + 0x352F4, BASE + 0x3A3B4, ACTOR + 0x80):
            contracts.append(address)
            value = (0 if case == 'pirates' else ACTOR) if address == BASE + 0x352F4 else (
                0 if case == 'unknown' else 1) if address == BASE + 0x3A3B4 else ARGUMENTS
            uc.reg_write(UC_ARM_REG_R0, value)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif not BASE + 0x70424 <= address < BASE + 0x70470:
            raise ValueError('Map selection executes outside mapped branch sequence')

    handle = machine.hook_add(UC_HOOK_CODE, code)
    machine.emu_start(BASE + 0x70424, BASE + 0x70470, count=1000)
    machine.hook_del(handle)
    pointer = machine.reg_read(UC_ARM_REG_R8)
    raw = bytes(machine.mem_read(pointer, 64)).split(b'\0', 1)[0]
    expected = {'pirates': b'Pirates', 'monster': b'Monster',
                'unknown': b'???', 'named': b'Named faction'}[case]
    if raw != expected or machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Native map label selection loses full wording or stack')
    return {'case': case, 'pointer': pointer, 'full_text_hex': (raw + b'\0').hex(),
            'external_entity_resolution_contracts': contracts}


def format_copy(source, field, values, expected):
    if field not in (0x705F0, 0x705F4) or len(values) != (2 if field == 0x705F0 else 3):
        raise ValueError('Complete mapped tooltip arguments required')
    machine = machine_for(source)
    pointers = []
    for index, raw in enumerate(values):
        pointer = ARGUMENTS + index * 0x100
        machine.mem_write(pointer, raw + b'\0')
        pointers.append(pointer)
    machine.mem_write(OUTPUT, b'\xA5' * (len(expected) + 65))
    machine.reg_write(UC_ARM_REG_R0, OUTPUT)
    machine.reg_write(UC_ARM_REG_R1, struct.unpack_from('<I', source, field)[0])
    machine.reg_write(UC_ARM_REG_R2, pointers[0])
    machine.reg_write(UC_ARM_REG_R3, pointers[1])
    if len(pointers) == 3:
        machine.mem_write(STACK, struct.pack('<I', pointers[2]))
    executed = set()

    def code(uc, address, size, _):
        if not BASE <= address <= BASE + len(source) - size:
            raise ValueError('Tooltip printf executes outside native source')
        executed.add(address - BASE)

    def write(uc, access, address, size, value, _):
        if not ((STACK - 0x10000 <= address and address + size <= STACK + 4)
                or (OUTPUT <= address and address + size <= OUTPUT + len(expected) + 1)):
            raise ValueError('Native tooltip printf writes outside bounded output/stack')

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(BASE + 0xD7720, STOP, count=1000000)
    full = bytes(machine.mem_read(OUTPUT, len(expected) + 1))
    if full != expected + b'\0' or machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Native tooltip printf loses leading/last bytes, NUL or stack')
    if bytes(machine.mem_read(OUTPUT + len(expected) + 1, 64)) != b'\xA5' * 64:
        raise ValueError('Native tooltip printf damages output guard')
    if not {0xD7720, 0xD7754, 0xD7950} <= executed:
        raise ValueError('Actual native tooltip printf engine was not executed')
    return {'pointer_field': field, 'arguments_hex': [v.hex() for v in values],
            'full_text_hex': full.hex(), 'native_printf_executed': True,
            'leading_last_nul_stack_and_guard_preserved': True,
            'executed_offsets': sorted(executed)}


def main():
    root = Path('work/analysis/map_entity_tooltips_v139')
    source = (root / 'proposed_arm9.bin').read_bytes()
    selections = [select(source, case) for case in ('pirates', 'monster', 'unknown', 'named')]
    copies = []
    for name in (b'Pirates', b'Monster', b'???', b'Named faction'):
        copies.append(format_copy(source, 0x705F0, [name, b'Carrack'], name + b'\n  Carrack class'))
    for name, percent, armament in ((b'Fleet', b'100', b'250'), (b'Monster', b'0', b'1')):
        copies.append(format_copy(source, 0x705F4, [name, percent, armament],
                                  name + b'  ' + percent.rjust(6) + b'%\n  Armament ' + armament.rjust(8)))
    report = {'status': 'pass-native-selection-and-format-copy-raster-pending',
              'selections': selections, 'format_copies': copies,
              'limitations': ['Faction resolution and virtual-name lookup are external contracts.',
                              'Pixel/layout, longest dynamic strings and physical routing remain pending.']}
    (root / 'native_copy_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Four native selection branches and six complete native printf copies pass; raster pending.')


if __name__ == '__main__':
    main()
