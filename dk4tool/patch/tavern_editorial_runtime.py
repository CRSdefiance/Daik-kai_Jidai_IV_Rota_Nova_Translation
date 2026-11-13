"""Scoped Tavern runtime resources; storage approval and release gates are external."""

import struct

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks

from dk4tool.patch.port_services_editorial import PREFIX as PORT_PREFIX
from dk4tool.patch.shipyard_editorial import DISPATCH, LITERAL

BASE = 0x02000000
SOURCE = 'f37dfc3e9690d084b68fc8412cf83eeb98b603cdb44bac03959499bb75b560d8'
GATE, GIFT = 0x0214797C, 0x02147D28
DIRECTIONS, TYPES, TYPE_HELPER = 0x02147C90, 0x02147A78, 0x02156058
BANKS = ((GATE, GATE + 168), (GIFT, GIFT + 44), (DIRECTIONS, DIRECTIONS + 72),
         (TYPES, TYPES + 88), (TYPE_HELPER, TYPE_HELPER + 40))
PROFESSIONS = (b'trader', b'pirate', b'soldier', b'conqueror')


def table_blob(base, groups):
    count = sum(map(len, groups))
    raw = bytearray(count * 4)
    for index, value in enumerate(value for group in groups for value in group):
        struct.pack_into('<I', raw, index * 4, base + len(raw))
        raw.extend(value + b'\0')
    return bytes(raw)


def assemble():
    ka = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    gate = bytes(ka.asm(f'''
push {{r3,r4,lr}}
ldr r3,[sp,#0x270]
ldr ip,direct_parent
cmp r3,ip
beq direct
ldr ip,yes_parent
cmp r3,ip
beq yes
ldr ip,gift_parent
cmp r3,ip
beq {GIFT}
ldr ip,player_parent
cmp r3,ip
bne fallback
ldr r4,[sp,#0x27c]
sub r4,r4,#0x300
cmp r4,#0x39
beq selected
b fallback
direct:
ldr r4,[sp,#0x280]
sub r4,r4,#0x300
sub r4,r4,#0x34
cmp r4,#30
bls selected
b fallback
yes:
ldr r4,[sp,#0x280]
sub r4,r4,#0x300
cmp r4,#0x47
beq selected
fallback:
pop {{r3,r4,lr}}
b {PORT_PREFIX}
selected:
pop {{r3,r4,lr}}
b {LITERAL}
direct_parent: .word 0x02054014
yes_parent: .word 0x02053fcc
gift_parent: .word 0x02053c14
player_parent: .word 0x02053c5c
''', GATE)[0])
    # Separate the small gift-table test to fit complete retired source slots.
    # GATE's fallback and selected labels precede its four literal words.
    fallback, selected = GATE + len(gate) - 32, GATE + len(gate) - 24
    gift = bytes(ka.asm(f'''
ldr r4,[sp,#0x27c]
ldr ip,table1
cmp r4,ip
beq {selected}
ldr ip,table2
cmp r4,ip
beq {selected}
b {fallback}
table1: .word 0x021166e0
table2: .word 0x02116610
''', GIFT)[0])
    helper = bytes(ka.asm(f'''
ldrb r1,[r0,#9]
cmp r1,#4
bhs original
ldr r0,table
ldr r0,[r0,r1,lsl #2]
bx lr
original: b 0x0203cf70
table: .word {TYPES}
''', TYPE_HELPER)[0])
    directions = table_blob(DIRECTIONS, ((b'north', b'south'), (b'east', b'west'), (b'a little', b'far', b'very far')))
    types = table_blob(TYPES, (PROFESSIONS,))
    lengths = (len(gate), len(gift), len(helper), len(directions), len(types))
    assert lengths == (148, 40, 32, 72, 48), lengths
    return {GATE: gate, GIFT: gift, TYPE_HELPER: helper, DIRECTIONS: directions, TYPES: types,
            DISPATCH: bytes(ka.asm(f'b {GATE}', DISPATCH)[0]),
            BASE + 0x59CC8: bytes(ka.asm(f'bl {TYPE_HELPER}', BASE + 0x59CC8)[0]),
            BASE + 0x58F08: struct.pack('<I', DIRECTIONS),
            BASE + 0x58F0C: struct.pack('<I', DIRECTIONS + 16),
            BASE + 0x58F10: struct.pack('<I', DIRECTIONS + 8)}
