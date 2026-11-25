"""Exact two-caller duel dispatch in source-proven unreachable cache-selector code.

The live ARM cache-slot entry535E0 retains its exact unconditional return0/BX.
Its old64-byte tail is not cache storage; it is source-owned executable code.
Reference/entry/selector/copy proofs must precede any registered integration.
"""
from keystone import Ks,KS_ARCH_ARM,KS_MODE_THUMB

BASE=0x02000000
HELPER,HELPER_END=0x020535E8,0x02053628
FRONT,FRONT_END=0x0200DAF0,0x0200DB5C
TABLE_BASE=0x02117340
TABLES=(0x02117340,0x02117360,0x021174E0,0x02117560,0x021175C0)
IDS=(*range(1980,1994),2146)


def helper():
    # Private leaf ABI:r0=exact original saved caller,r1=source saved selector,
    # r3=the front's immutable TABLE_BASE. r0 returns bool;r1/r2/flags scratch.
    # Numeric comparison is1993-ID, accepting0..13 and the single delta-153.
    assembly='''ldr r2,parent
subs r0,r0,r2
beq voice
cmp r0,#108
bne reject
ldr r2,last_ID
subs r1,r2,r1
cmp r1,#13
bls accept
adds r1,#153
bne reject
accept:
movs r0,#1
bx lr
voice:
subs r1,r1,r3
beq accept
cmp r1,#32
beq accept
subs r1,#208
subs r1,#208
beq accept
cmp r1,#128
beq accept
cmp r1,#224
bne reject
b accept
reject:
movs r0,#0
bx lr
.align 2
parent: .word 0x0200d4bc
last_ID: .word 1993
'''
    code=bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(assembly,HELPER)[0])
    assert len(code)<=HELPER_END-HELPER==64,len(code)
    return code+bytes(HELPER_END-HELPER-len(code)),assembly,len(code)


def front(size):
    assembly=f'''push {{r4-r6,lr}}
mov r4,r0
mov r5,r1
ldr r0,[r4,#108]
mov r2,r4
adds r2,#148
ldr r1,[r2]
ldr r3,table_base
bl {HELPER}
cmp r0,#0
beq original
selected:
ldr r0,carrier
blx 0x0205528c
ldr r6,cache
mov r0,r6
ldr r1,length
blx 0x020e4430
mov r0,r6
ldr r1,length
blx 0x020e447c
mov r0,r4
mov r1,r5
adds r6,#1
blx r6
pop {{r4-r6,pc}}
original:
mov r0,r4
mov r1,r5
blx 0x020d5404
pop {{r4-r6,pc}}
.align 2
table_base: .word {TABLE_BASE}
carrier: .word 1931
cache: .word 0x0228e70c
length: .word {size}
'''
    code=bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(assembly,FRONT)[0])
    assert len(code)<=FRONT_END-FRONT==108,len(code)
    return code+bytes(FRONT_END-FRONT-len(code)),assembly,len(code)
