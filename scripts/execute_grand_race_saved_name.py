"""Execute native name save/load loops with explicit successful byte-I/O contracts."""

import struct

PATHS = {'save': (0x830B0, 0x830D8, 0x46BE0),
         'load': (0x82FB8, 0x82FE0, 0x469DC)}


def execute(source, field, mode):
    if mode not in PATHS or len(field) != 17:
        raise ValueError('Native seventeen-byte save field and known mode required')
    start, end, helper = PATHS[mode]
    if struct.unpack_from('<I', source, helper + 0x14)[0] != 0xE3A02001:
        raise ValueError('Native storage wrapper no longer requests one byte')
    registers = [0] * 16
    registers[4], registers[5] = 0x7000, 0x1000
    output, calls = bytearray(), []
    pc, steps, difference = start, 0, 0
    while pc != end:
        steps += 1
        if steps > 200 or not start <= pc < end or pc & 3:
            raise ValueError('Native saved-name loop escaped')
        word = struct.unpack_from('<I', source, pc)[0]
        following = pc + 4
        if word == 0xE3A08000:
            registers[8] = 0
        elif word in (0xE1A06008, 0xE1A00004, 0xE1A02006):
            registers[(word >> 12) & 15] = registers[word & 15]
        elif word in (0xE2857020, 0xE2888001):
            registers[(word >> 12) & 15] = registers[(word >> 16) & 15] + (word & 255)
        elif word == 0xE0871008:
            registers[1] = registers[7] + registers[8]
        elif word >> 24 == 0xEB:
            displacement = word & 0xFFFFFF
            if displacement & 0x800000:
                displacement -= 1 << 24
            target = pc + 8 + displacement * 4
            offset = registers[1] - 0x1020
            if target != helper or registers[0] != 0x7000 or registers[2] != 0 or offset != len(calls):
                raise ValueError('Unexpected storage call or field address')
            if not 0 <= offset < 17:
                raise ValueError('Native storage reads or writes past the complete name field')
            calls.append({'target': helper, 'field_byte': offset, 'request_bytes': 1})
            output.append(field[offset])
            for register in (0, 1, 2, 3, 12):
                registers[register] = 0xDEAD0000 + register
        elif word & 0xFFFFFF00 == 0xE3580000:
            difference = registers[8] - (word & 255)
        elif word >> 24 == 0xDA:
            if difference <= 0:
                displacement = word & 0xFFFFFF
                if displacement & 0x800000:
                    displacement -= 1 << 24
                following = pc + 8 + displacement * 4
        else:
            raise ValueError(f'Unexpected saved-name opcode {word:08X}')
        pc = following
    if output != field or len(calls) != 17:
        raise ValueError('Native save/load omitted field bytes or the final terminator')
    return {'mode': mode, 'field_hex': field.hex(), 'output_hex': output.hex(),
            'steps': steps, 'calls': calls,
            'scope': 'Actual seventeen-iteration caller loop; byte-I/O helper bodies/physical saves modeled as successful contracts.'}
