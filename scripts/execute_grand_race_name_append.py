"""Execute the native end-insertion loop through its NUL write, before drawing."""

import struct


def execute(source, name, inserted, capacity=32, *, full_return=False):
    if b'\0' in name or b'\0' in inserted or len(name) > capacity or capacity > 32:
        raise ValueError('Invalid bounded insertion inputs')
    obj, incoming = 0x1000, 0x2000
    memory = bytearray(b'\xa5' * 0xC0)
    memory[0x7C:0x7C + len(name) + 1] = name + b'\0'
    struct.pack_into('<I', memory, 0x40, len(name))  # Cursor at complete end.
    struct.pack_into('<I', memory, 0xA0, capacity)
    before = bytes(memory)
    text = inserted + b'\0'
    registers = [0xA0000000 + index for index in range(16)]
    registers[0], registers[1] = obj, incoming
    registers[13], registers[14] = 0x10000, 0xFFFFFFFC
    saved_registers = registers[:]
    stack, external_calls = {}, []
    pc, steps, difference = (0xB08D8 if full_return else 0xB08E0), 0, 0
    writes = []
    rejected = False

    def read_byte(address):
        if obj <= address < obj + len(memory):
            return memory[address - obj]
        if incoming <= address < incoming + len(text):
            return text[address - incoming]
        raise ValueError('Native insertion reads outside initialized memory')

    stops = (0xFFFFFFFC,) if full_return else (0xB0950, 0xB0A08)
    while pc not in stops:
        steps += 1
        if steps > 1000 or not (0xB08D8 <= pc < 0xB0958 or 0xB0A08 <= pc <= 0xB0A14
                                or 0xCED28 <= pc <= 0xCED4C) or pc & 3:
            raise ValueError('Execution escaped native end insertion')
        word = struct.unpack_from('<I', source, pc)[0]
        following = pc + 4
        if word == 0xE92D43F0:  # Actual seven-register caller frame.
            registers[13] -= 28
            for index, register in enumerate((4, 5, 6, 7, 8, 9, 14)):
                stack[registers[13] + index * 4] = registers[register]
        elif word == 0xE24DD004:
            registers[13] -= 4
        elif word == 0xE28DD004:
            registers[13] += 4
        elif word == 0xE8BD83F0:
            for index, register in enumerate((4, 5, 6, 7, 8, 9, 15)):
                registers[register] = stack[registers[13] + index * 4]
            registers[13] += 28
            following = registers[15]
        elif word in (0xE1A08000, 0xE1A07001, 0xE1A00008, 0xE1A00007, 0xE1A00002):
            registers[(word >> 12) & 15] = registers[word & 15]
        elif word in (0xE288607C, 0xE2866001, 0xE2855001, 0xE2822001):
            registers[(word >> 12) & 15] = registers[(word >> 16) & 15] + (word & 255)
        elif word in (0xE3A05000, 0xE3A01000, 0xE3A02000):
            registers[(word >> 12) & 15] = 0
        elif word in (0xE1D610D0, 0xE1D700D0, 0xE0D700D1, 0xE0D010D1):
            base = (word >> 16) & 15
            value = read_byte(registers[base])
            registers[(word >> 12) & 15] = value if value < 128 else value - 256
            if word in (0xE0D700D1, 0xE0D010D1):
                registers[base] += 1
        elif word in (0xE5980040, 0xE59800A0, 0xE59810A0):
            registers[(word >> 12) & 15] = struct.unpack_from('<I', memory, word & 0xFFF)[0]
        elif word == 0xE0850000:
            registers[0] += registers[5]
        elif word in (0xE3510000, 0xE3500000):
            difference = registers[(word >> 16) & 15]
        elif word in (0xE1550000, 0xE1500001):
            difference = registers[(word >> 16) & 15] - registers[word & 15]
        elif word >> 24 == 0xEB:
            displacement = word & 0xFFFFFF
            if displacement & 0x800000:
                displacement -= 1 << 24
            following = pc + 8 + displacement * 4
            if following in (0xB0B54, 0xB0C70) and full_return:
                if registers[0] != obj:
                    raise ValueError('External cursor/drawing call lost its object')
                external_calls.append({'target': following, 'object': registers[0]})
                for register in (0, 1, 2, 3, 12):
                    registers[register] = 0xDEAD0000 + register
                registers[14] = pc + 4
                following = pc + 4
            elif following != 0xCED28:
                raise ValueError('Unexpected insertion helper')
            else:
                registers[14] = pc + 4
        elif word == 0xE12FFF1E:
            following = registers[14]
        elif word >> 24 in (0xEA, 0x0A, 0x1A, 0xBA, 0xAA, 0x8A):
            condition = word >> 28
            take = {14: True, 0: difference == 0, 1: difference != 0,
                    11: difference < 0, 10: difference >= 0, 8: difference > 0}[condition]
            if take:
                displacement = word & 0xFFFFFF
                if displacement & 0x800000:
                    displacement -= 1 << 24
                following = pc + 8 + displacement * 4
                if pc == 0xB0930 and following == 0xB0A08:
                    rejected = True
        elif word == 0x14C60001 and difference == 0:
            pass
        elif word in (0xE4C60001, 0xE5C61000, 0x14C60001):
            address = registers[6] - obj
            if not 0x7C <= address <= 0x7C + capacity:
                raise ValueError('Native insertion writes beyond text capacity')
            memory[address] = registers[1 if word == 0xE5C61000 else 0] & 255
            writes.append(address - 0x7C)
            if word in (0xE4C60001, 0x14C60001):
                registers[6] += 1
        else:
            raise ValueError(f'Unsupported end-insertion opcode {word:08X} at {pc:X}')
        pc = following
    end = memory.index(0, 0x7C, 0x7C + capacity + 1) - 0x7C
    if memory[:0x7C] != before[:0x7C] or memory[0x7C + capacity + 1:] != before[0x7C + capacity + 1:]:
        raise ValueError('Native insertion changed neighboring memory')
    if full_return and (registers[13] != saved_registers[13]
                        or registers[4:12] != saved_registers[4:12]):
        raise ValueError('Native function failed to preserve stack or callee registers')
    return {'name_hex': name.hex(), 'inserted_hex': inserted.hex(), 'capacity': capacity,
            'result_hex': memory[0x7C:0x7C + end].hex(), 'terminated_at': end,
            'writes': writes, 'steps': steps, 'rejected_whole_insert': rejected or pc == 0xB0A08,
            'full_return': full_return, 'external_calls': external_calls,
            'stack_balanced': registers[13] == saved_registers[13] if full_return else None,
            'scope': 'Actual append/strlen/frame/return when enabled; cursor/drawing helpers modeled with caller-register poisoning; middle insertion excluded.'}
