"""Record actual 96x12 draw commands while delegating all drawing unchanged."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import target
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

ROOT = Path('work/analysis/town_dispatch_trace_v496')
ENTRY, TRACE = 0x01FFC504, 0x01FFC5AC


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    parent = Path('out/all_routes_combined_v484_candidate.nds')
    rom = NdsImage.open(parent)
    source = rom.read_file('/__arm9__.bin')
    assert sha(source) == 'b03327187284a6ac560bf76ff442d75f9caa34c6b130438b582a44f2baf37c5b'
    old = target(source, 0x6BDC)
    text = f'''push {{r0-r3,ip,lr}}
cmp r0,#0x02000000
blo original
ldr ip,limit
cmp r0,ip
bhi original
ldr r1,[r0,#40]
ldr r2,[r0,#32]
sub r1,r1,r2
cmp r1,#96
bne original
ldr r1,[r0,#44]
ldr r2,[r0,#36]
sub r1,r1,r2
cmp r1,#12
bne original
ldr r1,trace
str r0,[r1,#64]
ldr r2,[r1,#68]
add r2,r2,#1
str r2,[r1,#68]
add r2,sp,#4
ldm r2,{{r2,r3,ip}}
add lr,r1,#72
stm lr,{{r2,r3,ip}}
mov r3,#64
copy:
ldr ip,[r0],#4
str ip,[r1],#4
subs r3,r3,#4
bne copy
original:
pop {{r0-r3,ip,lr}}
b {old}
trace: .word {TRACE}
limit: .word 0x023fffc0
'''
    blob = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(text, ENTRY)[0])
    assert ENTRY + len(blob) <= TRACE
    code = MainCodeFile(source, 0x02000000)
    section = code.sections[4]
    lo, hi = ENTRY - 0x01FFC000, TRACE + 84 - 0x01FFC000
    assert section.data[lo:hi] == bytes(hi - lo)
    section.data[lo:lo + len(blob)] = blob
    struct.pack_into('<I', code.sections[0].data, 0x6BDC, branch_link(0x02006BDC, ENTRY))
    arm = bytes(code.save())
    assert len(arm) == len(source)
    rom.replace_file('/__arm9__.bin', arm)
    path = ROOT / 'research_only_town_dispatch_trace.nds'
    rom.save(path)
    (ROOT / 'helper.asm').write_text(text)
    (ROOT / 'research_arm9.bin').write_bytes(arm)
    manifest = {'research_only': True, 'parent': str(parent), 'parent_sha256': sha(parent.read_bytes()),
                'research_ROM': str(path), 'research_ROM_sha256': sha(path.read_bytes()),
                'entry': ENTRY, 'trace': TRACE, 'trace_bytes': 84, 'old_dispatcher': old,
                'helper_bytes': len(blob), 'all_draw_inputs_restored_before_original_dispatcher': True,
                'match': {'width': 96, 'height': 12}, 'no_added_allocation_or_free': True,
                'production_ROM_unchanged': True, 'not_for_handoff': True}
    (ROOT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared bounded draw-command trace; original renderer retained.')


if __name__ == '__main__':
    main()
