"""Shipyard prose runtime in retired, source-mapped constant strings.

The assembler is preserved from the independently verified V759 prototype.
Only immutable source-owned placements differ; no pool or section grows.
"""

import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from keystone import KS_ARCH_ARM, KS_MODE_ARM, KS_MODE_THUMB, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000
SOURCE = '6929d261ceb8ffdafb8281742c433c594c5b0dea649459e1d9ccd684796d325e'
QUANTITY = 0x02131F48
FIRST_WIDTH = 0x02132004
DISPATCH = 0x02147E54
LITERAL = 0x02147B98
BALANCE = 0x02147AE4
DIRECT = (784, 785, 786, 787, 788, 790, 798, 799, 801)
YESNO = (789, 800, 802, 803, 804)
PRICE_RETURNS = (0x020620BC, 0x02062358, 0x02062378, 0x0206264C, 0x02063144, 0x02063178)
DAY_RETURN = 0x02063184
BANKS = ((0x02131F48, 0x02132044), (0x02147AE4, 0x02147B80),
         (0x02147B98, 0x02147C70), (0x02147E54, 0x02147F00))

def assemble(arm):
    ka, kt = Ks(KS_ARCH_ARM, KS_MODE_ARM), Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    for pc in (*PRICE_RETURNS, DAY_RETURN):
        instruction = next(Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(arm[pc - BASE - 4:pc - BASE], pc - 4))
        assert instruction.mnemonic == 'bl' and instruction.op_str == '#0x20abf50'
    quantity = bytes(ka.asm(f'''
push {{r4-r8,lr}}
mov r4,r0
adr r2,callers
mov r3,#7
find:
ldr ip,[r2],#4
cmp lr,ip
beq matched
subs r3,r3,#1
bne find
pop {{r4-r8,lr}}
b 0x020abf50
matched:
cmp r3,#1
moveq r5,#1
movne r5,#0
bl 0x020abf50
mov r6,r0
cmp r5,#0
adreq r5,coins
adrne r5,days
ldrb r1,[r5],#1
cmp r4,#1
subeq r1,r1,#1
sub r0,r6,r1
mov r7,r0
digits:
ldrb r2,[r6],#1
cmp r2,#0
strbne r2,[r7],#1
bne digits
suffix:
ldrb r2,[r5],#1
strb r2,[r7],#1
subs r1,r1,#1
bne suffix
mov r2,#0
strb r2,[r7]
pop {{r4-r8,pc}}
callers:
.word {','.join(str(v) for v in (*PRICE_RETURNS, DAY_RETURN))}
coins:
.byte 11
.ascii " gold coins"
days:
.byte 5
.ascii " days"
.align 2
''', QUANTITY)[0])
    direct_mask = sum(1 << (n - 784) for n in DIRECT)
    yes_mask = sum(1 << (n - 784) for n in YESNO)
    dispatch = bytes(ka.asm(f'''
push {{r3,r4,lr}}
ldr r3,[sp,#0x270]
ldr ip,direct_parent
cmp r3,ip
beq direct
ldr ip,yes_parent
cmp r3,ip
beq yes
ldr ip,queue_parent1
cmp r3,ip
beq queued
ldr ip,queue_parent2
cmp r3,ip
bne original
queued:
ldr r3,[sp,#0x288]
ldr ip,voice_table
cmp r3,ip
bne original
b selected
direct:
ldr ip,direct_bits
b numbered
yes:
ldr ip,yes_bits
numbered:
ldr r3,[sp,#0x280]
sub r3,r3,#784
cmp r3,#20
bhi original
mov r4,#1
mov r4,r4,lsl r3
tst ip,r4
beq original
selected:
pop {{r3,r4,lr}}
b {LITERAL}
original:
pop {{r3,r4,lr}}
ldr r3,[sp,#0x264]
b 0x01ffcf40
direct_parent: .word 0x02054014
yes_parent: .word 0x02053fcc
queue_parent1: .word 0x02053d24
queue_parent2: .word 0x02053db8
voice_table: .word 0x02118460
direct_bits: .word {direct_mask}
yes_bits: .word {yes_mask}
''', DISPATCH)[0])
    literal = bytes(ka.asm(f'''
push {{r4,lr}}
mov r4,r0
bl 0x01ff9fac
sub sp,sp,#0xf0
mov r0,r4
ldrb r3,[r0]
cmp r3,#0x20
beq ready
bl 0x020ced28
mov r2,r0
mov r0,r4
cmp r2,#0xed
bhi ready
shift:
ldrb r3,[r0,r2]
add ip,r2,#1
strb r3,[r0,ip]
subs r2,r2,#1
bpl shift
mov r3,#0x20
strb r3,[r0]
ready:
mov r0,r4
mov r1,sp
ldr r3,helper
blx r3
cmp r0,#0
beq done
add r2,r0,#1
mov r0,r4
mov r1,sp
bl 0x020cec74
done:
mov r0,#0
add sp,sp,#0xf0
pop {{r4,pc}}
helper: .word {BALANCE + 1}
''', LITERAL)[0])
    balance = bytes(kt.asm(f'''
push {{r4-r7,lr}}
sub sp,#8
mov r4,r0
mov r5,r1
movs r0,#36
lsls r0,r0,#8
adds r0,#35
str r0,[sp,#0]
run:
mov r0,r4
mov r1,r5
ldr r3,native_helper
blx r3
str r0,[sp,#4]
ldr r1,[sp,#0]
cmp r1,#0
beq success
cmp r0,#0
beq failed
mov r6,r5
movs r2,#0
movs r7,#0
scan:
ldrb r0,[r6]
adds r6,#1
cmp r0,#0
beq finish
cmp r0,#10
beq line_end
adds r2,#1
cmp r0,#32
beq space
lsls r7,r7,#8
orrs r7,r0
b scan
space:
movs r7,#0
b scan
line_end:
ldr r0,words
movs r1,#11
weak:
ldmia r0!,{{r3}}
cmp r3,r7
beq failed
subs r1,#1
bne weak
movs r2,#0
subs r2,#2
movs r7,#0
b scan
finish:
cmp r2,#8
bgt success
failed:
ldr r0,[sp,#0]
movs r1,#255
ands r1,r0
subs r1,#1
cmp r1,#16
bge decrement
subs r0,#237
lsrs r1,r0,#8
cmp r1,#16
bge store
fallback:
movs r0,#0
b store
decrement:
subs r0,#1
store:
str r0,[sp,#0]
b run
success:
ldr r0,[sp,#4]
add sp,#8
pop {{r4-r7,pc}}
.align 2
native_helper: .word 0x01ffca00
words: .word 0x01ffcb44
''', BALANCE)[0])
    first_width = bytes(ka.asm('''
ldr ip,[sp,#32]
tst ip,#1
beq original
ldr r7,[sp,#36]
movs r7,r7,lsr #8
bxne lr
original:
b 0x0213b9cc
''', FIRST_WIDTH)[0])
    return {QUANTITY: quantity, DISPATCH: dispatch, LITERAL: literal, BALANCE: balance, FIRST_WIDTH: first_width}


def runtime_transform(source):
    """Install only the pinned runtime, with exact source and bank ownership."""
    assert sha(source) == SOURCE
    ownership_path = Path('work/analysis/shipyard_storage_v760/owned_source_storage.json')
    ownership = read(ownership_path)
    assert ownership['source_ARM9_sha256'] == SOURCE
    assert ownership['module_sha256'] == sha(Path(__file__).read_bytes())
    assert ownership['owned_banks'] == [list(p) for p in BANKS]
    assert not any(ownership[k] for k in (
        'all_current_unaligned_absolute_aliases_into_banks',
        'all_current_aligned_ARM_branches_into_banks',
        'all_current_ARM_ADR_effective_targets_into_banks',
        'all_current_Cstrings_crossing_bank_start'))
    code = MainCodeFile(source, BASE)
    assert bytes(code.save()) == source and len(code.sections) == 5
    before = [bytes(s.data) for s in code.sections]
    patches = []
    ka = Ks(KS_ARCH_ARM, KS_MODE_ARM)

    def patch(address, data, kind):
        index = 4 if address < BASE else 0
        section = code.sections[index]
        at = address - section.ramAddress
        assert 0 <= at < at + len(data) <= len(section.data)
        old = bytes(section.data[at:at + len(data)])
        section.data[at:at + len(data)] = data
        patches.append({'address': address, 'section': index, 'kind': kind,
                        'source_hex': old.hex(), 'target_hex': data.hex()})

    blobs = assemble(source)
    for address, blob in blobs.items():
        assert any(lo <= address < address + len(blob) <= hi for lo, hi in BANKS)
        patch(address, blob, 'retired-immutable-const-slot-runtime')
    for pc in (*PRICE_RETURNS, DAY_RETURN):
        patch(pc - 4, bytes(ka.asm(f'bl {QUANTITY}', pc - 4)[0]), 'exact-original-numeric-call')
    assert before[4][0xF3C:0xF40] == bytes(ka.asm('ldr r3,[sp,#0x264]', 0x01FFCF3C)[0])
    patch(0x01FFCF3C, bytes(ka.asm(f'b {DISPATCH}', 0x01FFCF3C)[0]), 'scoped-source-dispatch')
    assert source[0x13B9C8:0x13B9CC] == bytes(ka.asm('ldr ip,[sp,#32]', 0x0213B9C8)[0])
    patch(0x0213B9C8, bytes(ka.asm(f'b {FIRST_WIDTH}', 0x0213B9C8)[0]), 'encoded-first-width-adapter')
    target = bytes(code.save())
    after = MainCodeFile(target, BASE)
    assert [len(s.data) for s in after.sections] == [len(s) for s in before]
    assert len(target) == len(source) and cache_plan(target) == cache_plan(source)
    for index, section in enumerate(after.sections):
        restored = bytearray(section.data)
        for row in patches:
            if row['section'] == index:
                at = row['address'] - section.ramAddress
                old = bytes.fromhex(row['source_hex'])
                restored[at:at + len(old)] = old
        assert bytes(restored) == before[index]
    assert all(bytes(after.sections[k].data) == before[k] for k in (1, 2, 3))
    # Preserve active race text, source RTTI/pointer arrays, and every active
    # village/Deck pointer and complete replacement string.
    assert target[0x138162:0x138294] == source[0x138162:0x138294]
    for row in ownership['all54_village_and3_Deck_active_replacements_verified']:
        field = row['pointer_field']
        assert target[field:field + 4] == source[field:field + 4]
    for lo, hi in BANKS:
        assert target[lo - BASE - 16:lo - BASE] == source[lo - BASE - 16:lo - BASE]
        assert target[hi - BASE:hi - BASE + 16] == source[hi - BASE:hi - BASE + 16]
    return target, {'source_ARM9_sha256': SOURCE, 'target_ARM9_sha256': sha(target), 'patches': patches,
        'ownership_report': str(ownership_path), 'ownership_report_sha256': sha(ownership_path.read_bytes()),
        'source_bank_payload_bytes': sum(len(b) for b in blobs.values()),
        'all_unselected_section_bytes_and_57_active_text_replacements_preserved': True,
        'all_sections_and123040_byte_pool_cache_startup_and_allocator_unchanged': True,
        'experimental_not_complete_without_native_and_actual_gameplay_verification': True}

