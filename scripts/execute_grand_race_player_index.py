"""Execute the native signed player-index guard; not wireless gameplay."""

import struct


def execute_guard(arm9, index):
    if not -(1 << 31) <= index < 1 << 31:
        raise ValueError('Index must be a signed native word')
    pc, value, steps = 0xF8CB8, None, 0
    negative, overflow = False, False
    while pc not in (0xF8C64, 0xF8CCC):
        steps += 1
        if steps > 5 or not 0xF8CB8 <= pc < 0xF8CCC or pc & 3:
            raise ValueError('Guard escaped bounded native instructions')
        instruction = struct.unpack_from('<I', arm9, pc)[0]
        next_pc = pc + 4
        if instruction == 0xE59D0008:
            value = index & 0xFFFFFFFF  # Actual LDR r0,[sp,#8], initialized packet output.
        elif instruction & 0xFFFFFF00 == 0xE3500000:
            if value is None:
                raise ValueError('CMP reads an uninitialized index')
            immediate = instruction & 255
            result = (value - immediate) & 0xFFFFFFFF
            negative = bool(result & 0x80000000)
            overflow = bool(((value ^ immediate) & (value ^ result)) & 0x80000000)
        elif instruction >> 24 in (0xBA, 0xAA):
            condition = instruction >> 28
            take = negative != overflow if condition == 11 else negative == overflow
            if take:
                distance = instruction & 0xFFFFFF
                if distance & 0x800000:
                    distance -= 1 << 24
                next_pc = pc + 8 + distance * 4
        else:
            raise ValueError(f'Unsupported native guard opcode {instruction:08X}')
        pc = next_pc
    return {'index': index, 'passes_guard': pc == 0xF8CCC, 'exit_offset': pc, 'steps': steps}


def prove_guard(arm9):
    # Signed extremes plus every boundary around the four-entry table.
    cases = [execute_guard(arm9, index) for index in
             (-(1 << 31), -65536, -2, -1, 0, 1, 2, 3, 4, 5, 65535, (1 << 31) - 1)]
    if any(case['passes_guard'] != (0 <= case['index'] < 4) for case in cases):
        raise ValueError('Native guard permits an invalid four-entry table index')
    return {'status': 'pass', 'cases': cases,
            'scope': 'Actual signed guard execution; packet/network/gameplay not executed'}
