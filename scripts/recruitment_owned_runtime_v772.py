"""No-growth dispatcher consolidation prototype; production ownership is pending."""

import struct

from keystone import KS_ARCH_ARM,KS_MODE_ARM,KS_MODE_THUMB,Ks

from dk4tool.patch.shipyard_editorial import LITERAL
from scripts.recruitment_runtime_research_v771 import STATUS_PHRASES,STATUS_SUFFIX
from scripts.recruitment_quantity_v772 import assemble as quantity_code

BASE=0x02000000
ENTRY=0x02132020
GATE=0x02147E54
CONTRACTS=0x0214797C
PACKED_PHRASES=CONTRACTS+128
STATUS=0x02147C20
STATUS_TAIL=0x02147D28
COPY=0x02147B70
STATUS_CONSTANTS=0x02147EE4
ORIGINAL_EXIT,LITERAL_EXIT,COORD_EXIT,STATUS_EXIT=0x02169F78,0x0216A010,0x0216A05C,0x0216A0B0
STATUS_RETURN=0x02156078
COORD=0x02147A78
DATA_BASE=0x02130000
DATA_ADDRESSES=(0x0216DCE8,0x02131FB0,0x02132030,0x02147C5C,0x02131FE0,
    0x02131FF8,0x02131E90,0x02147A14,0x021478E0,0x02131ED4,0x0216A074,
    0x02147D50,0x02131FC8,0x0216DE68,0x0216A018)

CONTRACT_ROWS=(
    (0x02054014,0x274,0,((784,788),(790,790),(798,799),(801,801),(808,808),(820,882),(905,907),(1245,1245))),
    (0x02053FCC,0x274,0,((789,789),(800,800),(802,804),(839,839),(1246,1246))),
    (0x02053D24,0x27C,0x0211,((0x8380,0x8380),(0x8400,0x8400),(0x8460,0x8460))),
    (0x02053DB8,0x27C,0x0211,((0x8360,0x8360),(0x83A0,0x83A0),(0x8460,0x8460))),
    (0x02053C14,0x270,0x0211,((0x6610,0x6610),(0x66E0,0x66E0),(0x66F0,0x66F0),(0x6810,0x6810))),
    (0x02053C5C,0x270,0,((825,825),)),
    (0x02053E38,0x27C,0,((904,904),)),
)


def assemble(data_addresses=None):
    ka,kt=Ks(KS_ARCH_ARM,KS_MODE_ARM),Ks(KS_ARCH_ARM,KS_MODE_THUMB)
    arm=lambda source,at:bytes(ka.asm(source,at)[0])
    thumb=lambda source,at:bytes(kt.asm(source,at)[0])
    blobs={ENTRY:arm(f'push {{r3-r7,lr}}; ldr ip,[pc]; bx ip; .word {GATE|1}',ENTRY)}
    table=bytearray()
    for parent,offset,high,ranges in CONTRACT_ROWS:
        field=(offset+24-0x180)//4
        assert 0<=field<128 and high in(0,0x0211)
        table.extend(struct.pack('<HBB',parent&0xffff,field|(128 if high else 0),len(ranges)))
        for lo,hi in ranges:table.extend(struct.pack('<HH',lo,hi-lo))
    assert len(table)==128
    blobs[CONTRACTS]=bytes(table)
    blobs[GATE]=thumb(f'''
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
ldrb r6,[r4,#3]
lsls r6,r6,#2
adds r4,#4
adds r4,r4,r6
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
ranges:
ldrh r6,[r4]
subs r6,r3,r6
ldrh r7,[r4,#2]
cmp r6,r7
bls selected
adds r4,#4
subs r5,#1
bne ranges
fallback:
ldr r3,original_exit
bx r3
selected:
ldr r4,coord_ID
subs r4,r3,r4
beq coordinate
subs r4,#63
cmp r4,#1
bls status
ldr r3,literal_exit
bx r3
coordinate:
ldr r3,coord_exit
bx r3
status:
ldr r3,status_exit
bx r3
.align 2
parent_base: .word 0x02050000
contracts: .word {CONTRACTS}
original_exit: .word {ORIGINAL_EXIT}
literal_exit: .word {LITERAL_EXIT}
coord_exit: .word {COORD_EXIT}
status_exit: .word {STATUS_EXIT}
coord_ID: .word 842
field_high: .word 0x0211
''',GATE)
    blobs[ORIGINAL_EXIT]=arm('pop {r3-r7,lr}; ldr r3,[sp,#0x264]; b 0x01ffcf40',ORIGINAL_EXIT)
    blobs[LITERAL_EXIT]=arm(f'pop {{r3-r7,lr}}; b {LITERAL}',LITERAL_EXIT)
    blobs[COORD_EXIT]=arm(f'pop {{r3-r7,lr}}; b {COORD}',COORD_EXIT)
    blobs[STATUS_EXIT]=arm(f'pop {{r3-r7,lr}}; ldr ip,[pc]; bx ip; .word {STATUS|1}',STATUS_EXIT)
    blobs[STATUS_RETURN]=arm(f'pop {{r0-r7,lr}}; b {LITERAL}',STATUS_RETURN)
    # These proposed placements still require complete source/alias ownership
    # evidence before an ARM9 or ROM transform may be approved.
    texts=tuple(s.removeprefix('a ') if i<5 else s.removeprefix('a serious shortage of ') for i,s in enumerate(STATUS_PHRASES))
    if data_addresses is None:
        data_addresses=DATA_ADDRESSES
    assert len(data_addresses)==15
    phrase_pointers=[]
    for at,text in zip(data_addresses,texts+('a serious shortage of ',' lately.','a ')):
        assert at%4==0 and DATA_BASE<=at<DATA_BASE+0x40000
        blobs[at]=text.encode()+b'\0'
    for at in data_addresses[:12]:phrase_pointers.append((at-DATA_BASE)//4)
    blobs[PACKED_PHRASES]=struct.pack('<12H',*phrase_pointers)
    prefix,suffix,article=data_addresses[12:]
    blobs[STATUS]=thumb(f'''
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
mov r6,r2
mov r0,r5
blx 0x020ced28
mov r5,r0
mov r0,r4
blx 0x020ced28
adds r4,r4,r0
subs r4,#8
subs r4,r4,r5
b {STATUS_TAIL}
done:
ldr r3,return_ARM
bx r3
.align 2
UI_table: .word 0x02156430
return_ARM: .word {STATUS_RETURN}
''',STATUS)
    # Keep the code in the existing44-byte gift allocation. Its six literal
    # words are placed in the recovered end of the old Yard dispatch bank.
    literals=(PACKED_PHRASES,DATA_BASE,article,prefix,suffix,STATUS_RETURN)
    def literal_instruction(register,index,at):
        delta=STATUS_CONSTANTS+index*4-((at+4)&~3)
        assert delta>=0 and delta%4==0 and delta<=1020
        return f'ldr {register},[pc,#{delta}]'
    snippets=[
        'lsrs r6,r6,#1',('r7',0),'ldrh r7,[r7,r6]','lsls r7,r7,#2',('r0',1),
        'adds r7,r7,r0','cmp r6,#10',('r0',2),'blo prepend',('r0',3),'prepend:',
        f'bl {COPY}','mov r0,r7',f'bl {COPY}',('r0',4),f'bl {COPY}',('r3',5),'bx r3']
    lines=[];pc=STATUS_TAIL
    for snippet in snippets:
        if isinstance(snippet,tuple):snippet=literal_instruction(*snippet,pc)
        lines.append(snippet)
        if snippet.endswith(':'):continue
        pc+=4 if snippet.startswith('bl ') else 2
    blobs[STATUS_TAIL]=thumb('\n'.join(lines),STATUS_TAIL)
    blobs[STATUS_CONSTANTS]=struct.pack('<6I',*literals)
    assert len(blobs[STATUS_TAIL])<=44
    blobs[COPY]=thumb('''
loop:
ldrb r1,[r0]
adds r0,#1
strb r1,[r4]
cmp r1,#0
beq done
adds r4,#1
b loop
done:
bx lr
''',COPY)
    blobs[0x01FFCF3C]=arm(f'b {ENTRY}',0x01FFCF3C)
    blobs.update(quantity_code())
    spans=sorted((a,a+len(b)) for a,b in blobs.items())
    assert all(end<=following for (_,end),(following,_) in zip(spans,spans[1:])),spans
    return blobs


def code():return assemble()


def load(u,data_addresses=None):
    for at,blob in assemble(data_addresses).items():u.mem_write(at,blob)
