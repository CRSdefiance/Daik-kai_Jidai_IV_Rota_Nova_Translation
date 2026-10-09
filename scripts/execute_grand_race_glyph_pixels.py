"""Execute native 16-bit/4-bit glyph loops in a bounded synthetic framebuffer."""

import struct

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm import ARM_OP_IMM, ARM_OP_REG

GLYPH, BUFFER, STACK = 0x1000, 0x2000, 0x3000


def execute(arm9, rows, *, mode, x=0, pitch=16, style=3, background=9):
    if len(rows) != 11 or mode not in (16, 4) or not 0 <= x <= pitch * (4 if mode == 4 else 1) - 6:
        raise ValueError('Invalid native glyph/format/stride bounds')
    if not 0 <= style < (16 if mode == 4 else 65536):
        raise ValueError('Invalid pixel style')
    data = bytearray()
    for _ in range(pitch * 11):
        data.extend(struct.pack('<H', background if mode == 16 else background * 0x1111))
    r = [0xDEADDEAD] * 16
    r[13] = STACK
    words = {STACK: pitch, STACK + 4: (x & 3) * 4, STACK + 8: 0}
    if mode == 16:
        r[0], r[1], r[4], r[6], r[7], r[10] = pitch, 0, 0, 0, GLYPH, style
        r[11] = BUFFER + x * 2
        start, end = 0xD1718, 0xD1758
    else:
        r[0], r[1], r[4], r[5], r[10] = 0, style, 0, GLYPH, 0
        r[11] = BUFFER + (x >> 2) * 2
        start, end = 0xD17A4, 0xD1814
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    instructions = {i.address: i for i in decoder.disasm(arm9[start:end], start)}
    aliases = {'sb': 9, 'sl': 10, 'fp': 11, 'ip': 12, 'sp': 13, 'lr': 14, 'pc': 15}
    pc, zero, negative, overflow, steps, writes = start, False, False, False, 0, 0

    def register(insn, identity):
        name = insn.reg_name(identity)
        return aliases[name] if name in aliases else int(name.removeprefix('r'))

    def value(insn, operand):
        if operand.type == ARM_OP_IMM:
            return operand.imm
        if operand.type != ARM_OP_REG:
            raise ValueError('Unsupported pixel operand')
        result = r[register(insn, operand.reg)]
        if operand.shift.type:
            # Native shifted operands here are register-controlled LSL only.
            if operand.shift.type not in (2, 7):
                raise ValueError('Unsupported native pixel operand shift')
            count = operand.shift.value if operand.shift.type == 2 else r[register(insn, operand.shift.value)] & 255
            result <<= count
        return result & 0xFFFFFFFF

    def address(insn, operand):
        memory = operand.mem
        if memory.index:
            raise ValueError('Unexpected indexed pixel memory operand')
        return r[register(insn, memory.base)] + memory.disp

    while pc != end:
        steps += 1
        if steps > 3000 or pc not in instructions:
            raise ValueError('Pixel loop escaped bounded code')
        insn = instructions[pc]
        word = struct.unpack_from('<I', arm9, pc)[0]
        condition = word >> 28
        enabled = {1: not zero, 10: negative == overflow, 11: negative != overflow, 14: True}
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
        if mnemonic == 'b':
            next_pc = operands[0].imm
        elif mnemonic in ('ldrb', 'ldrh', 'ldr', 'strh'):
            destination = register(insn, operands[0].reg)
            target = address(insn, operands[1])
            if mnemonic == 'ldrb' and GLYPH <= target < GLYPH + 11:
                r[destination] = rows[target - GLYPH]
            elif mnemonic == 'ldr' and target in words:
                r[destination] = words[target]
            elif mnemonic in ('ldrh', 'strh') and BUFFER <= target <= BUFFER + len(data) - 2 and not target & 1:
                if mnemonic == 'ldrh':
                    r[destination] = struct.unpack_from('<H', data, target - BUFFER)[0]
                else:
                    struct.pack_into('<H', data, target - BUFFER, r[destination] & 65535)
                    writes += 1
            else:
                raise ValueError('Native pixel read/write escapes initialized buffers')
        elif mnemonic in ('mov', 'mvn', 'add', 'and', 'ands', 'orr', 'asr', 'cmp'):
            args = [value(insn, operand) for operand in operands[1:]]
            if mnemonic == 'cmp':
                left, right = value(insn, operands[0]), args[0]
                result = (left - right) & 0xFFFFFFFF
                zero, negative = result == 0, bool(result & 0x80000000)
                overflow = bool(((left ^ right) & (left ^ result)) & 0x80000000)
            else:
                destination = register(insn, operands[0].reg)
                if mnemonic == 'mov':
                    result = args[0]
                elif mnemonic == 'mvn':
                    result = ~args[0]
                elif mnemonic == 'add':
                    result = args[0] + args[1]
                elif mnemonic in ('and', 'ands'):
                    result = args[0] & args[1]
                elif mnemonic == 'orr':
                    result = args[0] | args[1]
                else:
                    signed = args[0] - (1 << 32) if args[0] & 0x80000000 else args[0]
                    result = signed >> args[1]
                r[destination] = result & 0xFFFFFFFF
                if mnemonic == 'ands':
                    zero, negative = result == 0, bool(result & 0x80000000)
        else:
            raise ValueError(f'Unsupported native pixel instruction: {insn.mnemonic}')
        pc = next_pc
    width = pitch * (4 if mode == 4 else 1)
    pixels = []
    for y in range(11):
        line = []
        for column in range(width):
            offset = y * pitch * 2 + (column * 2 if mode == 16 else (column >> 2) * 2)
            packed = struct.unpack_from('<H', data, offset)[0]
            line.append(packed if mode == 16 else (packed >> ((column & 3) * 4)) & 15)
        pixels.append(line)
    return {'pixels': pixels, 'steps': steps, 'writes': writes,
            'scope': 'Native glyph loop; synthetic initialized framebuffer, not actual screen routing'}
