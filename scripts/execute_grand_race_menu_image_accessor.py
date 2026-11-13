"""Bounded native execution of the adjusted menu image accessor."""

import struct

BASE, OWNER = 0x02000000, 0x02300000


def execute_raster_dispatch(arm9):
    """Execute the actual four-instruction owner-to-rasterizer handoff."""
    registers = [0] * 16
    registers[4] = OWNER
    memory = {OWNER: BASE + 0x1409E4}
    for offset in range(0xAD620, 0xAD630, 4):
        instruction = struct.unpack_from('<I', arm9, offset)[0]
        if instruction == 0xE1A00004:
            registers[0] = registers[4]
        elif instruction in (0xE5901000, 0xE591104C):
            base = (instruction >> 16) & 15
            address = registers[base] + (instruction & 0xFFF)
            if address in memory:
                registers[1] = memory[address]
            elif BASE <= address < BASE + len(arm9) - 3:
                registers[1] = struct.unpack_from('<I', arm9, address - BASE)[0]
            else:
                raise ValueError('Dispatch reads outside the initialized owner')
        elif instruction == 0xE12FFF31:
            if registers[0] != OWNER or registers[1] != BASE + 0xACB10:
                raise ValueError('Raster dispatch lost owner or selects wrong callback')
            return {'callback': registers[1], 'this_pointer': registers[0],
                    'text_buffer_pointer': registers[0] + 0x68,
                    'scope': 'actual owner handoff; rasterizer body not executed'}
        else:
            raise ValueError('Unexpected native raster handoff opcode')
    raise ValueError('Native raster callback was not invoked')


def execute(arm9, *, state=0, normal=0, selected=0):
    memory = {OWNER + 0xAC: BASE + 0x140AC4,
              OWNER + 0x44: normal, OWNER + 0x48: selected, OWNER + 0x4C: state}
    registers = [0] * 16
    registers[0] = OWNER + 0xAC
    pc, zero, steps = BASE + 0x163D8, False, 0

    def read(address):
        if address in memory:
            return memory[address]
        if BASE <= address < BASE + len(arm9) - 3 and address % 4 == 0:
            return struct.unpack_from('<I', arm9, address - BASE)[0]
        raise ValueError('Accessor read outside initialized native objects')

    while True:
        steps += 1
        if steps > 40 or not (BASE + 0x163D8 <= pc < BASE + 0x163E8 or BASE + 0xAD734 <= pc < BASE + 0xAD76C):
            raise ValueError('Image accessor escaped bounded native code')
        instruction = read(pc)
        condition = instruction >> 28
        if condition not in (0, 1, 14):
            raise ValueError('Unknown accessor condition')
        enabled = condition == 14 or (condition == 0 and zero) or (condition == 1 and not zero)
        next_pc = pc + 4
        if not enabled:
            pc = next_pc
            continue
        if instruction == 0xE12FFF1E:
            return {'steps': steps, 'returned_image_pointer': registers[0],
                    'owner_pointer': OWNER, 'input_subobject_pointer': OWNER + 0xAC,
                    'scope': 'bounded native property execution; not raster/paint execution'}
        if instruction & 0x0F000000 == 0x0A000000:
            distance = instruction & 0xFFFFFF
            if distance & 0x800000:
                distance -= 1 << 24
            next_pc = pc + 8 + distance * 4
        elif instruction & 0x0C000000 == 0x04000000:
            if instruction & 0x02200000 or not instruction & 0x01100000 == 0x01100000:
                raise ValueError('Unsupported accessor memory opcode')
            base, destination = (instruction >> 16) & 15, (instruction >> 12) & 15
            offset = instruction & 0xFFF
            address = registers[base] + (offset if instruction & 0x00800000 else -offset)
            registers[destination] = read(address)
        elif instruction & 0x0C000000 == 0:
            opcode, base, destination = (instruction >> 21) & 15, (instruction >> 16) & 15, (instruction >> 12) & 15
            operand = instruction & 255 if instruction & 0x02000000 else registers[instruction & 15]
            if instruction & (0xF00 if instruction & 0x02000000 else 0xFF0):
                raise ValueError('Unsupported shifted accessor arithmetic')
            if opcode == 10:
                zero = registers[base] == operand
            elif opcode == 4:
                registers[destination] = (registers[base] + operand) & 0xFFFFFFFF
            elif opcode == 13:
                registers[destination] = operand
            else:
                raise ValueError('Unsupported accessor arithmetic opcode')
        else:
            raise ValueError('Unknown accessor opcode')
        pc = next_pc
