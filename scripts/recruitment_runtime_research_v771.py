"""CPU-only dispatch and typed condition-phrase expansion; no owned placement."""

import struct

from keystone import KS_ARCH_ARM,KS_MODE_ARM,Ks

from dk4tool.patch.shipyard_editorial import LITERAL
from dk4tool.patch.tavern_continuation_runtime import PREFIX as PREVIOUS

GATE,STATUS,PHRASES=0x02472000,0x02472600,0x02472800
STATUS_PHRASES=('a major war','a serious plague outbreak','a severe famine',
    'a major economic boom','a major economic slump','a serious shortage of seasonings',
    'a serious shortage of spices','a serious shortage of luxury goods',
    'a serious shortage of alcohol','a serious shortage of fiber',
    'a serious shortage of dye','a serious shortage of ore')
STATUS_SUFFIX=b' lately.'


def code():
    ks=Ks(KS_ARCH_ARM,KS_MODE_ARM)
    gate=bytes(ks.asm(f'''
push {{r3,r4,lr}}
ldr r3,[sp,#0x270]
ldr ip,direct_parent
cmp r3,ip
beq direct
ldr ip,role_direct_parent
cmp r3,ip
beq role_direct
ldr ip,yes_parent
cmp r3,ip
beq yes
ldr ip,queue_parent
cmp r3,ip
bne fallback
ldr r4,[sp,#0x288]
ldr ip,shortage_table
cmp r4,ip
beq selected
ldr ip,call_table
cmp r4,ip
beq selected
b fallback
yes:
ldr r4,[sp,#0x288]
ldr ip,cost_table
cmp r4,ip
beq selected
b fallback
role_direct:
ldr r4,[sp,#0x288]
sub r4,r4,#0x300
cmp r4,#0x88
beq selected
b fallback
direct:
ldr r4,[sp,#0x280]
sub r4,r4,#0x300
sub r4,r4,#0x89
cmp r4,#1
bls status
cmp r4,#2
beq selected
fallback:
pop {{r3,r4,lr}}
b {PREVIOUS}
selected:
pop {{r3,r4,lr}}
b {LITERAL}
status:
pop {{r3,r4,lr}}
b {STATUS}
direct_parent: .word 0x02054014
role_direct_parent: .word 0x02053e38
yes_parent: .word 0x02053d24
queue_parent: .word 0x02053db8
shortage_table: .word 0x021183a0
cost_table: .word 0x02118380
call_table: .word 0x02118360
''',GATE)[0])
    # At original direct parent54014,the saved R3 status pointer is SP+27C.
    # This helper saves32 bytes first. Only the last printed status field is
    # localized; the source UI string and all town-name bytes stay exact.
    status=bytes(ks.asm(f'''
push {{r0-r6,lr}}
mov r4,r1
ldr r5,[sp,#0x29c]
ldr r6,original_UI_table
mov r3,#0
find:
ldr r0,[r6,r3,lsl #2]
cmp r0,r5
beq found
add r3,r3,#1
cmp r3,#12
blo find
b done
found:
ldr r6,private_table
ldr r6,[r6,r3,lsl #2]
mov r0,r5
bl 0x020ced28
mov r5,r0
mov r0,r4
bl 0x020ced28
add r4,r4,r0
sub r4,r4,#{len(STATUS_SUFFIX)}
sub r4,r4,r5
copy:
ldrb r0,[r6],#1
cmp r0,#0
strbne r0,[r4],#1
bne copy
adr r6,suffix
tail:
ldrb r0,[r6],#1
strb r0,[r4],#1
cmp r0,#0
bne tail
done:
pop {{r0-r6,lr}}
b {LITERAL}
original_UI_table: .word 0x02156430
private_table: .word {PHRASES}
suffix: .asciz " lately."
.align 2
''',STATUS)[0])
    phrases=bytearray(12*4)
    for i,text in enumerate(STATUS_PHRASES):
        struct.pack_into('<I',phrases,i*4,PHRASES+len(phrases));phrases.extend(text.encode()+b'\0')
    return {GATE:gate,STATUS:status,PHRASES:bytes(phrases),0x01FFCF3C:bytes(ks.asm(f'b {GATE}',0x01FFCF3C)[0])}


def load(u):
    for at,blob in code().items():u.mem_write(at,blob)
