"""Exact-key scheme routing in the existing private dispatcher allocations."""

import struct
from keystone import KS_ARCH_ARM,KS_MODE_THUMB,Ks
from dk4tool.patch import recruitment_editorial_runtime as prior

SOURCE='9e54d5456e1de352c2cdf574a8cca5bcb93fbbbd0414fdb38b627b1278617d92'
NEW_NARRATION=(0x7B40,0x82C0,0x8300,0x8320,0x8340)
NEW_CONFIRM=(0x8260,0x8280,0x82A0)

def contract_rows():
    rows=[]
    for parent,offset,high,ranges in prior.CONTRACT_ROWS:
        values=list(ranges)
        if parent==0x02053DB8:values.extend((n,n) for n in NEW_NARRATION)
        if parent==0x02053D24:values.extend((n,n) for n in NEW_CONFIRM)
        rows.append((parent,offset,high,tuple(sorted(values))))
    return rows

def assemble():
    table=bytearray()
    for parent,offset,high,ranges in contract_rows():
        field=(offset+24-0x180)//4
        assert 0<=field<128 and high in (0,0x0211)
        encoded=[]
        for lo,hi in ranges:
            if high:
                assert lo==hi and not(lo&15)
                encoded.append(lo>>4)
            else:
                while lo<=hi:
                    end=min(lo+15,hi)
                    assert 0<=lo<=end<4096
                    encoded.append(lo|((end-lo)<<12))
                    lo=end+1
        table.extend(struct.pack('<HBB',parent&65535,field|(128 if high else 0),len(encoded)))
        table.extend(struct.pack('<'+'H'*len(encoded),*encoded))
    assert len(table)==100
    # Every item packs a12-bit low key and4-bit interval delta. Exact pointer
    # keys are divided by16 only after rejecting every unaligned low nibble.
    assembly=f'''
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
ldr r7,field_high
ands r6,r7
lsls r3,r3,#25
lsrs r3,r3,#23
add r5,sp,#0x180
ldr r3,[r5,r3]
lsrs r7,r3,#16
cmp r6,r7
bne fallback
lsls r3,r3,#16
lsrs r3,r3,#16
ldrb r5,[r4,#3]
adds r4,#4
cmp r6,#0
beq ranges
lsls r7,r3,#28
bne fallback
lsrs r3,r3,#4
ranges:
ldrh r6,[r4]
lsls r7,r6,#20
lsrs r7,r7,#20
subs r7,r3,r7
lsrs r6,r6,#12
cmp r7,r6
bls selected
adds r4,#2
subs r5,#1
bne ranges
fallback:
blx {prior.ORIGINAL_EXIT}
selected:
ldr r4,coord_ID
subs r4,r3,r4
beq coordinate
subs r4,#63
cmp r4,#1
bls status
blx {prior.LITERAL_EXIT}
coordinate:
blx {prior.COORD_EXIT}
status:
blx {prior.STATUS_EXIT}
.align 2
parent_base: .word 0x02050000
contracts: .word {prior.CONTRACTS}
coord_ID: .word 842
field_high: .word 0x0211
'''
    code=bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(assembly,prior.GATE)[0])
    return bytes(table),code,assembly


def code():
    table,gate,_=assemble()
    assert len(table)==100 and len(gate)==140
    return {prior.CONTRACTS:table,prior.GATE:gate}
