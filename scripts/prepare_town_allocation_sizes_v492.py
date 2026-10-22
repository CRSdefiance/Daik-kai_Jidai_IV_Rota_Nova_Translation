"""Matched movie controls for compact town buffers; no release changes."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

ROOT = Path('work/analysis/town_allocation_sizes_v492')
PARENT = Path('out/all_routes_combined_v484_candidate.nds')
ENTRY, SLOT = 0x01FFC504, 0x01FFC5FC


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    parent = NdsImage.open(PARENT)
    source = parent.read_file('/__arm9__.bin')
    assert sha(source) == 'b03327187284a6ac560bf76ff442d75f9caa34c6b130438b582a44f2baf37c5b'
    movie = parent.read_file('/FLS/M28.fls')
    for size in (0, 16, 128, 608, 2912):
        code = MainCodeFile(source, 0x02000000)
        section = code.sections[4]
        assert section.ramAddress == 0x01FFC000
        struct.pack_into('<I', code.sections[0].data, 0xB59AC,
                         branch_link(0x020B59AC, ENTRY if size else 0x020D3E44))
        assembly = f'''push {{r4-r6,lr}}
mov r4,r0
mov r5,r1
ldr r6,slot
ldr r0,[r6]
cmp r0,#0
bne ready
ldr r0,amount
bl 0x02005154
str r0,[r6]
ready:
mov r0,r4
mov r1,r5
mov r2,#0
mov r3,#0
pop {{r4-r6,lr}}
b 0x020d3e44
slot: .word {SLOT}
amount: .word {size}
'''
        if size:
            blob = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(assembly, ENTRY)[0])
            offset = ENTRY - section.ramAddress
            assert ENTRY + len(blob) < SLOT
            assert section.data[offset:offset + len(blob)] == bytes(len(blob))
            assert section.data[SLOT - section.ramAddress:SLOT - section.ramAddress + 4] == bytes(4)
            section.data[offset:offset + len(blob)] = blob
        arm = bytes(code.save())
        assert len(arm) == len(source)
        rom = NdsImage.open(PARENT)
        rom.replace_file('/__arm9__.bin', arm)
        rom.replace_file('/FLS/M20.fls', movie)
        path = ROOT / f'research_only_allocate_{size}.nds'
        rom.save(path)
        (ROOT / f'allocate_{size}.asm').write_text(assembly, encoding='utf-8')
        report = {'research_only': True, 'parent': str(PARENT),
                  'parent_sha256': sha(PARENT.read_bytes()), 'research_ROM': str(path),
                  'research_ROM_sha256': sha(path.read_bytes()), 'controlled_allocation_bytes': size,
                  'original_shared_header_and_view_binding_retained': True,
                  'helper_address': ENTRY if size else None, 'pointer_slot': SLOT if size else None,
                  'M20_replaced_with_exact_M28_for_research': True,
                  'normal_ending_or_unlock_not_proven': True, 'not_for_handoff': True}
        (ROOT / f'allocate_{size}_manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Prepared five matched allocation controls; no release change.')


if __name__ == '__main__':
    main()
