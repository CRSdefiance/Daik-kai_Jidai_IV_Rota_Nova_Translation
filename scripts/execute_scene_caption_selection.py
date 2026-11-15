"""Execute native caption selection/centering/wrapper; drawing contracts explicit."""

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
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

BASE, FRAME, STACK, OWNER, STOP = 0x02000000, 0x02400000, 0x027F0000, 0x02410000, 0x0204300C


def execute(source, table, index, count, *, advance=6, wrapper_only=False, clear=0):
    if advance not in (5, 6):
        raise ValueError('Only mapped native caption advances are allowed')
    if not 0 <= index < count:
        raise ValueError('Caption index must be inside its native route array')
    source = bytes(source)
    pointer = struct.unpack_from('<I', source, table + index * 4)[0]
    offset = pointer - BASE
    if not 0 <= offset < len(source):
        raise ValueError('Caption source pointer escapes ARM9')
    raw = source[offset:source.index(0, offset)]
    if clear not in (0, 1):
        raise ValueError('Native wrapper clear flag must be zero or one')
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(BASE, 0x800000)
    machine.mem_write(BASE, source)
    machine.mem_write(FRAME + 0x50, struct.pack('<I', 70))
    registers = {UC_ARM_REG_R4: 2, UC_ARM_REG_R5: 0, UC_ARM_REG_R6: 1,
                 UC_ARM_REG_R7: index, UC_ARM_REG_R8: BASE + table,
                 UC_ARM_REG_R10: OWNER, UC_ARM_REG_R11: FRAME}
    for register, value in {**registers, UC_ARM_REG_SP: STACK}.items():
        machine.reg_write(register, value)
    stop = 0x027FFF00 if wrapper_only else STOP
    if wrapper_only:
        for register, value in ((UC_ARM_REG_R0, OWNER), (UC_ARM_REG_R1, clear),
                                (UC_ARM_REG_R2, pointer),
                                (UC_ARM_REG_R3, (128 - len(raw) * advance // 2) & 0xFFFFFFFF),
                                (UC_ARM_REG_LR, stop)):
            machine.reg_write(register, value)
        machine.mem_write(STACK, struct.pack('<2I', 70, 1))
    draws, executed, clears = [], set(), []

    def word(at):
        return struct.unpack('<I', machine.mem_read(at, 4))[0]

    def code(uc, address, size, _):
        if not BASE <= address <= BASE + len(source) - size:
            raise ValueError('Caption execution escapes supplied ARM9')
        executed.add(address - BASE)
        if address == BASE + 0xD5160:
            # External draw-local initialization; this is not its native body.
            context = uc.reg_read(UC_ARM_REG_R0)
            if uc.reg_read(UC_ARM_REG_R1) != OWNER + 0x6028 or uc.reg_read(UC_ARM_REG_R2) != 1:
                raise ValueError('Caption draw context initialization differs')
            uc.mem_write(context, bytes(0x48))
            uc.mem_write(context + 0x2C, struct.pack('<I', OWNER + 0x6028))
            uc.mem_write(context + 0x30, struct.pack('<I', 1))
        elif address == BASE + 0xD5404:
            context, text = uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)
            if text != pointer:
                raise ValueError('Native consumer selects a different complete caption')
            observed = bytes(uc.mem_read(text, len(raw) + 1))
            if observed != raw + b'\0':
                raise ValueError('Caption loses leading/last text or NUL')
            draws.append({'pointer': text, 'full_text_hex': observed.hex(),
                          'x': word(context + 0x24), 'y': word(context + 0x28),
                          'style': word(context + 0x30), 'tracking': word(context + 0x1C)})
        elif address == BASE + 0xD393C:
            if uc.reg_read(UC_ARM_REG_R0) != OWNER + 0x6028:
                raise ValueError('Native wrapper clears a different bitmap')
            clears.append(OWNER + 0x6028)
        elif address != BASE + 0xD5140:
            return
        # Explicit init/raster/destroy contracts poison caller registers.
        initializer_result = uc.reg_read(UC_ARM_REG_R0) if address == BASE + 0xD5160 else None
        for register in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3):
            uc.reg_write(register, 0xBAD00000 + register)
        if initializer_result is not None:
            # D5160 ends with MOV r0,r6 (the supplied context) at D51A0.
            uc.reg_write(UC_ARM_REG_R0, initializer_result)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    def write(uc, access, address, size, value, _):
        if not (STACK - 0x1000 <= address and address + size <= STACK + 8):
            raise ValueError('Native caption code writes outside bounded stack')

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(BASE + (0x456A0 if wrapper_only else 0x42FD0), stop,
                      timeout=10000000, count=20000)
    if machine.reg_read(UC_ARM_REG_PC) != stop or machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Caption selector/wrapper does not restore native stack')
    if any(machine.reg_read(register) != value for register, value in registers.items()):
        raise ValueError('Caption selector/wrapper damages preserved registers')
    expected_x = (128 - len(raw) * advance // 2) & 0xFFFFFFFF
    if len(draws) != 1 or (draws[0]['x'], draws[0]['y'], draws[0]['style']) != (expected_x, 70, 1):
        raise ValueError('Native full-caption centering/Y/style differs')
    if draws[0]['tracking'] != (advance - 6) & 0xFFFFFFFF:
        raise ValueError('Native caption tracking differs from its centering width')
    if wrapper_only and len(clears) != clear:
        raise ValueError('Native wrapper clear behavior changed')
    return {**draws[0], 'index': index, 'table': table, 'clear_calls': clears,
            'stack_and_registers_preserved': True, 'executed_offsets': sorted(executed),
            'scope': 'Actual 42FD0 selection/strlen/centering and 456A0 wrapper; D5160/D5404/D5140 external contracts.'}
