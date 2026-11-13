"""Research-only source-owned level-up adapter; no allocation growth or ROM build."""

import struct
from pathlib import Path

from keystone import Ks, KS_ARCH_ARM, KS_MODE_ARM, KS_MODE_THUMB
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from scripts.ceremony_runtime_v808 import LITERAL
from scripts.verify_village_wrap_v608 import read, save

BASE = 0x02000000
START = BASE+0x7E3B8
END = BASE+0x7E404
HOOK = BASE+0x7E56C
ROOT = Path('work/analysis/levelup_format_v818')

COORDINATES = '''ldr r1,[sp,#40]
ldr r0,[sp,#48]
ldr r2,[sp,#44]
adds r0,r1,r0
ldr r1,[sp,#52]
lsrs r3,r0,#31
adds r0,r0,r3
asrs r0,#1
adds r1,r2,r1
lsrs r3,r1,#31
adds r1,r1,r3
asrs r1,#1
str r0,[sp,#32]
subs r0,#52
str r0,[sp,#24]
str r1,[sp,#36]
subs r1,#12
str r1,[sp,#28]
movs r0,#97
ldr r3,back
bx r3
.align 2
back: .word 0x0207e404
'''

ADAPTER = f'''push {{r4,lr}}
mov r4,r0
mov r1,r0
movs r2,#0
blx {LITERAL}
mov r0,r4
blx 0x0205473c
pop {{r4,pc}}
'''


def patches(arm):
    cfg = read('translations/ceremony_editorial_release_v1.json')
    assert sha(arm) == cfg['target_arm9_sha256']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x7E2E8:0x7E5C4] == clean[0x7E2E8:0x7E5C4]
    ka, kt = Ks(KS_ARCH_ARM, KS_MODE_ARM), Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    stub = bytes(ka.asm('add ip,pc,#1;bx ip', START)[0])
    coordinate = bytes(kt.asm(COORDINATES, START+8)[0])
    helper = START+len(stub)+len(coordinate)
    adapter = bytes(kt.asm(ADAPTER, helper)[0])
    assert helper == BASE+0x7E3F0 and [len(stub), len(coordinate), len(adapter)] == [8,48,20]
    replacement = stub+coordinate+adapter
    assert len(replacement) == END-START == 76
    hook = bytes(ka.asm(f'blx {helper}', HOOK)[0])
    assert len(hook) == 4
    assert arm[HOOK-BASE:HOOK-BASE+4] == bytes(ka.asm('bl 0x0205473c', HOOK)[0])
    # Reject external ARM branches or address literals into the rewritten body.
    incoming = []; pointers = []
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
        if START <= word < END:
            pointers.append(dict(file_offset=offset,target=word))
    assert not incoming and not pointers, (incoming,pointers)
    return {START: replacement, HOOK: hook}


def apply(arm):
    result = bytearray(arm)
    for at, value in patches(arm).items():
        result[at-BASE:at-BASE+len(value)] = value
    return bytes(result)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open('out/all_routes_combined_v809_candidate.nds')
    old = rom.read_file('/__arm9__.bin'); new = apply(old)
    before, after = [MainCodeFile(a, BASE) for a in (old,new)]
    assert [(s.ramAddress,len(s.data),s.bssSize) for s in before.sections] == [(s.ramAddress,len(s.data),s.bssSize) for s in after.sections]
    assert cache_plan(old) == cache_plan(new)
    assert all(bytes(a.data) == bytes(b.data) for a,b in zip(before.sections[1:],after.sections[1:],strict=True))
    assert len(after.sections[3].data)-48 == 123040
    allowed = set(range(START-BASE,END-BASE)) | set(range(HOOK-BASE,HOOK-BASE+4))
    assert all(a==b or n in allowed for n,(a,b) in enumerate(zip(old,new,strict=True)))
    (ROOT/'ARM9_RESEARCH_ONLY.bin').write_bytes(new)
    save(ROOT/'prospective_runtime_plan.json',dict(source_ARM9_sha256=sha(old),research_ARM9_sha256=sha(new),
        source_owned_coordinate_span=[START,END],source_owned_compound_callsite=HOOK,
        helper=BASE+0x7E3F0,existing_guarded_formatter=LITERAL,
        only80_owned_code_bytes_permitted=True,geometry_cache_BSS_all_other_sections_exact=True,
        no_external_ARM_branch_or_address_literal_into_repacked_body=True,
        original_coordinate_contract='SP/rectangle words,R0=97,R1/R2,callee-saved registers;R3/IP/flags dead before original single-argument Common getter.',
        coordinate_ASM=COORDINATES,adapter_ASM=ADAPTER,
        native_coordinate_full_parent_and_all_stat_combinations_pending=True,
        COMMON_ROM_registry_and_frozen_dependencies_not_modified=True,
        playable_registered_candidate_not_created=True,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Research runtime fits the existing76-byte block plus one4-byte callsite;all other sections/cache/BSS and123040-byte staged payload exact. Native equivalence and actual scenes pending.',flush=True)


if __name__ == '__main__':
    main()
