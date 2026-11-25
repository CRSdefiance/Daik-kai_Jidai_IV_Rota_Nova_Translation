"""Research sort-label full strokes and source-exact old Hodram middle alias."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

ROOT = Path('work/analysis/fleet_detail_v372')
SORT, MIDDLE, WORDS = 0x01FFCC00, 0x01FFCD00, 0x01FFCE00


def assemble(text, address):
    return bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(text, address)[0])


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open('work/analysis/fleet_detail_v370/research_only_fleet_detail.nds')
    source = rom.read_file('/__arm9__.bin')
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    payload = bytearray(before[4])
    assert len(payload) <= 0xC00
    payload.extend(bytes(0xC00 - len(payload)))
    sort = assemble('''
        push {r4-r8,lr}
        sub sp,sp,#16
        mov r4,r0
        mov r5,r1
        mov r6,r2
        mov r7,r3
        ldr r8,[sp,#40]
        mov r12,r3
        cmp r12,#0
        beq fallback
        mov r2,#0
    scan:
        ldrb r0,[r12],#1
        cmp r0,#0
        beq start
        cmp r0,#32
        blo fallback
        cmp r0,#126
        bhi fallback
        add r2,r2,#1
        cmp r2,#7
        bhi fallback
        b scan
    start:
        ldmia r6,{r0,r1}
        str r0,[sp,#4]
        str r1,[sp,#8]
    letter:
        ldrb r0,[r7],#1
        cmp r0,#0
        beq done
        strb r0,[sp,#12]
        mov r0,#0
        strb r0,[sp,#13]
        str r8,[sp]
        mov r0,r4
        mov r1,r5
        add r2,sp,#4
        add r3,sp,#12
        bl 0x020d1604
        ldr r0,[sp,#4]
        add r0,r0,#5
        str r0,[sp,#4]
        b letter
    done:
        mov r0,#0
        add sp,sp,#16
        pop {r4-r8,pc}
    fallback:
        mov r0,r4
        mov r1,r5
        mov r2,r6
        mov r3,r7
        add sp,sp,#16
        pop {r4-r8,lr}
        b 0x020d1604
    ''', SORT)
    assert len(sort) <= 0x100
    payload.extend(sort)
    payload.extend(bytes(0xD00 - len(payload)))
    middle = assemble('''
        push {r1-r6,lr}
        sub sp,sp,#4
        mrs r6,cpsr
        mov r4,r0
        add r0,r4,#0x31
        ldr r1,=0x01ffce00
        bl equal
        cmp r0,#0
        beq original
        add r0,r4,#0x20
        ldr r1,=0x01ffce08
        bl equal
        cmp r0,#0
        beq original
        add r0,r4,#0x42
        ldr r1,=0x01ffce0f
        bl equal
        cmp r0,#0
        beq original
        ldr r0,=0x0215c3d4
        b finish
    original:
        add r0,r4,#0x31
    finish:
        msr cpsr_f,r6
        add sp,sp,#4
        pop {r1-r6,pc}
    equal:
        ldrb r2,[r0],#1
        ldrb r3,[r1],#1
        cmp r2,r3
        movne r0,#0
        bxne lr
        cmp r3,#0
        bne equal
        mov r0,#1
        bx lr
    ''', MIDDLE)
    assert len(middle) <= 0x100
    payload.extend(middle)
    payload.extend(bytes(0xE00 - len(payload)))
    payload.extend(b'Joachim\0Hodram\0Bergstrom\0')
    payload.extend(bytes(-len(payload) % 4))
    assert len(payload) <= 0x1000
    assert source[0x15C3D4:0x15C3DB] == b'Joakim\0'
    sort_field, name_field = 0x9D760, 0x148EB8
    assert struct.unpack_from('<I', source, sort_field)[0] == branch_link(0x02000000 + sort_field, 0x020D1604)
    assert struct.unpack_from('<I', source, name_field)[0] == 0x0203F024
    struct.pack_into('<I', code.sections[0].data, sort_field, branch_link(0x02000000 + sort_field, SORT))
    struct.pack_into('<I', code.sections[0].data, name_field, MIDDLE)
    code.sections[4].data = payload
    target = bytes(code.save())
    loaded = MainCodeFile(target, 0x02000000)
    assert all(bytes(loaded.sections[i].data) == before[i] for i in (1, 2, 3))
    assert bytes(loaded.sections[4].data[:len(before[4])]) == before[4]
    restored = bytearray(loaded.sections[0].data)
    for field in (sort_field, name_field):
        restored[field:field + 4] = source[field:field + 4]
    o = code.codeSettingsOffs
    restored[o:o + 12] = before[0][o:o + 12]
    assert bytes(restored) == before[0]
    rom.replace_file('/__arm9__.bin', target)
    rom.save(ROOT / 'research_only_fleet_detail.nds')
    (ROOT / 'research_arm9.bin').write_bytes(target)
    (ROOT / 'plan.json').write_text(json.dumps({'source_arm9_sha256': sha(source),
        'target_arm9_sha256': sha(target), 'sort_call': sort_field, 'sort_helper': SORT,
        'middle_vtable_field': name_field, 'middle_helper': MIDDLE,
        'old_default_tuple': ['Hodram', 'Joachim', 'Bergstrom'],
        'display_tuple': ['Hodram', 'Joakim', 'Bergstrom'],
        'canonical_existing_middle_pointer': 0x0215C3D4,
        'only_exact_known_old_default_alias_changed_all_fields_and_custom_names_preserved': True,
        'sort_whole_6x11_glyphs_five_pixel_advance_original_36_pixel_cells': True,
        'only_static_ASCII_labels_up_to7_characters_compacted_else_original_painter': True,
        'native_and_actual_verification_pending': True, 'not_for_handoff': True,
        'full_goal_complete': False}, indent=2) + '\n')
    print('Prepared bounded sort-label painter and exact old-default middle-name alias; no save edits.')


if __name__ == '__main__':
    main()
