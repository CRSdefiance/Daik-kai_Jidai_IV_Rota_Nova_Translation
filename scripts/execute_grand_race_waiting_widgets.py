"""Bounded execution of actual ARM widget code, not a gameplay emulator."""

import struct

from dk4tool.patch.grand_race_waiting_widget import INIT_START, immediate

BASE = 0x02000000
STACK = 0x02300000
OWNER = 0x02301000
TABLE = 0x16B470
ALLOWED = ((0xF8508, 0xF85D8), (0xFAFFC, 0xFB038), (0xFB1EC, 0xFB220))


def execute(arm9, strings, *, scratch_table=True):
    """Run initialization, native constructors, virtual setter and linked append.

    Every instruction comes from the proposed ARM9. Unsupported instructions,
    uninitialized scratch reads and unexpected control flow fail closed.
    Three text pointers are supplied as scratch allocation inputs; this does not
    allocate or change the source ROM's text pool.
    """
    memory = {OWNER + 0x70: 0}
    if scratch_table:
        memory[BASE + 0xF89DC] = BASE + TABLE
        for index, pointer in enumerate(strings):
            memory[BASE + TABLE + index * 4] = pointer
    registers = [0xDEADDEAD] * 16
    registers[9], registers[10], registers[13] = 0, OWNER, STACK
    pc = BASE + INIT_START
    zero, carry = False, False
    calls, writes, steps = [], [], 0

    def read(address):
        if address & 3:
            raise ValueError('Unaligned ARM word read')
        if address in memory:
            return memory[address]
        if BASE <= address <= BASE + len(arm9) - 4:
            return struct.unpack_from('<I', arm9, address - BASE)[0]
        raise ValueError(f'Uninitialized scratch read at {address:#x}')

    def write(address, value):
        if address & 3:
            raise ValueError('Unaligned ARM word write')
        if not STACK - 8 <= address < STACK + 636 and not OWNER <= address < OWNER + 0x200:
            raise ValueError(f'Unexpected native memory write at {address:#x}')
        memory[address] = value & 0xFFFFFFFF
        writes.append(address)

    def value(register):
        return pc + 8 if register == 15 else registers[register]

    while pc != BASE + 0xF85D8:
        steps += 1
        if steps > 1000 or not any(BASE + lo <= pc < BASE + hi for lo, hi in ALLOWED):
            raise ValueError('Execution escaped bounded native code')
        instruction = read(pc)
        condition = instruction >> 28
        enabled = {0: zero, 1: not zero, 3: not carry, 14: True}
        if condition not in enabled:
            raise ValueError('Unsupported condition in bounded execution')
        next_pc = pc + 4
        if not enabled[condition]:
            pc = next_pc
            continue
        # BX / BLX register.
        if instruction & 0x0FFFFFF0 in (0x012FFF10, 0x012FFF30):
            next_pc = value(instruction & 15)
            if instruction & 0x0FFFFFF0 == 0x012FFF30:
                registers[14] = pc + 4
                calls.append(next_pc)
        elif instruction & 0x0E000000 == 0x0A000000:
            displacement = instruction & 0xFFFFFF
            if displacement & 0x800000:
                displacement -= 1 << 24
            next_pc = pc + 8 + displacement * 4
            if instruction & 0x01000000:
                registers[14] = pc + 4
                calls.append(next_pc)
        elif instruction & 0x0FFFFFFF == 0x092D4000:
            registers[13] -= 4
            write(registers[13], registers[14])
        elif instruction & 0x0FFFFFFF == 0x08BD8000:
            next_pc = read(registers[13])
            registers[13] += 4
        elif instruction & 0x0C000000 == 0x04000000:
            if instruction & 0x00400000 or instruction & 0x01200000 != 0x01000000:
                raise ValueError('Unsupported byte/writeback memory operation')
            base, destination = (instruction >> 16) & 15, (instruction >> 12) & 15
            displacement = instruction & 0xFFF
            if instruction & 0x02000000:
                if instruction & 0xFF0 != 0x100:
                    raise ValueError('Unsupported register addressing shift')
                displacement = value(instruction & 15) << 2
            address = value(base) + (displacement if instruction & 0x00800000 else -displacement)
            if instruction & 0x00100000:
                registers[destination] = read(address)
            else:
                write(address, value(destination))
        elif instruction & 0x0C000000 == 0:
            opcode, base, destination = (instruction >> 21) & 15, (instruction >> 16) & 15, (instruction >> 12) & 15
            operand = immediate(instruction) if instruction & 0x02000000 else value(instruction & 15)
            if not instruction & 0x02000000 and instruction & 0xFF0:
                raise ValueError('Unsupported arithmetic register shift')
            if opcode == 13:
                result = operand
            elif opcode == 4:
                result = value(base) + operand
            elif opcode in (2, 10):
                result = value(base) - operand
            else:
                raise ValueError('Unsupported arithmetic instruction')
            if instruction & 0x00100000:
                zero, carry = result == 0, value(base) >= operand
            if opcode != 10:
                registers[destination] = result & 0xFFFFFFFF
        else:
            raise ValueError(f'Unsupported opcode {instruction:08x}')
        pc = next_pc
    widgets = []
    for index, pointer in enumerate(strings):
        address = STACK + 0x98 + index * 32
        fields = [read(address + offset) for offset in range(0, 32, 4)]
        expected_next = address + 32 if index < len(strings) - 1 else 0
        if fields != [BASE + 0x16B290, expected_next, 0, 16, 64 + index * 16, pointer, 1, 0]:
            raise ValueError('Native widget fields/text/geometry/list links differ')
        widgets.append({'address': address, 'text_pointer': pointer, 'x': fields[3], 'y': fields[4]})
    if read(OWNER + 0x70) != STACK + 0x98 or registers[13] != STACK:
        raise ValueError('List head or native call stack balance differs')
    if any(STACK + 0xF8 <= address < STACK + 636 for address in writes):
        raise ValueError('Widget loop overwrote a following screen object')
    if calls != [target for _ in strings for target in (BASE + 0xFB004, BASE + 0xFAFFC, BASE + 0xFB1EC)]:
        raise ValueError('Native constructor/setter/append call sequence differs')
    return {'steps': steps, 'native_calls': calls, 'widgets': widgets,
            'stack_balanced': True, 'following_objects_untouched': True,
            'scope': 'bounded ARM execution; not wireless/gameplay runtime'}
