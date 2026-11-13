"""Research shared first-row alignment without changing text or continuation guards."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

ROOT = Path('work/analysis/unguarded_alignment_v377')
ENTRY = 0x01FFCE40


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open('out/all_routes_combined_v375_candidate.nds')
    source = rom.read_file('/__arm9__.bin')
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    field = 0x54924
    word = struct.unpack_from('<I', source, field)[0]
    assert word >> 24 == 0xEB
    delta = word & 0xFFFFFF
    if delta & 0x800000:
        delta -= 0x1000000
    original = 0x02000000 + field + 8 + delta * 4
    assert original == 0x0239B104
    assembly = f'''
        push {{r2-r6,lr}}
        cmp r1,#0
        beq original
        ldr r2,[r0,#0x1c]
        cmp r2,#0
        bne original
        ldr r2,[r0,#0x24]
        ldr r3,[r0,#4]
        cmp r2,r3
        bne original
        ldr r2,[r0,#0x28]
        ldr r3,[r0,#8]
        cmp r2,r3
        bne original
        ldr r2,[r0,#0x10]
        sub r2,r2,r3
        cmp r2,#16
        blt original
        ldr r2,[r0,#0xc]
        ldr r3,[r0,#4]
        sub r6,r2,r3
        cmp r6,#12
        blt original
        sub r6,r6,#18
        ldrb r2,[r1]
        cmp r2,#33
        blo original
        cmp r2,#126
        bhi original
        mov r4,r1
        mov r5,#0
    scan:
        ldrb r2,[r4],#1
        cmp r2,#10
        beq newline
        cmp r2,#32
        blo original
        cmp r2,#126
        bhi original
        add r5,r5,#6
        cmp r5,r6
        bhi original
        b scan
    newline:
        ldrb r2,[r4]
        cmp r2,#32
        bne original
        ldrb r2,[r4,#1]
        cmp r2,#32
        bne original
        ldrb r2,[r4,#2]
        cmp r2,#33
        blo original
        cmp r2,#126
        bhi original
        ldr r2,[r0,#0x24]
        add r2,r2,#6
        str r2,[r0,#0x24]
    original:
        pop {{r2-r6,lr}}
        b {original:#x}
    '''
    payload = bytearray(before[4])
    assert len(payload) <= 0xE40
    payload.extend(bytes(0xE40 - len(payload)))
    raw = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(assembly, ENTRY)[0])
    payload.extend(raw)
    assert len(payload) <= 0x1000
    struct.pack_into('<I', code.sections[0].data, field, branch_link(0x02000000 + field, ENTRY))
    code.sections[4].data = payload
    target = bytes(code.save())
    loaded = MainCodeFile(target, 0x02000000)
    assert all(bytes(loaded.sections[i].data) == before[i] for i in (1, 2, 3))
    assert bytes(loaded.sections[4].data[:len(before[4])]) == before[4]
    restored = bytearray(loaded.sections[0].data)
    restored[field:field + 4] = source[field:field + 4]
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    assert bytes(restored) == before[0]
    (ROOT / 'research_arm9.bin').write_bytes(target)
    rom.replace_file('/__arm9__.bin', target)
    rom.save(ROOT / 'research_only_alignment.nds')
    (ROOT / 'plan.json').write_text(json.dumps({'source_arm9_sha256': sha(source),
        'target_arm9_sha256': sha(target), 'call_site': field, 'entry': ENTRY,
        'inherited_alignment_helper': original, 'new_payload_extent': len(payload),
        'only_unguarded_ASCII_first_row_with_exact_two_space_continuation_and_native_pair_flush_room': True,
        'text_source_controls_macros_dimensions_and_continuation_handling_unchanged': True,
        'actual_and_native_verification_pending': True, 'not_for_handoff': True,
        'full_goal_complete': False}, indent=2) + '\n')
    print('Prepared guarded first-row shift; all other inputs delegate to existing alignment helper.')


if __name__ == '__main__':
    main()
