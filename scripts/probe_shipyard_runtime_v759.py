"""Research typed quantities and literal ship names in reviewed Yard prose.

All new executable addresses are disposable Unicorn scratch, NOT ROM storage.
This script cannot build a ROM or register a release. Storage ownership, final
integration and actual gameplay remain separate required gates.
"""

import json
import re
import struct
from itertools import product
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from keystone import KS_ARCH_ARM, KS_MODE_ARM, KS_MODE_THUMB, Ks
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.probe_shipyard_layout_v759 import number
from scripts.review_shipyard_editorial_v759 import CURRENT, MANUSCRIPT, NUMERIC_RAM, ROOT
from scripts.verify_village_wrap_v608 import read, save

QUANTITY, DISPATCH, LITERAL, BALANCE = (0x02460000, 0x02461000, 0x02461800, 0x02462000)
FIRST_WIDTH = 0x02462400
DIRECT = (784, 785, 786, 787, 788, 790, 798, 799, 801)
YESNO = (789, 800, 802, 803, 804)
PRICE_RETURNS = (0x020620BC, 0x02062358, 0x02062378, 0x0206264C, 0x02063144, 0x02063178)
DAY_RETURN = 0x02063184
NAMES = ('A', 'Vestaros', 'FALCON', 'ICARUS', 'FIONA', 'FORTUNE', 'FURY',
         'ABCDEFGHIJKLMNOPQRSTUVW', 'A B C D E F G H I J K L')
PRICES = (1, 9, 99, 1000, 50000, 1000000, 2147483647)


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


def loaded(arm, blobs):
    u = machine(arm)
    u.mem_write(BASE, NUMERIC_RAM.read_bytes())
    for address, raw in blobs.items():
        u.mem_write(address, raw)
    # Only disposable emulation redirects; no production bytes/files change.
    u.mem_write(0x01FFCF3C, bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(f'b {DISPATCH}', 0x01FFCF3C)[0]))
    u.mem_write(0x0213B9C8, bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(f'b {FIRST_WIDTH}', 0x0213B9C8)[0]))
    return u


def quantity_cases(arm, blobs):
    rows, supported = [], (*PRICE_RETURNS, DAY_RETURN)
    values = (0, 1, 2, 9, 10, 16, 99, 100, 999, 1000, 12345, 50000, 65535, 1000000, 2147483647)
    for index, (ret, n) in enumerate(product(supported, values)):
        u = loaded(arm, blobs)
        thunk = 0x02464000
        ka = Ks(KS_ARCH_ARM, KS_MODE_ARM)
        u.mem_write(thunk, bytes(ka.asm(f'ldr lr,[pc,#0]; b {QUANTITY}; .word {ret}', thunk)[0]))
        u.mem_write(ret, bytes(ka.asm('b 0x027e0000', ret)[0]))
        # call() independently verifies all callee-saved registers and SP.
        call(u, thunk - BASE, (n,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        out = bytes(u.mem_read(pointer, 80)).split(b'\0')[0]
        suffix = (' day' if n == 1 else ' days') if ret == DAY_RETURN else (' gold coin' if n == 1 else ' gold coins')
        expected = number(n) + suffix.encode('ascii')
        assert out == expected, (n, hex(ret), out, expected)
        assert len(out) < 128
        rows.append({'native_value': n, 'original_return_PC': ret, 'output_hex': out.hex(), 'pointer': pointer,
                     'full_native_digits_and_typed_singular_plural_suffix': True})
    u = loaded(arm, blobs)
    for n in values:
        call(u, QUANTITY - BASE, (n,))  # STOP isn't an authorized numeric caller.
        out = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 80)).split(b'\0')[0]
        assert out == number(n)
    return {'typed_cases': rows, 'unknown_caller_fallback_cases': len(values)}


def prose():
    doc = read(MANUSCRIPT)
    rows = []
    for original in doc['records']:
        row = dict(original)
        text = original['english'].removesuffix('{PAD}')
        if row['message_id'] in (789, 799, 800, 802, 803, 804):
            text = text.replace('%s gold coins', '%s').replace('%s days', '%s')
        if row['message_id'] == 803:
            text = "A ship just like %s? It'll cost %s and take %s to prepare. Buy it?"
        row['research_english'] = text
        rows.append(row)
    return rows


def layout(u, raw, n, values):
    template, output, wrapped = 0x02420000, 0x02420810, 0x02420C10
    pointers = (0x02422000, 0x02422100, 0x02422200)
    u.mem_write(template, raw + b'\0')
    for ptr, value in zip(pointers, values):
        u.mem_write(ptr, value + b'\0')
    u.mem_write(output - 16, b'\xA5' * 288)
    u.mem_write(STACK, struct.pack('<I', pointers[2]))
    call(u, 0xD7720, (output, template, pointers[0], pointers[1]))
    expected = raw
    for value in values:
        expected = expected.replace(b'%s', value, 1)
    assert bytes(u.mem_read(output, len(expected) + 1)) == expected + b'\0'
    assert bytes(u.mem_read(output - 16, 16)) == b'\xA5' * 16
    assert bytes(u.mem_read(output + len(expected) + 1, 271 - len(expected))) == b'\xA5' * (271 - len(expected))
    u.mem_write(wrapped - 16, b'\xA5' * 288)
    parent = 0x02053DB8 if 791 <= n <= 797 else 0x02053FCC if n in YESNO else 0x02054014
    u.mem_write(STACK + 0x264, struct.pack('<I', parent))
    # Queued source SP+274 is a saved return address, NOT the selected message.
    u.mem_write(STACK + 0x274, struct.pack('<I', 0x020624B8 if 791 <= n <= 797 else n))
    u.mem_write(STACK + 0x27C, struct.pack('<I', 0x02118460))
    call(u, 0x01FFCF3C - BASE, (wrapped, output, 0), instruction_limit=2000000)
    result = bytes(u.mem_read(wrapped, 256)).split(b'\0')[0]
    assert bytes(u.mem_read(wrapped - 16, 16)) == bytes(u.mem_read(wrapped + 256, 16)) == b'\xA5' * 16
    assert b' '.join(result.split()) == b' '.join(expected.split()), (n, values, result, expected)
    rows = [r.strip() for r in result.split(b'\n')]
    findings = []
    if len(rows) > 4 or any(len(r) > 35 for r in rows):
        findings.append('four_row_whole_word_bound')
    if len(rows) > 1 and len(rows[-1]) <= 8:
        findings.append('short_final_row')
    weak = {'a', 'an', 'as', 'at', 'for', 'from', 'in', 'of', 'the', 'to', 'with'}
    # Attribute words to their source field. A inside a supplied ship name is
    # a proper name; its matching bytes do not make it the English article a.
    name_start = raw.index(b'%s') if n in (803, 804) else -1
    name_end = name_start + len(values[0]) if name_start >= 0 else -1
    tokens, index, weak_ends = list(re.finditer(rb'\S+', expected)), 0, []
    for line in rows:
        index += len(line.split())
        token = tokens[index - 1]
        proper = name_start <= token.start() < name_end if name_start >= 0 else False
        weak_ends.append(not proper and token.group().decode('cp932').strip('.,!?;:').lower() in weak)
    if any(weak_ends[:-1]):
        findings.append('weak_line_end')
    return {'id': n, 'values_hex': [v.hex() for v in values], 'parent': parent,
            'formatted_hex': result.hex(), 'lines': [r.decode('cp932') for r in rows],
            'findings': findings, 'complete_bytes_and_guarded_printf_wrap_ABI': True}


def dispatch_cases(arm, blobs):
    u, selected, rows = loaded(arm, blobs), [], []
    targets = (LITERAL, 0x01FFCF40)
    h = u.hook_add(UC_HOOK_CODE, lambda c, a, s, d: c.emu_stop() if a in targets else None)
    try:
        for parent in (0x02054014, 0x02053FCC, 0x02054044, 0x02053D24, 0x02053DB8):
            for table in (0x02118460, 0x021184C0):
                for n in range(3668):
                    u.mem_write(STACK + 0x264, struct.pack('<I', parent))
                    u.mem_write(STACK + 0x274, struct.pack('<I', n))
                    u.mem_write(STACK + 0x27C, struct.pack('<I', table))
                    from unicorn.arm_const import UC_ARM_REG_SP
                    u.reg_write(UC_ARM_REG_SP, STACK)
                    u.emu_start(0x01FFCF3C, 0x027E0000, count=100)
                    pc = u.reg_read(UC_ARM_REG_PC)
                    expected = (parent == 0x02054014 and n in DIRECT or parent == 0x02053FCC and n in YESNO
                                or parent in (0x02053D24, 0x02053DB8) and table == 0x02118460)
                    assert pc == (LITERAL if expected else 0x01FFCF40), (parent, table, n, hex(pc))
                    assert u.reg_read(UC_ARM_REG_SP) == STACK
                    selected.append(expected)
    finally:
        u.hook_del(h)
    return {'count': len(selected), 'selected': sum(selected), 'all_exact_parent_ID_or_original_queue_table_membership': True,
            'queue_saved_return_address_not_mistaken_for_message_ID': True}


def main():
    arm = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    blobs = assemble(arm)
    dest = ROOT / 'typed_literal_runtime_RESEARCH'
    dest.mkdir(parents=True, exist_ok=True)
    save(dest / 'research_code.json', {'scratch_only_not_ROM_owned': True, 'blobs': {hex(a): b.hex() for a, b in blobs.items()},
         'source_ARM9_sha256': sha(arm), 'producer_sha256': sha(Path(__file__).read_bytes())})
    quantities = quantity_cases(arm, blobs)
    save(dest / 'typed_quantities.json', quantities)
    selection = dispatch_cases(arm, blobs)
    save(dest / 'dispatch_membership.json', selection)
    print('Typed quantities and exact dispatch passed.', flush=True)
    checks, u, count = [], loaded(arm, blobs), 0
    for row in prose():
        n = row['message_id']
        raw = b' ' + row['research_english'].encode('ascii')
        price = lambda p: number(p) + (b' gold coin' if p == 1 else b' gold coins')
        days = lambda d: number(d) + (b' day' if d == 1 else b' days')
        cases = ([(number(m), number(h)) for m, h in product((1, 3, 5), (1, 100, 65535))] if n == 786 else
                 [(price(p),) for p in PRICES] if n in (789, 799, 800, 802) else
                 [(number(p),) for p in (5, 22, 40)] if n == 798 else
                 [(s.encode('ascii'), price(p), days(d)) for s, p, d in product(NAMES, PRICES, range(1, 17))] if n == 803 else
                 [(s.encode('ascii'), price(p)) for s, p in product(NAMES, PRICES)] if n == 804 else [()])
        for values in cases:
            if count % 64 == 0:
                u = loaded(arm, blobs)
            checks.append(layout(u, raw, n, values))
            count += 1
    save(dest / 'native_layout_matrix.json', {'count': len(checks), 'findings_count': sum(bool(r['findings']) for r in checks),
         'cases': checks, 'scope': 'Original printf and bounded wrapper with new code only in disposable Unicorn scratch. Boundary values supplied; actual gameplay, owned ROM storage and integration pending.'})
    save(dest / 'prose_templates.json', prose())
    print(f'{len(checks)} complete native layouts; {sum(bool(r["findings"]) for r in checks)} remaining layout findings. No ROM emitted.', flush=True)


if __name__ == '__main__':
    main()
