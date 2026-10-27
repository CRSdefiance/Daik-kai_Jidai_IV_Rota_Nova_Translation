"""Execute zero-record dispatch, native printf and modal macro expansion."""

import struct

from unicorn import UC_ARCH_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_MODE_ARM, Uc
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

BASE, STACK = 0x02000000, 0x027F0000


def execute(source, *, count=0):
    if not 0 <= count <= 255:
        raise ValueError('Unmapped Golden Route record count')
    pointer = struct.unpack_from('<I', source, 0xF14D8)[0]
    offset = pointer - BASE
    if not 0 <= offset < len(source):
        raise ValueError('Zero-record message pointer escapes source')
    raw = source[offset:source.index(0, offset)]
    if not raw or len(raw) >= 0x100:
        raise ValueError('Zero-record literal message exceeds bounded copy scope')
    formatted, expanded = struct.unpack_from('<2I', source, 0x54890)
    for buffer in (formatted, expanded):
        if not BASE + len(source) + 32 <= buffer < BASE + 0x800000 - 0x420:
            raise ValueError('Modal message buffer literals differ')
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(BASE, 0x800000)
    machine.mem_write(BASE, bytes(source))
    for buffer in (formatted, expanded):
        machine.mem_write(buffer - 32, b'\xA5' * (len(raw) + 65))
    machine.reg_write(UC_ARM_REG_SP, STACK)
    executed, inputs = set(), []
    stop = BASE + (0x5479C if count == 0 else 0xF0B94)

    def code(uc, address, size, _):
        if not BASE <= address <= BASE + len(source) - size:
            raise ValueError('Zero-record native copy executes outside ARM9')
        executed.add(address - BASE)
        if address == BASE + 0xDB4F4:
            if uc.reg_read(UC_ARM_REG_R0) != 3:
                raise ValueError('Viewer requests a different record category')
            # External saved-record count contract; no save-file claim.
            uc.reg_write(UC_ARM_REG_R0, count)
            for reg in (UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3):
                uc.reg_write(reg, 0xBAD00000 + reg)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == BASE + 0x5473C:
            if uc.reg_read(UC_ARM_REG_R0) != pointer:
                raise ValueError('Zero-record dialog receives a different complete string')
            inputs.append(pointer)

    def write(uc, access, address, size, value, _):
        if not ((STACK - 0x10000 <= address and address + size <= STACK)
                or any(buffer <= address and address + size <= buffer + len(raw) + 1 for buffer in (formatted, expanded))):
            raise ValueError('Modal copy escapes bounded stack/message buffers')

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(BASE + 0xF0B70, stop, timeout=10000000, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != stop:
        raise ValueError('Zero-record dispatch/copy failed to reach its native continuation')
    if count:
        if inputs or machine.reg_read(UC_ARM_REG_SP) != STACK:
            raise ValueError('Nonempty viewer enters the empty-message dialog')
        return {'count': count, 'empty_dialog_selected': False, 'executed_offsets': sorted(executed)}
    for buffer in (formatted, expanded):
        if bytes(machine.mem_read(buffer, len(raw) + 1)) != raw + b'\0':
            raise ValueError('Modal printf/macro expansion drops or changes complete English')
        guards = bytes(machine.mem_read(buffer - 32, 32)) + bytes(machine.mem_read(buffer + len(raw) + 1, 31))
        if guards != b'\xA5' * 63:
            raise ValueError('Modal native copy overwrites neighboring bytes')
    if inputs != [pointer] or not {0x5473C, 0x54774, 0xCE898, 0x53914}.issubset(executed):
        raise ValueError('Complete zero-record formatted-copy pipeline was not executed')
    if machine.reg_read(UC_ARM_REG_SP) != STACK - 0xE0:
        raise ValueError('Modal copy damages its live native stack frame')
    return {'count': 0, 'empty_dialog_selected': True, 'pointer': pointer,
            'complete_text_hex': (raw + b'\0').hex(), 'native_printf_macro_expansion': True,
            'native_stack_frame_intact': True, 'executed_offsets': sorted(executed)}
