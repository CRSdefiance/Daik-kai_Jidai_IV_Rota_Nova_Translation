"""Prospective no-growth runtime; ownership and release approval are separate.

All placements are documented static string tails or previously retired owned
banks. The original short UI names are preserved exactly; a separate pointer
table contains the full dialogue phrases. No ROM is emitted by this module.
"""

import struct

from keystone import KS_ARCH_ARM, KS_MODE_ARM, KS_MODE_THUMB, Ks

from dk4tool.patch import tavern_coordinate_runtime as old
from dk4tool.patch.port_services_editorial import PREFIX as PORT_PREFIX
from dk4tool.patch.region_name_boundaries import LABELS, START, END, TABLE
from dk4tool.patch.shipyard_editorial import DISPATCH, LITERAL

BASE = 0x02000000
SOURCE = 'd45104c66e5e6b4d53ef7867dac5deb9f793dd87971babf68baf7c10fd2d6f6b'
GATE, GIFT, COORD = old.GATE, old.previous.GIFT, old.COORD
BRIDGE, NEW_WORLD = 0x021478E0, 0x020F8576
PREFIX, COMPARE, CHOOSE = 0x02169F78, 0x0216A010, 0x0216A05C
UNWIND, QUEUE, QUEUE_TABLE = old.TYPE_HELPER + 32, 0x0216A0B0, 0x0216A074
REGION, REGION_LOAD, REGION_END = 0x02169F3C, 0x02169FA8, 0x0216A110
NORTH, MEDITERRANEAN, INDIAN = 0x02147A58, 0x0216DC80, 0x02143D60
REGION_TABLE = BASE + START + 52
AFRICA, SOUTHEAST, EAST = 0x0215D2CD, 0x02137AA8, 0x0216B012
TAILS = ((PREFIX, PREFIX+12), (COMPARE, COMPARE+12), (CHOOSE, CHOOSE+12),
    (QUEUE, QUEUE+24), (QUEUE_TABLE, QUEUE_TABLE+8), (REGION, REGION+12),
    (REGION_LOAD,REGION_LOAD+8),(REGION_END, REGION_END+12),
    (MEDITERRANEAN, MEDITERRANEAN+19), (INDIAN, INDIAN+24))


def assemble(arm):
    ka, kt = Ks(KS_ARCH_ARM, KS_MODE_ARM), Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    def a(code, at): return bytes(ka.asm(code, at)[0])
    blobs = {}
    # Exactly one extra ARM instruction fits the existing168-byte gate. This
    # conditional interworking jump uses the nearby retired8-byte source slot.
    gift_delta = GATE + 48 - (BRIDGE + 1)
    gate = a(f'''
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
subeq ip,pc,#{gift_delta}
bxeq ip
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
cmp r4,#62
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
''', GATE)
    assert len(gate) == 168
    fallback, selected = GATE+128, GATE+136
    gift = bytes(kt.asm(f'''
ldr r4,[sp,#0x27c]
ldr r3,base
subs r4,r4,r3
beq selected
cmp r4,#0xd0
beq selected
cmp r4,#0xe0
beq selected
movs r3,#1
lsls r3,r3,#9
cmp r4,r3
beq selected
ldr r3,fallback_ptr
bx r3
selected:
ldr r3,selected_ptr
bx r3
.align 2
base: .word 0x02116610
fallback_ptr: .word {fallback}
selected_ptr: .word {selected}
''', GIFT)[0])
    assert len(gift) == 44
    blobs[GATE], blobs[GIFT] = gate, gift
    blobs[BRIDGE] = bytes(kt.asm(f'b {GIFT}', BRIDGE)[0])
    assert len(blobs[BRIDGE]) == 2
    blobs[DISPATCH] = a(f'b {PREFIX}', DISPATCH)
    blobs[PREFIX] = a(f'push {{r3,r4,lr}}; ldr r3,[sp,#0x270]; b {COMPARE}', PREFIX)
    blobs[COMPARE] = a(f'ldr ip,[pc,#{CHOOSE+8-(COMPARE+8)}]; cmp r3,ip; b {CHOOSE}', COMPARE)
    blobs[CHOOSE] = a(f'beq {QUEUE}; b {UNWIND}; .word 0x02053d24', CHOOSE)
    blobs[UNWIND] = a(f'pop {{r3,r4,lr}}; b {GATE}', UNWIND)
    blobs[QUEUE_TABLE] = struct.pack('<I',0x02118400)
    blobs[QUEUE] = a(f'''
ldr r4,[sp,#0x288]
ldr ip,[pc,#{QUEUE_TABLE-(QUEUE+4+8)}]
cmp r4,ip
bne {UNWIND}
pop {{r3,r4,lr}}
b {LITERAL}
''',QUEUE)
    assert [len(blobs[p]) for p in (PREFIX,COMPARE,CHOOSE,UNWIND,QUEUE)] == [12,12,12,8,24]
    blobs[REGION] = a(f'cmp r0,#7; bhs 0x020945b4; b {REGION_LOAD}',REGION)
    blobs[REGION_LOAD] = a(f'ldr r1,[pc,#{REGION_END+8-(REGION_LOAD+8)}]; b {REGION_END}',REGION_LOAD)
    blobs[REGION_END] = a('add r0,r1,r0,lsl #2; bx lr',REGION_END)
    blobs[REGION_END+8] = struct.pack('<I',REGION_TABLE)
    assert len(blobs[REGION]) == 12 and len(blobs[REGION_LOAD]) == len(blobs[REGION_END]) == 8
    blobs[NORTH] = b'the North Sea\0'
    blobs[MEDITERRANEAN] = b'the Mediterranean\0'
    blobs[INDIAN] = b'the Indian Ocean\0'
    # Seven unchanged UI names packed in their previously owned80-byte region
    # allocation. The identical active Africa string is shared by pointer only.
    payload = bytearray(); ui_fields = []
    for i in sorted(range(8), key=lambda i: struct.unpack_from('<I',arm,TABLE+i*52)[0]):
        if i == 2: pointer = AFRICA
        else:
            pointer = BASE+START+len(payload)
            payload.extend(LABELS[i].encode('ascii')+b'\0')
        ui_fields.append((BASE+TABLE+i*52,struct.pack('<I',pointer)))
    assert len(payload) == 51
    payload.append(0)
    payload.extend(struct.pack('<7I',NORTH,MEDITERRANEAN,AFRICA,INDIAN,SOUTHEAST,EAST,NEW_WORLD))
    assert len(payload) == END-START == 80
    blobs[BASE+START] = bytes(payload)
    blobs.update(ui_fields)
    # Precisely two original region-provider call sites and two argument moves.
    # Full caller execution and preservation are verified separately.
    for address in (0x020582BC,0x02059968):
        blobs[address] = a(f'bl {REGION}',address)
    blobs[0x02058070] = a('mov r3,r0',0x02058070)
    blobs[0x02058078] = a('mov r2,r6',0x02058078)
    return blobs


def load_into_cpu(u, arm):
    blobs = assemble(arm)
    for at,blob in blobs.items():u.mem_write(at,blob)
    return blobs
