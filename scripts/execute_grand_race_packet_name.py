"""Execute FA5B8:FA614 name-slot selection and exact seventeen-byte copy."""

import struct

from dk4tool.patch.grand_race_waiting_widget import immediate


def execute(source, name_field, player):
    if len(name_field) != 17 or player not in range(4):
        raise ValueError('One native seventeen-byte field and valid player required')
    obj, packet = 0x1000, 0x2000
    output = bytearray(b'\xa5' * 0x200)
    incoming = bytearray(b'\x5a' * 0x34)
    incoming[0x10:0x21] = name_field
    registers = [0] * 16
    registers[0], registers[1], registers[2] = obj, player, packet
    pc, steps, zero = 0xFA5B8, 0, False
    writes = []

    def read(address, size):
        offset = address - packet
        if not 0 <= offset <= len(incoming) - size:
            raise ValueError('Packet name reads beyond initialized source')
        return int.from_bytes(incoming[offset:offset + size], 'little')

    def write(address, value, size):
        offset = address - obj
        if not 0 <= offset <= len(output) - size:
            raise ValueError('Packet name writes beyond initialized destination')
        output[offset:offset + size] = (value & ((1 << (size * 8)) - 1)).to_bytes(size, 'little')
        writes.extend(range(offset, offset + size))

    while pc != 0xFA614:
        steps += 1
        if steps > 150 or not 0xFA5B8 <= pc < 0xFA614 or pc & 3:
            raise ValueError('Execution escaped native packet-name copy')
        word = struct.unpack_from('<I', source, pc)[0]
        following = pc + 4
        if word in (0xE28040D0, 0xE2824010, 0xE2803F45, 0xE2823021):
            registers[(word >> 12) & 15] = registers[(word >> 16) & 15] + immediate(word)
        elif word & 0xFFFFF000 in (0xE3A03000, 0xE3A0E000, 0xE3A00000, 0xE3A02000):
            registers[(word >> 12) & 15] = word & 255
        elif word & 0xFFF000F0 == 0xE0200090:  # MLA Rd,Rm,Rs,Rn.
            registers[(word >> 16) & 15] = (registers[word & 15]
                                            * registers[(word >> 8) & 15]
                                            + registers[(word >> 12) & 15])
        elif word == 0xE080C101:
            registers[12] = registers[0] + (registers[1] << 2)
        elif word in (0xE5923008, 0xE592300C):
            registers[3] = read(registers[2] + (word & 0xFFF), 4)
        elif word in (0xE58C30B0, 0xE58C30C0):
            write(registers[12] + (word & 0xFFF), registers[3], 4)
        elif word in (0xE4D4C001, 0xE4D43001, 0xE5D40000):
            registers[(word >> 12) & 15] = read(registers[4], 1)
            if word != 0xE5D40000:
                registers[4] += 1
        elif word == 0xE25EE001:
            registers[14] -= 1
            zero = registers[14] == 0
        elif word in (0xE4C5C001, 0xE4C53001, 0xE5C50000):
            write(registers[5], registers[(word >> 12) & 15], 1)
            if word != 0xE5C50000:
                registers[5] += 1
        elif word >> 24 == 0x1A:
            if not zero:
                displacement = word & 0xFFFFFF
                if displacement & 0x800000:
                    displacement -= 1 << 24
                following = pc + 8 + displacement * 4
        else:
            raise ValueError(f'Unexpected native packet-name opcode {word:08X} at {pc:X}')
        pc = following
    start = 0xD0 + player * 17
    expected_writes = (list(range(0xB0 + player * 4, 0xB4 + player * 4))
                       + list(range(0xC0 + player * 4, 0xC4 + player * 4))
                       + list(range(start, start + 17)))
    if sorted(writes) != sorted(expected_writes) or output[start:start + 17] != name_field:
        raise ValueError('Native transfer changed field length, name bytes or adjacent slot')
    if any(value != 0xA5 for offset, value in enumerate(output) if offset not in writes):
        raise ValueError('Native transfer changed neighboring bytes')
    return {'player': player, 'name_field_hex': name_field.hex(), 'saved_field_hex': output[start:start + 17].hex(),
            'name_slot_offset': start, 'steps': steps,
            'terminated_at': name_field.find(b'\0'), 'exact_seventeen_bytes': True,
            'scope': 'Actual slot selection and packet name copy; incoming field validity remains a separate requirement.'}
