"""Execute the actual ARM sprintf and every reached helper without substitution."""

import struct

from unicorn import UC_ARCH_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_MODE_ARM, Uc
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

BASE, OUTPUT, FORMAT, PLACE, NUMBER, NAME = 0x02000000, 0x02400020, 0x02401000, 0x02402000, 0x02402100, 0x02402200
STACK, STOP = 0x027F0000, 0x027FFF00


def execute(source, place, number, name):
    source = bytes(source)
    if not place or not number or not name or len(name) > 16 or b'\0' in name:
        raise ValueError('Complete native labels and name of at most sixteen bytes required')
    place_raw, number_raw = place.encode('ascii'), number.encode('ascii')
    name.decode('cp932')
    expected = place_raw + b' ' + number_raw + b' ' + name + b'\0'
    if len(expected) > 32:
        raise ValueError('Full result row does not fit the native buffer')
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(BASE, 0x800000)
    machine.mem_write(BASE, source)
    machine.mem_write(OUTPUT - 32, b'\xa5' * 96)
    for at, raw in ((FORMAT, b'%s %s %s'), (PLACE, place_raw), (NUMBER, number_raw), (NAME, name)):
        machine.mem_write(at, raw + b'\0')
    for register, value in ((UC_ARM_REG_R0, OUTPUT), (UC_ARM_REG_R1, FORMAT),
                            (UC_ARM_REG_R2, PLACE), (UC_ARM_REG_R3, NUMBER),
                            (UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, STOP)):
        machine.reg_write(register, value)
    preserved = {UC_ARM_REG_R4 + index: 0x12340000 + index for index in range(8)}
    for register, value in preserved.items():
        machine.reg_write(register, value)
    machine.mem_write(STACK, struct.pack('<I', NAME))
    executed, writes = set(), []
    instructions = 0

    def code_hook(uc, address, size, _):
        nonlocal instructions
        instructions += 1
        if not BASE <= address <= BASE + len(source) - size:
            raise ValueError('Printf executes outside the supplied native ARM9')
        executed.add(address - BASE)

    def write_hook(uc, access, address, size, value, _):
        if OUTPUT <= address and address + size <= OUTPUT + 32:
            writes.extend(range(address - OUTPUT, address - OUTPUT + size))
        elif not STACK - 0x10000 <= address <= STACK + 4 - size:
            raise ValueError('Printf writes outside its native output buffer and bounded stack')

    machine.hook_add(UC_HOOK_CODE, code_hook)
    machine.hook_add(UC_HOOK_MEM_WRITE, write_hook)
    machine.emu_start(BASE + 0xD7720, STOP, timeout=10000000, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP:
        raise ValueError('Native formatter did not return within its execution bound')
    if machine.reg_read(UC_ARM_REG_SP) != STACK or any(
            machine.reg_read(register) != value for register, value in preserved.items()):
        raise ValueError('Native printf changed the caller stack or preserved registers')
    actual = bytes(machine.mem_read(OUTPUT, len(expected)))
    guards = bytes(machine.mem_read(OUTPUT - 32, 32)) + bytes(machine.mem_read(OUTPUT + len(expected), 64 - len(expected)))
    if actual != expected or guards != b'\xa5' * len(guards):
        raise ValueError('Native printf dropped text/NUL or changed buffer neighbors')
    if machine.reg_read(UC_ARM_REG_R0) != len(expected) - 1 or sorted(set(writes)) != list(range(len(expected))):
        raise ValueError('Native printf length or complete output writes differ')
    return {'full_row_hex': actual.hex(), 'bytes_with_nul': len(actual),
            'instructions': instructions, 'executed_offsets': sorted(executed),
            'stack_balanced': True, 'callee_registers_preserved': True,
            'scope': 'Actual D7720 sprintf and all reached native helper bodies; no external formatter/copy models.'}
