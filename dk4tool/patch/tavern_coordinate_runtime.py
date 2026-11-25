"""Tavern842-only typed coordinate formatting after original printf expansion."""

import struct

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks

from dk4tool.patch import tavern_editorial_runtime as previous
from dk4tool.patch.port_services_editorial import PREFIX as PORT_PREFIX
from dk4tool.patch.shipyard_editorial import LITERAL

BASE, SOURCE = previous.BASE, previous.SOURCE
GATE, COORD = previous.GATE, previous.TYPES
TYPES, WORDS1, WORDS2 = 0x02147908, 0x02147930, 0x02147958
TYPE_HELPER, PROFESSIONS = previous.TYPE_HELPER, previous.PROFESSIONS
BANKS = (*previous.BANKS, (TYPES, TYPES + 16), (WORDS1, WORDS1 + 16), (WORDS2, WORDS2 + 24))


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
beq {previous.GIFT}
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
cmp r4,#22
beq coordinates
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
coordinates:
pop {{r3,r4,lr}}
b {COORD}
direct_parent: .word 0x02054014
yes_parent: .word 0x02053fcc
gift_parent: .word 0x02053c14
player_parent: .word 0x02053c5c
''', GATE)[0])
    assert len(gate) == 164
    # The gift helper has exact branches back into this version's gate labels.
    fallback, selected = GATE + 124, GATE + 132
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
''', previous.GIFT)[0])
    compact = bytes(ka.asm(f'''
push {{r0,r2,r3,r4,r5,lr}}
mov r4,r1
mov r5,r1
loop:
ldrb r2,[r4],#1
strb r2,[r5],#1
cmp r2,#0
beq done
cmp r2,#0x4e
cmpne r2,#0x53
cmpne r2,#0x45
cmpne r2,#0x57
bne loop
mov r3,r4
spaces:
ldrb r2,[r3],#1
cmp r2,#32
beq spaces
sub r2,r2,#48
cmp r2,#9
subls r4,r3,#1
b loop
done:
pop {{r0,r2,r3,r4,r5,lr}}
b {LITERAL}
''', COORD)[0])
    assert len(compact) == 88
    blobs = previous.assemble()
    blobs.update({GATE: gate, previous.GIFT: gift, COORD: compact,
        TYPES: struct.pack('<4I', WORDS1, WORDS1 + 7, WORDS2, WORDS2 + 8),
        WORDS1: b'trader\0pirate\0', WORDS2: b'soldier\0conqueror\0'})
    helper = bytearray(blobs[TYPE_HELPER]); struct.pack_into('<I', helper, 28, TYPES)
    blobs[TYPE_HELPER] = bytes(helper)
    return blobs
