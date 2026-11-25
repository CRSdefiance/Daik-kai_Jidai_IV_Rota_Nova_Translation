"""Execute the actual host/join seventeen-byte stored-name payload copy."""

import struct

from dk4tool.patch.grand_race_waiting_widget import immediate

PATHS = {'join': (0xF8ED8, 0xF8F00), 'host': (0xF9C48, 0xF9C70)}


def execute(source, name_field, role):
    if role not in PATHS or len(name_field) != 17:
        raise ValueError('Known sender role and seventeen-byte field required')
    start, end = PATHS[role]
    registers = [0] * 16
    registers[0], registers[10] = 0x1000, 0x2000
    output = bytearray(b'\xa5' * 0x200)
    pc, steps, zero = start, 0, False
    writes = []
    while pc != end:
        steps += 1
        if steps > 100 or not start <= pc < end or pc & 3:
            raise ValueError('Native sender escaped its copy loop')
        word = struct.unpack_from('<I', source, pc)[0]
        following = pc + 4
        if word & 0xFFFFF000 == 0xE28A4000:
            registers[4] = registers[10] + immediate(word)
        elif word & 0xFFFFFF00 == 0xE3A03000:
            registers[3] = word & 255
        elif word in (0xE4D02001, 0xE4D01001, 0xE5D00000):
            offset = registers[0] - 0x1000
            if not 0 <= offset < len(name_field):
                raise ValueError('Native sender reads beyond stored-name field')
            registers[(word >> 12) & 15] = name_field[offset]
            if word != 0xE5D00000:
                registers[0] += 1
        elif word == 0xE2533001:
            registers[3] -= 1
            zero = registers[3] == 0
        elif word in (0xE4C42001, 0xE4C41001, 0xE5C40000):
            offset = registers[4] - 0x2000
            if not 0x170 <= offset <= 0x180:
                raise ValueError('Native sender writes outside its name payload')
            output[offset] = registers[(word >> 12) & 15] & 255
            writes.append(offset)
            if word != 0xE5C40000:
                registers[4] += 1
        elif word >> 24 == 0x1A:
            if not zero:
                displacement = word & 0xFFFFFF
                if displacement & 0x800000:
                    displacement -= 1 << 24
                following = pc + 8 + displacement * 4
        else:
            raise ValueError(f'Unexpected native sender opcode {word:08X}')
        pc = following
    if writes != list(range(0x170, 0x181)) or output[0x170:0x181] != name_field:
        raise ValueError('Sender changed complete stored-name bytes or field boundary')
    if any(value != 0xA5 for offset, value in enumerate(output) if offset not in writes):
        raise ValueError('Sender changed neighboring payload bytes')
    return {'role': role, 'stored_field_hex': name_field.hex(),
            'payload_field_hex': output[0x170:0x181].hex(), 'steps': steps,
            'terminated_at': name_field.find(b'\0'),
            'scope': 'Actual stored-name payload copy; getter dispatch and network transport separate.'}
