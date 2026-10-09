"""Execute native glyph painter entry with a bounded external copy contract."""

import struct

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm import ARM_OP_IMM, ARM_OP_REG

BASE, CONTEXT, BUFFER, STACK = 0x02000000, 0x1000, 0x2000, 0x100000


def execute(arm9, character, *, mode, x=0, y=0, pitch=16, style=3, background=9):
    if len(character) != 1 or not 32 <= ord(character) <= 126 or mode not in (16, 4):
        raise ValueError('Invalid printable glyph or pixel format')
    if x < 0 or x + 6 > pitch * (4 if mode == 4 else 1) or not 0 <= y < 192 or not 0 <= style < 16:
        raise ValueError('Invalid native context bounds')
    data = bytearray()
    for _ in range(pitch * (11 + y)):
        data.extend(struct.pack('<H', background if mode == 16 else background * 0x1111))
    r = [0xDEADDEAD] * 16
    r[0], r[1], r[2], r[3], r[13], r[14] = 0x5000, CONTEXT, x, y, STACK, 0xFFFFFFFC
    memory = {}
    def store(address, value, size):
        for index in range(size):
            memory[address + index] = (value >> (index * 8)) & 255
    store(CONTEXT, mode, 4)
    store(CONTEXT + 4, pitch, 4)
    store(CONTEXT + 16, BUFFER - CONTEXT, 4)
    store(STACK, ord(character), 4)
    store(STACK + 4, style, 4)
    start, end = 0xD16B4, 0xD1894
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    instructions = {i.address: i for i in decoder.disasm(arm9[start:end], start)}
    aliases = {'sb': 9, 'sl': 10, 'fp': 11, 'ip': 12, 'sp': 13, 'lr': 14, 'pc': 15}
    pc, zero, negative, overflow, carry, steps, writes = start, False, False, False, False, 0, 0
    copy_calls = []

    def register(insn, identity):
        name = insn.reg_name(identity)
        return aliases[name] if name in aliases else int(name.removeprefix('r'))

    def value(insn, operand):
        if operand.type == ARM_OP_IMM:
            return operand.imm
        if operand.type != ARM_OP_REG:
            raise ValueError('Unsupported pixel operand')
        identity = register(insn, operand.reg)
        result = pc + 8 if identity == 15 else r[identity]
        if operand.shift.type:
            # Native shifted operands here are register-controlled LSL only.
            if operand.shift.type not in (1, 2, 7):
                raise ValueError('Unsupported native pixel operand shift')
            count = operand.shift.value if operand.shift.type in (1, 2) else r[register(insn, operand.shift.value)] & 255
            if operand.shift.type == 1:
                result = (result - (1 << 32) if result & 0x80000000 else result) >> count
            else:
                result <<= count
        return result & 0xFFFFFFFF

    def address(insn, operand):
        memory = operand.mem
        identity = register(insn, memory.base)
        return (pc + 8 if identity == 15 else r[identity]) + memory.disp + (r[register(insn, memory.index)] if memory.index else 0)

    def read(address, size):
        if BUFFER <= address <= BUFFER + len(data) - size:
            return int.from_bytes(data[address - BUFFER:address - BUFFER + size], 'little')
        if all(address + i in memory for i in range(size)):
            return sum(memory[address + i] << (i * 8) for i in range(size))
        offset = address - BASE if address >= BASE else address
        if 0 <= offset <= len(arm9) - size:
            return int.from_bytes(arm9[offset:offset + size], 'little')
        raise ValueError('Uninitialized painter read')

    while pc != 0xFFFFFFFC:
        if pc == 0xE2A5C:
            # External memcpy contract; native helper body is not executed here.
            if r[2] != 11 or not STACK - 64 <= r[1] < STACK or not BASE + 0x125A60 <= r[0] < BASE + 0x125E75:
                raise ValueError('Unexpected glyph-copy contract')
            copy_calls.append({'source': r[0], 'destination': r[1], 'bytes': r[2]})
            for index in range(11):
                store(r[1] + index, read(r[0] + index, 1), 1)
            pc = r[14]
            continue
        steps += 1
        if steps > 3000 or pc not in instructions:
            raise ValueError('Pixel loop escaped bounded code')
        insn = instructions[pc]
        word = struct.unpack_from('<I', arm9, pc)[0]
        condition = word >> 28
        enabled = {0: zero, 1: not zero, 3: not carry, 8: carry and not zero, 10: negative == overflow, 11: negative != overflow, 14: True}
        if condition not in enabled:
            raise ValueError('Unexpected pixel condition')
        next_pc = pc + 4
        if not enabled[condition]:
            pc = next_pc
            continue
        mnemonic = insn.mnemonic
        if condition != 14:
            mnemonic = mnemonic[:-2]
        operands = insn.operands
        if mnemonic in ('push', 'pop'):
            identities = [register(insn, operand.reg) for operand in operands]
            if mnemonic == 'push':
                r[13] -= len(identities) * 4
                for index, identity in enumerate(identities):
                    store(r[13] + index * 4, r[identity], 4)
            else:
                values = [read(r[13] + index * 4, 4) for index in range(len(identities))]
                r[13] += len(identities) * 4
                for identity, result in zip(identities, values):
                    if identity == 15:
                        next_pc = result
                    else:
                        r[identity] = result
        elif mnemonic in ('b', 'bl'):
            if mnemonic == 'bl':
                r[14] = pc + 4
            next_pc = operands[0].imm
        elif mnemonic in ('ldrb', 'ldrh', 'ldr', 'str', 'strh', 'strb'):
            destination = register(insn, operands[0].reg)
            target = address(insn, operands[1])
            size = 1 if mnemonic.endswith('b') else 2 if mnemonic.endswith('h') else 4
            if mnemonic.startswith('ldr'):
                r[destination] = read(target, size)
            elif BUFFER <= target <= BUFFER + len(data) - size:
                data[target - BUFFER:target - BUFFER + size] = (r[destination] & ((1 << (8 * size)) - 1)).to_bytes(size, 'little')
                writes += 1
            elif STACK - 80 <= target <= STACK + 4:
                store(target, r[destination], size)
            else:
                raise ValueError(f'Native painter write outside initialized buffers: pc={pc:#x}, target={target:#x}')
        elif mnemonic in ('mov', 'mvn', 'add', 'sub', 'and', 'ands', 'orr', 'asr', 'lsl', 'cmp', 'mul', 'mla'):
            args = [value(insn, operand) for operand in operands[1:]]
            if mnemonic == 'cmp':
                left, right = value(insn, operands[0]), args[0]
                result = (left - right) & 0xFFFFFFFF
                zero, negative = result == 0, bool(result & 0x80000000)
                overflow = bool(((left ^ right) & (left ^ result)) & 0x80000000)
                carry = left >= right
            else:
                destination = register(insn, operands[0].reg)
                if mnemonic == 'mov':
                    result = args[0]
                elif mnemonic == 'mvn':
                    result = ~args[0]
                elif mnemonic == 'add':
                    result = args[0] + args[1]
                elif mnemonic == 'sub':
                    result = args[0] - args[1]
                elif mnemonic == 'mul':
                    result = args[0] * args[1]
                elif mnemonic == 'mla':
                    result = args[0] * args[1] + args[2]
                elif mnemonic == 'lsl':
                    result = args[0] if len(args) == 1 else args[0] << args[1]
                elif mnemonic in ('and', 'ands'):
                    result = args[0] & args[1]
                elif mnemonic == 'orr':
                    result = args[0] | args[1]
                else:
                    signed = args[0] - (1 << 32) if args[0] & 0x80000000 else args[0]
                    result = args[0] if len(args) == 1 else signed >> args[1]
                r[destination] = result & 0xFFFFFFFF
                if mnemonic == 'ands':
                    zero, negative = result == 0, bool(result & 0x80000000)
        else:
            raise ValueError(f'Unsupported native pixel instruction: {insn.mnemonic}')
        pc = next_pc
    if r[13] != STACK:
        raise ValueError('Painter stack is not balanced')
    width = pitch * (4 if mode == 4 else 1)
    pixels = []
    for row_index in range(11 + y):
        line = []
        for column in range(width):
            offset = row_index * pitch * 2 + (column * 2 if mode == 16 else (column >> 2) * 2)
            packed = struct.unpack_from('<H', data, offset)[0]
            line.append(packed if mode == 16 else (packed >> ((column & 3) * 4)) & 15)
        pixels.append(line)
    return {'pixels': pixels, 'steps': steps, 'writes': writes,
            'copy_calls': copy_calls, 'stack_balanced': True,
            'scope': 'Native painter entry/resolver/both pixel loops; synthetic context and external memcpy contract'}
