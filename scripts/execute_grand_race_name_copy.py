"""Bounded execution of the actual stored-name population byte copier."""

import struct


def execute(arm9, name):
    if b'\0' in name or len(name) > 16:
        raise ValueError('Input must be one complete name of at most 16 bytes')
    source = name + b'\0'
    output = bytearray(b'\xa5' * 17)
    r = [0] * 4
    r[0], r[1] = 0x1000, 0x2000
    pc, zero, steps = 0xCED98, False, 0
    written = []

    def read(address):
        index = address - 0x2000
        if not 0 <= index < len(source):
            raise ValueError('Native copier reads beyond input NUL')
        byte = source[index]
        return byte if byte < 128 else byte - 256

    def write(address, value):
        index = address - 0x1000
        if not 0 <= index < 17:
            raise ValueError('Native copier writes beyond stored name field')
        output[index] = value & 255
        written.append(index)

    while steps < 150:
        steps += 1
        if not 0xCED98 <= pc < 0xCEDC8 or pc & 3:
            raise ValueError('Execution escaped the native name copier')
        instruction = struct.unpack_from('<I', arm9, pc)[0]
        next_pc = pc + 4
        if instruction in (0xE1D120D0, 0xE1F120D1):
            if instruction == 0xE1F120D1:
                r[1] += 1
            r[2] = read(r[1])
        elif instruction == 0xE1A03000:
            r[3] = r[0]
        elif instruction == 0xE3520000:
            zero = r[2] == 0
        elif instruction in (0x0A000004, 0x1AFFFFFA):
            if (instruction >> 28 == 0 and zero) or (instruction >> 28 == 1 and not zero):
                distance = instruction & 0xFFFFFF
                if distance & 0x800000:
                    distance -= 0x1000000
                next_pc = pc + 8 + distance * 4
        elif instruction == 0xE4C32001:
            write(r[3], r[2])
            r[3] += 1
        elif instruction == 0xE3A01000:
            r[1] = 0
        elif instruction == 0xE5C31000:
            write(r[3], r[1])
        elif instruction == 0xE12FFF1E:
            if output[:len(source)] != source or written != list(range(len(source))):
                raise ValueError('Native copier changed name bytes or dropped a character')
            return {'steps': steps, 'stored_hex': output.hex(), 'writes': written,
                    'leading_byte_intact': not name or output[0] == name[0],
                    'terminated_at': len(name), 'scope': 'Actual byte copier only; input length is conditional.'}
        else:
            raise ValueError(f'Unexpected native name-copy opcode at {pc:#x}')
        pc = next_pc
    raise ValueError('Native name copier exceeded execution bound')
