"""Compact private seven-caller quantity helper; caller closure must be proven.

This is not a public ABI. Installation must reject any incoming reference other
than the original six price BLs and one day BL. Native behavior at those seven
source-bound callers remains the required equivalence contract.
"""

from keystone import KS_ARCH_ARM,KS_MODE_ARM,KS_MODE_THUMB,Ks

from dk4tool.patch.shipyard_editorial import QUANTITY,PRICE_RETURNS,DAY_RETURN

FALLBACK=0x021478E0


def assemble():
    ka,kt=Ks(KS_ARCH_ARM,KS_MODE_ARM),Ks(KS_ARCH_ARM,KS_MODE_THUMB)
    start=QUANTITY+12
    head=bytes(ka.asm(f'ldr ip,[pc]; bx ip; .word {start|1}',QUANTITY)[0])
    body=bytes(kt.asm(f'''
push {{r4-r7,lr}}
mov r4,r0
mov r3,lr
ldr r2,day_return
cmp r3,r2
adr r5,coins
bne kind_ready
adr r5,days
kind_ready:
blx 0x020abf50
mov r6,r0
ldrb r1,[r5]
adds r5,#1
cmp r4,#1
bne plural
subs r1,#1
plural:
subs r0,r6,r1
mov r7,r0
digits:
ldrb r2,[r6]
adds r6,#1
cmp r2,#0
beq suffix
strb r2,[r7]
adds r7,#1
b digits
suffix:
ldrb r2,[r5]
adds r5,#1
strb r2,[r7]
adds r7,#1
subs r1,#1
bne suffix
movs r2,#0
strb r2,[r7]
pop {{r4-r7,pc}}
.align 2
day_return: .word {DAY_RETURN}
coins: .byte 11
.ascii " gold coins"
days: .byte 5
.ascii " days"
.align 2
''',start)[0])
    end=start+len(body)
    assert end<=QUANTITY+188
    return {QUANTITY:head+body}
