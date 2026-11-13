"""Research selector extension within the previously owned runtime allocations."""

import struct

from keystone import KS_ARCH_ARM, KS_MODE_THUMB, Ks

from dk4tool.patch import recruitment_editorial_runtime as bank
from dk4tool.patch import shared_dialogue_runtime as previous

SOURCE = 'daa9686528955df3e88258c5c3fc1b63adb551b08669f2a33584e3bd9d674c02'
CONTRACTS, GATE = bank.CONTRACTS, bank.GATE
# Source-bounded tail of the translated Extras tie-in introduction. The old
# scheme-name strings at C550 already contain the V626 live alignment bridge.
# Installation requires the fresh tail/reference proof in V785.
BOOM = 0x0216DEFC
CONSTANTS = GATE+164


def contract_rows():
    rows = []
    for parent, offset, high, ranges in previous.contract_rows():
        values = set(n for a, b in ranges for n in range(a, b+1))
        if parent == 0x02054014:
            values.update((*range(1070, 1073), 1074, *range(1083, 1086), 1095, 1096, 1097, 1123, 1130))
        elif parent == 0x02053FCC:
            values.update((1073, 1086))
        elif parent == 0x02053DB8:
            values.update((0x8160, 0x8140, 0x8120, 0x8100, 0x7FE0, 0x8020, 0x8040))
        elif parent == 0x02053D24:
            values.update((0x7F60, 0x80C0, 0x80A0))
        rows.append((parent, offset, high, tuple(sorted(values))))
    return rows


def table():
    result = bytearray()
    for parent, offset, high, values in contract_rows():
        shift = (4 if parent == 0x02053C14 else 5) if high else 0
        assert all(not n & ((1 << shift)-1) for n in values)
        keys = sorted((n >> shift)-512 if high else n for n in values)
        ranges = []
        for key in keys:
            if ranges and key == ranges[-1][1]+1:
                ranges[-1] = (ranges[-1][0], key)
            else:
                ranges.append((key, key))
        encoded = []
        for lo, hi in ranges:
            while lo <= hi:
                end = min(lo+31, hi)
                assert 0 <= lo <= end < 2048
                encoded.append(lo | (end-lo) << 11)
                lo = end+1
        field = (offset+24-0x180)//4
        assert high in (0, 0x0211) and (not high or field in (0x42, 0x45))
        result.extend(struct.pack('<HBB', parent & 65535, field | (128 if high else 0), len(encoded)))
        result.extend(struct.pack('<'+'H'*len(encoded), *encoded))
    assert len(result) <= 128, len(result)
    return bytes(result)+bytes(128-len(result))


def assemble():
    kt = Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    thumb = lambda text, at: bytes(kt.asm(text, at)[0])
    assembly = f'''
ldr r3,[sp,#0x27c]
ldr r4,parent_base
subs r3,r3,r4
lsrs r5,r3,#16
bne fallback
ldr r4,contracts
movs r5,#7
parents:
ldrh r6,[r4]
cmp r3,r6
beq matched
ldrb r7,[r4,#3]
lsls r7,r7,#1
adds r4,#4
adds r4,r4,r7
subs r5,#1
bne parents
b fallback
matched:
ldrb r3,[r4,#2]
lsrs r6,r3,#7
negs r6,r6
lsrs r7,r4,#16
subs r7,#3
ands r6,r7
lsls r3,r3,#25
lsrs r3,r3,#23
add r5,sp,#0x180
ldr r3,[r5,r3]
lsls r6,r6,#16
eors r3,r6
lsrs r7,r3,#16
bne fallback
cmp r6,#0
beq ready
ldrb r7,[r4,#2]
lsrs r7,r7,#1
bcs aligned32
lsls r7,r3,#28
bne fallback
lsrs r3,r3,#4
b pointer_bias
aligned32:
lsls r7,r3,#27
bne fallback
lsrs r3,r3,#5
pointer_bias:
movs r7,#2
lsls r7,r7,#8
subs r3,r3,r7
ready:
ldrb r5,[r4,#3]
adds r4,#4
ranges:
ldrh r6,[r4]
lsls r7,r6,#21
lsrs r7,r7,#21
subs r7,r3,r7
lsrs r6,r6,#11
cmp r7,r6
bls selected
adds r4,#2
subs r5,#1
bne ranges
fallback:
blx {bank.ORIGINAL_EXIT}
selected:
ldr r4,coord_ID
subs r4,r3,r4
beq coordinate
subs r4,#63
cmp r4,#1
bls status
subs r4,#123
cmp r4,#1
bls coordinate
blx {bank.LITERAL_EXIT}
coordinate:
blx {bank.COORD_EXIT}
status:
blx {bank.STATUS_EXIT}
.align 2
parent_base: .word 0x02050000
contracts: .word {CONTRACTS}
coord_ID: .word 842
'''
    gate = thumb(assembly, GATE)
    assert len(gate) == 164, len(gate)
    status = thumb(f'''
push {{r0-r7,lr}}
mov r4,r1
ldr r5,[sp,#0x2a0]
ldr r6,UI_table
movs r2,#0
find:
ldr r0,[r6,r2]
cmp r0,r5
beq found
adds r2,#4
cmp r2,#48
blo find
b done
found:
lsrs r6,r2,#1
mov r0,r5
blx 0x020ced28
mov r5,r0
mov r0,r4
blx 0x020ced28
adds r4,r4,r0
subs r4,#8
subs r4,r4,r5
cmp r6,#10
ldr r5,article
blo prefix_ready
ldr r5,prefix
prefix_ready:
ldr r7,phrases
b {bank.STATUS_TAIL}
done:
blx {bank.STATUS_RETURN}
.align 2
UI_table: .word 0x02156430
article: .word {bank.DATA_ADDRESSES[14]}
prefix: .word {bank.DATA_ADDRESSES[12]}
phrases: .word {bank.PACKED_PHRASES}
''', bank.STATUS)
    literals = (bank.DATA_ADDRESSES[13],)

    def literal(register, index, pc):
        delta = CONSTANTS+index*4-((pc+4) & ~3)
        assert 0 <= delta <= 1020 and delta % 4 == 0
        return f'ldr {register},[pc,#{delta}]'

    snippets = ['mov r0,r7', 'lsrs r0,r0,#16', 'subs r0,#1', 'lsls r0,r0,#16',
                'ldrh r7,[r7,r6]', 'lsls r7,r7,#2', 'adds r7,r7,r0', 'mov r0,r5', f'bl {bank.COPY}',
                'mov r0,r7', f'bl {bank.COPY}', ('r0', 0), f'bl {bank.COPY}', f'blx {bank.STATUS_RETURN}']
    lines, pc = [], bank.STATUS_TAIL
    for value in snippets:
        value = literal(*value, pc) if isinstance(value, tuple) else value
        lines.append(value)
        if not value.endswith(':'):
            pc += 4 if value.startswith(('bl ', 'blx ')) else 2
    tail = thumb('\n'.join(lines), bank.STATUS_TAIL)
    assert len(status) == 80 and len(tail) == 36, (len(status), len(tail))
    words = list(struct.unpack('<12H', bank.assemble()[bank.PACKED_PHRASES]))
    assert words[3]*4+bank.DATA_BASE == bank.DATA_ADDRESSES[3]
    words[3] = (BOOM-bank.DATA_BASE)//4
    return {CONTRACTS: table(), GATE: gate+struct.pack('<I', *literals),
            bank.STATUS: status, bank.STATUS_TAIL: tail,
            bank.PACKED_PHRASES: struct.pack('<12H', *words), BOOM: b'major economic boom\0'}, assembly


def code():
    return assemble()[0]
