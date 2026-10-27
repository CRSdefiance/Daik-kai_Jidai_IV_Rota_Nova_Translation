"""Research-only ARM rewrite for a third wireless waiting text widget.

The caller must lock the complete original function before using this rewrite.
It neither allocates strings nor writes a ROM. No release integration is implied.
"""

import struct

START, END = 0xF848C, 0xF89BC
INIT_START, INIT_END = 0xF8508, 0xF8584
OLD_FRAME, NEW_FRAME = 0x25C, 0x27C
SHIFT_START, SHIFT = 0xD8, 0x20


def ror(value, count):
    count %= 32
    return ((value >> count) | (value << ((32 - count) % 32))) & 0xFFFFFFFF


def immediate(word):
    return ror(word & 255, ((word >> 8) & 15) * 2)


def encode_immediate(value):
    for rotation in range(16):
        byte = ror(value, 32 - rotation * 2)
        if byte <= 255 and ror(byte, rotation * 2) == value:
            return rotation << 8 | byte
    raise ValueError(f'Unencodable ARM immediate: {value:#x}')


def pc_load(offset, register, literal):
    distance = literal - offset - 8
    if not 0 <= distance <= 0xFFF:
        raise ValueError('Literal is outside positive ARM LDR range')
    return 0xE59F0000 | register << 12 | distance


def initializer():
    # r9 remains zero until the native constructor loop increments it.
    words = [pc_load(INIT_START, 1, 0xF89CC), 0xE28D2098, 0xE3A03003,
             0xE5821000, 0xE5829004, 0xE5829008, 0xE582901C,
             0xE2822020, 0xE2533001, 0x1AFFFFF8]
    offset = INIT_START + 4 * len(words)
    words.extend([pc_load(offset, 0, 0xF89D8), 0xE5901000, 0xE5900004,
                  pc_load(offset + 12, 6, 0xF89DC)])
    words.extend([0xE1A00000] * ((INIT_END - INIT_START) // 4 - len(words)))
    return words


def rewrite_function(arm9):
    """Return a same-length research ARM9 and every changed instruction.

    Relocate stack references across the *entire* function, including conditional
    returns. Unsupported explicit SP forms fail rather than silently escaping.
    The string table literal is left alone for a later owned allocation.
    """
    out = bytearray(arm9)
    changes = []
    frame_count = 0
    for offset in range(START, END, 4):
        old = struct.unpack_from('<I', arm9, offset)[0]
        new = old
        if INIT_START <= offset < INIT_END:
            new = initializer()[(offset - INIT_START) // 4]
            reason = 'initialize three complete linked text widgets'
        elif offset == 0xF85CC:
            if old != 0xE3590002:
                raise ValueError('Original text loop count differs')
            new = 0xE3590003
            reason = 'construct and append three text widgets'
        elif old & 0x0E000000 == 0x02000000 and (old >> 16) & 15 == 13:
            opcode, destination = (old >> 21) & 15, (old >> 12) & 15
            value = immediate(old)
            if opcode not in (2, 4) or old & 0x00100000:
                raise ValueError(f'Unsupported SP arithmetic at {offset:#x}')
            if destination == 13:
                if value != OLD_FRAME:
                    raise ValueError('Unexpected stack frame adjustment')
                new = old & ~0xFFF | encode_immediate(NEW_FRAME)
                frame_count += 1
                reason = 'preserve entry/return stack balance'
            elif opcode == 4 and value >= SHIFT_START:
                if value >= OLD_FRAME:
                    raise ValueError('Stack pointer escapes original frame')
                new = old & ~0xFFF | encode_immediate(value + SHIFT)
                reason = 'move object after added text widget'
        elif old & 0x0C000000 == 0x04000000 and (old >> 16) & 15 == 13:
            if old & 0x02000000 or old & 0x01200000 != 0x01000000 or not old & 0x00800000:
                raise ValueError(f'Unsupported SP memory access at {offset:#x}')
            value = old & 0xFFF
            if value >= SHIFT_START:
                if value >= OLD_FRAME:
                    raise ValueError('Stack access escapes original frame')
                new = old & ~0xFFF | (value + SHIFT)
                reason = 'move field after added text widget'
        elif old & 0x0E000000 == 0x08000000 and (old >> 16) & 15 == 13:
            # Only the pinned function prologue and conditional epilogues use it.
            if old & 0xFFFF not in (0x4FF0, 0x8FF0):
                raise ValueError('Unexpected stack register transfer')
        elif old & 0x0C000000 == 0 and (old >> 16) & 15 == 13:
            raise ValueError(f'Unclassified explicit SP instruction at {offset:#x}')
        if new != old:
            struct.pack_into('<I', out, offset, new)
            changes.append({'offset': offset, 'old': f'{old:08x}', 'new': f'{new:08x}',
                            'reason': reason})
    if frame_count < 2:
        raise ValueError('Missing frame entry or return adjustments')
    return bytes(out), changes
