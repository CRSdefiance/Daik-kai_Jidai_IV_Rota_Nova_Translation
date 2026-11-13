"""Research-only, source-owned compound-stat guard; never grows the ARM9 pool.

The alternate header is instruction-set repacked to make room for a private
adapter. The adapter copies to the unused second part of the original 768-byte
local buffer, retaining every stat row and allowing the original modal pager.
No generic prose formatter or unrelated raw-message caller is changed.
"""

import struct
from pathlib import Path

from keystone import Ks, KS_ARCH_ARM, KS_MODE_ARM, KS_MODE_THUMB
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from scripts.levelup_format_runtime_v818 import COORDINATES
from scripts.verify_village_wrap_v608 import read, save

BASE = 0x02000000
START, END, HOOK = BASE+0x7E3A8, BASE+0x7E444, BASE+0x7E56C
ROOT = Path('work/analysis/levelup_format_v819')
COPY_OFFSET = 240

GUARD = '''push {r4-r6,lr}
mov r4,r0
mov r5,r0
adds r5,#240
mov r6,r5
movs r0,#32
strb r0,[r5]
adds r5,#1
next:
ldrb r0,[r4]
adds r4,#1
cmp r0,#0
beq done
cmp r0,#10
bne copy
ldrb r1,[r4]
cmp r1,#0
beq done
strb r0,[r5]
adds r5,#1
movs r0,#32
strb r0,[r5]
adds r5,#1
copy:
strb r0,[r5]
adds r5,#1
b next
done:
movs r0,#0
strb r0,[r5]
mov r0,r6
blx 0x0205473c
pop {r4-r6,pc}
'''


def assembled():
    ka, kt = Ks(KS_ARCH_ARM, KS_MODE_ARM), Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    # LR is dead here: the very next instruction is the original manager call.
    # A single ARM BLX enters the inline Thumb block without a second stub word.
    stub = bytes(ka.asm(f'blx {START+4}', START)[0])
    body = bytearray()

    def emit(text):
        body.extend(bytes(kt.asm(text, START+len(stub)+len(body))[0]))

    def literal(rd, target):
        pc = START+len(stub)+len(body)
        d = target-((pc+4)&~3)
        assert 0 <= d <= 1020 and d % 4 == 0
        body.extend(struct.pack('<H', 0x4800 | (rd << 8) | (d // 4)))

    emit('blx 0x0203f0f8;mov r1,r0;add r0,sp,#40;blx 0x02090698')
    coordinates_at = START+len(stub)+len(body)
    coordinate_text = COORDINATES.split('ldr r3,back')[0]
    emit(coordinate_text)
    assert bytes(body[-38:]) == bytes(kt.asm(coordinate_text, coordinates_at)[0])
    emit('blx 0x0205528c;mov r4,r0;mov r0,r6;ldr r1,[r0];ldr r1,[r1,#32];blx r1;mov r2,r0')
    literal(0, BASE+0x7E5B4)
    emit('mov r1,r4;blx 0x020abfcc')
    literal(2, BASE+0x7E5B8)
    emit('mov r1,r0;str r2,[sp,#0]')
    literal(0, BASE+0x7E5BC)
    emit('add r2,sp,#24;movs r3,#90')
    pc = START+len(stub)+len(body)
    d = END-((pc+4)&~3)
    assert 0 <= d <= 1020 and d % 4 == 0
    body.extend(struct.pack('<H', 0xA400 | (d // 4)))
    emit('bx r4')
    helper = START+len(stub)+len(body)
    guard = bytes(kt.asm(GUARD, helper)[0])
    replacement = stub+bytes(body)+guard
    assert [len(stub), len(body), len(guard)] == [4,90,62]
    assert helper == BASE+0x7E406
    assert len(replacement) == END-START == 156
    hook = bytes(ka.asm(f'blx {helper}', HOOK)[0])
    assert len(hook) == 4
    return {START: replacement, HOOK: hook}, helper, coordinates_at


def patches(arm):
    cfg = read('translations/ceremony_editorial_release_v1.json')
    assert sha(arm) == cfg['target_arm9_sha256']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x7E2E8:0x7E5C4] == clean[0x7E2E8:0x7E5C4]
    ka = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    assert arm[HOOK-BASE:HOOK-BASE+4] == bytes(ka.asm('bl 0x0205473c', HOOK)[0])
    incoming, pointers = [], []
    for offset in range(0, 0x110000, 4):
        word = struct.unpack_from('<I', arm, offset)[0]
        if word & 0x0E000000 == 0x0A000000:
            delta = word & 0xFFFFFF
            if delta & 0x800000:
                delta -= 1 << 24
            target = BASE+offset+8+delta*4
            if START <= target < END and not START <= BASE+offset < END:
                incoming.append(dict(source=BASE+offset,target=target))
    for offset in range(0, len(arm)-3, 4):
        word = struct.unpack_from('<I', arm, offset)[0]
        if START <= (word & ~1) < END:
            pointers.append(dict(file_offset=offset,target=word))
    assert incoming == [dict(source=BASE+0x7E370,target=START)] and not pointers, (incoming,pointers)
    return assembled()[0]


def apply(arm):
    result = bytearray(arm)
    for at, value in patches(arm).items():
        result[at-BASE:at-BASE+len(value)] = value
    return bytes(result)


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    old = NdsImage.open('out/all_routes_combined_v809_candidate.nds').read_file('/__arm9__.bin')
    new = apply(old)
    before, after = [MainCodeFile(a,BASE) for a in (old,new)]
    assert [(s.ramAddress,len(s.data),s.bssSize) for s in before.sections] == [(s.ramAddress,len(s.data),s.bssSize) for s in after.sections]
    assert cache_plan(old) == cache_plan(new)
    assert all(bytes(a.data)==bytes(b.data) for a,b in zip(before.sections[1:],after.sections[1:],strict=True))
    assert len(after.sections[3].data)-48 == 123040
    allowed = set(range(START-BASE,END-BASE)) | set(range(HOOK-BASE,HOOK-BASE+4))
    assert all(a==b or n in allowed for n,(a,b) in enumerate(zip(old,new,strict=True)))
    assert old[END-BASE:END-BASE+4] == new[END-BASE:END-BASE+4]
    (ROOT/'ARM9_RESEARCH_ONLY.bin').write_bytes(new)
    save(ROOT/'prospective_runtime_plan.json',dict(source_ARM9_sha256=sha(old),research_ARM9_sha256=sha(new),
        owned_source_header_span=[START,END],compound_callsite=HOOK,helper=assembled()[1],
        original_final_header_call_preserved=True,original_768_byte_local_buffer_copy_offset=COPY_OFFSET,
        original_stat_names_wording_order_and_numbers_preserved=True,
        six_rows_use_original_modal_pagination_instead_of_four_row_reflow=True,
        geometry_cache_BSS_other_sections_and_123040_payload_exact=True,
        only_original_entry_branch_targets_repacked_header=True,
        header_and_compound_contracts_and_actual_GPU_pagination_pending=True,
        COMMON_ROM_registry_and_frozen_dependencies_not_modified=True,
        playable_registered_candidate_not_created=True,guard_ASM=GUARD,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Research adapter fits156 existing header bytes plus4-byte compound call; no allocations grow. Full contracts and pagination remain pending.',flush=True)


if __name__ == '__main__':
    main()
