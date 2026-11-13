"""Research scoped post-substitution retry formatter in owned old string slots."""

import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs
from keystone import KS_ARCH_ARM, KS_MODE_ARM, KS_MODE_THUMB, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_stock_rows import scatter
from dk4tool.rom.nds import NdsImage
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import BASE, machine
from scripts.probe_market_stock_layout_v755 import experimental_arm
from scripts.review_market_stock_v755 import CURRENT
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/market_balanced_v756')
ENTRY, MAIN, RETRY, WEAK = 0x021399B4, 0x0213B958, 0x02139934, 0x02139818
DONE = MAIN + 144
WIDTH = 0x021398A4
WIDTH_BLOCKS = [(WIDTH, WIDTH + 28), (0x0213E320, 0x0213E330),
                (0x0213B9FC, 0x0213BA04), (0x0213E2F8, 0x0213E300),
                (0x0213E310, 0x0213E318), (0x0213E33C, 0x0213E344),
                (0x0213E354, 0x0213E35C)]


def transform(arm):
    inventory = read('work/analysis/market_stock_v755/readonly_source_span_inventory_RESEARCH.json')
    for row in inventory['free']:
        at = row['lo'] - BASE
        assert arm[at:row['hi'] - BASE] == bytes.fromhex(row['source_hex'])
    code = MainCodeFile(arm, BASE)
    main = code.sections[0].data
    ka, kt = Ks(KS_ARCH_ARM, KS_MODE_ARM), Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    entry = bytes(ka.asm(f'''ldr r3,[sp,#0x36c]
sub ip,r3,#764
sub ip,ip,#3
cmp ip,#3
bhi 0x01ffca00
ldr ip,[pc,#0]
bx ip
.word {MAIN + 1}''', ENTRY)[0])
    assert len(entry) == 32
    # All internal long jumps are Thumb-1 BL, using the already saved LR.
    # The only interworking call is the native ARM helper through BLX r3.
    text = f'''push {{r4-r7,lr}}
sub sp,#8
mov r4,r0
mov r5,r1
movs r0,#35
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
bl {WEAK}
movs r2,#0
subs r2,#2
movs r7,#0
b scan
finish:
cmp r2,#8
bgt success
failed:
bl {RETRY}
success:
bl {DONE}
.align 2
native_helper: .word 0x01ffca00
'''
    body = bytes(kt.asm(text, MAIN)[0])
    assert len(body) == 96, len(body)
    instructions = list(Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(body, MAIN))
    call = next(i for i in instructions if i.mnemonic == 'blx')
    assert call.size == 2 and call.op_str == 'r3'
    return_pc = (call.address + 2) | 1
    # Thumb BL target run is first source instruction after initial width store.
    run = MAIN + 12
    retry = bytes(kt.asm(f'''ldr r0,[sp,#0]
subs r0,#1
movs r1,#127
ands r1,r0
cmp r1,#24
bge store
cmp r0,#127
bgt fallback
movs r0,#162
b store
fallback:
movs r0,#0
store:
str r0,[sp,#0]
bl {run}
''', RETRY)[0])
    assert len(retry) <= 32, len(retry)
    done = bytes(kt.asm('ldr r0,[sp,#4]; add sp,#8; pop {r4-r7,pc}', DONE)[0])
    weak = bytes(kt.asm(f'''ldr r0,table
movs r1,#11
loop:
ldmia r0!,{{r3}}
cmp r3,r7
bne next
bl {RETRY}
next:
subs r1,#1
bne loop
bx lr
.align 2
table: .word 0x01ffcb44
''', WEAK)[0])
    assert len(weak) <= 28, len(weak)
    # All existing callers of this project-owned helper are ARM calls. The
    # scoped retry adapter is its sole Thumb caller; ownership is a release gate.
    width = bytes(ka.asm('''ldr ip,[sp,#32]
tst ip,#1
bne selected
ldr r7,portrait_return
cmp ip,r7
mov r7,#37
moveq r7,#35
bx lr
selected:
ldr r7,[sp,#36]
and r7,r7,#127
cmp r7,#0
moveq r7,#35
bx lr
portrait_return: .word 0x01ffcfd4
''', WIDTH)[0])
    patches, mapping = scatter(width, 52, WIDTH, WIDTH_BLOCKS)
    first_at = MAIN + len(body)
    first = bytes(ka.asm('''ldr ip,[sp,#32]
tst ip,#1
moveq r7,#36
bxeq lr
ldr r7,[sp,#36]
tst r7,#128
andne r7,r7,#127
addne r7,r7,#1
moveq r7,#36
bx lr''', first_at)[0])
    assert first_at + len(first) <= DONE
    used = [(ENTRY, entry), (MAIN, body), (first_at, first), (DONE, done), (RETRY, retry), (WEAK, weak), *patches]
    for at, raw in used:
        assert any(lo <= at and at + len(raw) <= hi for lo, hi in inventory['merged']), (hex(at), len(raw))
        main[at - BASE:at - BASE + len(raw)] = raw
    section = code.sections[4].data
    assert section[0xA14:0xA18] == bytes(ka.asm('mov r7,#36', 0x01FFCA14)[0])
    section[0xA14:0xA18] = bytes(ka.asm(f'bl {first_at}', 0x01FFCA14)[0])
    assert section[0xFD0:0xFD4] == bytes(ka.asm('bl 0x01ffca00', 0x01FFCFD0)[0])
    section[0xFD0:0xFD4] = bytes(ka.asm(f'bl {ENTRY}', 0x01FFCFD0)[0])
    section[0xB40:0xB44] = bytes(ka.asm(f'b {WIDTH}', 0x01FFCB40)[0])
    words = ('a', 'an', 'as', 'at', 'for', 'from', 'in', 'of', 'the', 'to', 'with')
    section[0xB44:0xB70] = struct.pack('<11I', *(int.from_bytes(s.encode('ascii'), 'big') for s in words))
    result = bytes(code.save())
    return result, {'source_ARM9_sha256': sha(arm), 'research_ARM9_sha256': sha(result),
        'private_Thumb_return_PC': return_pc, 'main_bytes': len(body), 'retry_bytes': len(retry),
        'weak_bytes': len(weak), 'source_string_patches': [(a, raw.hex()) for a, raw in used],
        'width_mapping': mapping, 'not_registered_or_distributed': True}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    arm = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    arm, _ = experimental_arm(arm)
    target, report = transform(arm)
    cpu = machine(target)
    cpu.mem_write(0x02387A20, bytes(MainCodeFile(target, BASE).sections[3].data[:-48]))
    doc = read('translations/market_stock_manuscript_v1.json')
    samples = []
    for row, values in ((doc['records'][0], ('Wheat', 'Rice')),
                        (doc['records'][1], ('Olive Oil',)),
                        (doc['records'][2], ('Wheat', 'Soybean')),
                        (doc['records'][3], ('Tea',))):
        out, lines = native_layout(cpu, b' ' + row['english'].removesuffix('{PAD}').encode(), row['message_id'], values)
        samples.append({'id': row['message_id'], 'values': values, 'lines': lines, 'hex': out.hex()})
    report['four_supplied_native_smoke_cases'] = samples
    save(ROOT / 'research_smoke.json', report)
    (ROOT / 'research_ARM9.bin').write_bytes(target)
    print([(r['id'], r['lines']) for r in samples], flush=True)


if __name__ == '__main__':
    main()
