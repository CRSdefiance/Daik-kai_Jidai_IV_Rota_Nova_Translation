"""Execute actual Golden Route title lookup, centering and native printf copy."""

import struct

from unicorn import UC_ARCH_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_MODE_ARM, Uc
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_SP,
)

BASE, FRAME, GEOMETRY, STACK, STOP = 0x02000000, 0x02410000, 0x02411000, 0x027F0000, 0x020F2C40
TABLE = 0x16A1B0
TABLE_LITERAL = 0xF2D04


def execute(source, selection, *, y=12):
    if selection not in (0, 1) or not 0 <= y <= 181:
        raise ValueError('Unmapped Golden Route heading selection/geometry')
    table = struct.unpack_from('<I', source, TABLE_LITERAL)[0] - BASE
    if not 0 <= table <= len(source) - 8:
        raise ValueError('Golden Route title table escapes source')
    pointer = struct.unpack_from('<I', source, table + selection * 4)[0]
    offset = pointer - BASE
    if not 0 <= offset < len(source):
        raise ValueError('Golden Route title pointer escapes source')
    raw = source[offset:source.index(0, offset)]
    if not raw or b'%' in raw:
        raise ValueError('Golden Route title must be complete literal text')
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(BASE, 0x800000)
    machine.mem_write(BASE, bytes(source))
    machine.mem_write(FRAME + 0x218, struct.pack('<I', selection))
    machine.mem_write(GEOMETRY + 0x10, struct.pack('<I', y))
    machine.mem_write(STACK + 0x30, struct.pack('<I', 1))
    for reg, value in ((UC_ARM_REG_R5, FRAME), (UC_ARM_REG_R6, GEOMETRY), (UC_ARM_REG_SP, STACK)):
        machine.reg_write(reg, value)
    output = struct.unpack_from('<I', source, 0xD529C)[0]
    if not BASE + len(source) <= output <= BASE + 0x800000 - 0x400:
        raise ValueError('Native printf buffer literal differs')
    draws, executed = [], set()

    def word(address):
        return struct.unpack('<I', machine.mem_read(address, 4))[0]

    def code(uc, address, size, _):
        if not BASE <= address <= BASE + len(source) - size:
            raise ValueError('Golden Route heading executes outside source')
        executed.add(address - BASE)
        if address == BASE + 0xD5404:
            context, text = uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)
            formatted = bytes(uc.mem_read(text, len(raw) + 1))
            if context != STACK or text != output or formatted != raw + b'\0':
                raise ValueError('Native title printf loses leading/last bytes/NUL')
            draws.append({'full_text_hex': formatted.hex(), 'formatted_pointer': text,
                          'x': word(context + 0x24), 'y': word(context + 0x28),
                          'style': word(context + 0x30)})
            # Raster is executed independently with the selected actual text
            # and coordinates. This hook substitutes only this raster call.
            for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3):
                uc.reg_write(reg, 0xBAD00000 + reg)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    def write(uc, access, address, size, value, _):
        if not ((STACK - 0x10000 <= address and address + size <= STACK + 0x48)
                or (output <= address and address + size <= output + 0x400)):
            raise ValueError('Golden Route title printf writes outside bounded native storage')

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(BASE + 0xF2BFC, STOP, timeout=10000000, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Native Golden Route title does not restore its stack')
    if machine.reg_read(UC_ARM_REG_R5) != FRAME or machine.reg_read(UC_ARM_REG_R6) != GEOMETRY:
        raise ValueError('Native Golden Route title damages preserved owner/geometry')
    if len(draws) != 1 or (draws[0]['x'], draws[0]['y'], draws[0]['style']) != (128 - len(raw) * 3, y, 1):
        raise ValueError('Native Golden Route title centering/style differs')
    if 0xCE898 not in executed or 0xCED28 not in executed:
        raise ValueError('Native title strlen/printf bodies were not executed')
    return {'selection': selection, 'source_pointer': pointer, **draws[0],
            'native_strlen_printf_executed': True, 'stack_and_owners_preserved': True,
            'executed_offsets': sorted(executed)}
