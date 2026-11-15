"""Bounded execution of D1604 through ASCII glyph requests, not pixel painting."""

import struct

from dk4tool.patch.grand_race_waiting_widget import immediate

BASE, STACK, TEXT, XY = 0x02000000, 0x02300000, 0x02301000, 0x02302000


def execute(arm9, text, x, y, style=15):
    if not text or any(not 32 <= ord(c) <= 126 for c in text):
        raise ValueError('Complete printable ASCII selection required')
    raw = text.encode('ascii') + b'\0'
    r = [0xDEADDEAD] * 16
    r[0], r[1], r[2], r[3] = 0x02303000, 0x02304000, XY, TEXT
    r[13], r[14] = STACK, 0xFFFFFFFC
    words = {XY: x, XY + 4: y, STACK: style}
    pc, zero, carry, steps = BASE + 0xD1604, False, False, 0
    requests = []

    def read(address, byte=False):
        if byte and TEXT <= address < TEXT + len(raw):
            return raw[address - TEXT]
        if not byte and address in words:
            return words[address]
        if not byte and BASE <= address <= BASE + len(arm9) - 4 and not address & 3:
            return struct.unpack_from('<I', arm9, address - BASE)[0]
        raise ValueError(f'Uninitialized/out-of-selection read at {address:#x}')

    def write(address, value):
        if address & 3 or not STACK - 40 <= address <= STACK:
            raise ValueError('Renderer writes outside bounded stack')
        words[address] = value & 0xFFFFFFFF

    def reg(index):
        return pc + 8 if index == 15 else r[index]

    while pc != 0xFFFFFFFC:
        steps += 1
        if steps > 10000:
            raise ValueError('Native ASCII loop did not terminate')
        if pc == BASE + 0xD16B4:
            requests.append({'character': chr(read(r[13])), 'x': r[2], 'y': r[3],
                             'style': read(r[13] + 4), 'context': r[1]})
            # Actual callee body is outside this proof; caller-saved registers poisoned.
            r[0:4] = [0xDEADDEAD] * 4
            r[12] = 0xDEADDEAD
            pc = r[14]
            continue
        if not BASE + 0xD1604 <= pc < BASE + 0xD16B4 or pc & 3:
            raise ValueError('Execution escaped ASCII request loop')
        instruction = read(pc)
        enabled = {0: zero, 1: not zero, 3: not carry, 8: carry and not zero, 14: True}
        condition = instruction >> 28
        if condition not in enabled:
            raise ValueError('Unsupported native condition')
        next_pc = pc + 4
        if not enabled[condition]:
            pc = next_pc
            continue
        if instruction & 0x0E000000 == 0x08000000:
            registers = [i for i in range(16) if instruction & (1 << i)]
            if instruction & 0x0FFF0000 == 0x092D0000:
                r[13] -= len(registers) * 4
                for n, index in enumerate(registers):
                    write(r[13] + n * 4, reg(index))
            elif instruction & 0x0FFF0000 == 0x08BD0000:
                for n, index in enumerate(registers):
                    value = read(r[13] + n * 4)
                    if index == 15:
                        next_pc = value
                    else:
                        r[index] = value
                r[13] += len(registers) * 4
            else:
                raise ValueError('Unsupported block-transfer mode')
        elif instruction & 0x0E000000 == 0x0A000000:
            distance = instruction & 0xFFFFFF
            if distance & 0x800000:
                distance -= 1 << 24
            next_pc = pc + 8 + distance * 4
            if instruction & 0x01000000:
                r[14] = pc + 4
        elif instruction & 0x0C000000 == 0x04000000:
            if instruction & 0x02000000 or not instruction & 0x01000000:
                raise ValueError('Unsupported native memory mode')
            source, destination = (instruction >> 16) & 15, (instruction >> 12) & 15
            displacement = instruction & 0xFFF
            address = reg(source) + (displacement if instruction & 0x00800000 else -displacement)
            if instruction & 0x00100000:
                r[destination] = read(address, bool(instruction & 0x00400000))
            else:
                if instruction & 0x00400000:
                    raise ValueError('Unexpected native byte store')
                write(address, reg(destination))
            if instruction & 0x00200000:
                r[source] = address
        elif instruction & 0x0C000000 == 0:
            opcode, source, destination = (instruction >> 21) & 15, (instruction >> 16) & 15, (instruction >> 12) & 15
            if instruction & 0x02000000:
                operand = immediate(instruction)
            else:
                operand = reg(instruction & 15)
                shift, mode = (instruction >> 7) & 31, (instruction >> 5) & 3
                if instruction & 16 or mode == 3 or (mode == 1 and shift == 0):
                    raise ValueError('Unsupported native register shift')
                if mode == 0:
                    operand = operand << shift
                elif mode == 1:
                    operand >>= shift
                else:
                    signed = operand - (1 << 32) if operand & 0x80000000 else operand
                    operand = signed >> (shift or 32)
                operand &= 0xFFFFFFFF
            left = reg(source)
            if opcode == 0:
                value = left & operand
            elif opcode in (2, 10):
                value = left - operand
            elif opcode == 4:
                value = left + operand
            elif opcode == 13:
                value = operand
            else:
                raise ValueError('Unsupported native arithmetic opcode')
            if instruction & 0x00100000:
                zero, carry = (value & 0xFFFFFFFF) == 0, left >= operand
            if opcode != 10:
                r[destination] = value & 0xFFFFFFFF
        else:
            raise ValueError(f'Unsupported native instruction {instruction:08X}')
        pc = next_pc
    if r[13] != STACK or ''.join(row['character'] for row in requests) != text:
        raise ValueError('Native requests lose text or stack balance')
    if any(row['x'] != x + n * 6 or row['y'] != y or row['style'] != style for n, row in enumerate(requests)):
        raise ValueError('Native request positions/style differ')
    return {'requests': requests, 'steps': steps, 'stack_balanced': True,
            'scope': 'Actual D1604 ASCII loop through glyph requests; D16B4 pixel painting not executed'}
