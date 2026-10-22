"""Research independent market name surfaces; preserve the shared source atlas."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_commodity_market_v350 import helper as origin_payload
from scripts.probe_common_display_name_hook import branch_link

BASE, ENTRY = 0x02000000, 0x01FFC000
ROOT = Path('work/analysis/commodity_private_market_v354')


def helper(source):
    assembly = """
        push {r4-r11,lr}
        sub sp,sp,#0x6c
        mov r4,r0
        mov r5,r1
        ldr r6,[r4,#0x2c]
        ldr r11,=0x01ffc600
        ldr r10,=0x01ffc680
        ldr r8,[r10]
        cmp r8,#0
        bne ready
        mov r0,#0x1000
        bl 0x02005154
        mov r8,r0
        mov r1,#0
        mov r2,#0x1000
        bl 0x020d763c
        mov r0,#4
        str r0,[r8]
        mov r0,#46
        str r0,[r8,#4]
        mov r0,#36
        str r0,[r8,#8]
        ldr r0,=0x02125a20
        sub r0,r0,r8
        str r0,[r8,#0xc]
        mov r0,#32
        str r0,[r8,#0x10]
        str r8,[r10]
    ready:
        str r8,[r6,#0x10]
        mov r0,#0
        str r0,[r6,#0x1c]
        str r0,[r6,#0x20]
        mov r0,#112
        str r0,[r6,#0x28]
        str r0,[r6,#0x3c]
        ldr r1,[r6,#0x64]
        add r1,r1,r0
        str r1,[r6,#0x6c]
        mov r0,r6
        bl 0x020d393c
        mov r0,r4
        bl 0x020d5094
        ldr r9,[r4]
        str r11,[r4]
        mov r0,r4
        mov r1,r5
        bl 0x0215bb40
        str r0,[sp,#0x68]
        str r9,[r4]
        add r0,sp,#0x48
        mov r1,r5
        mov r2,#0
        mov r3,#0
    copy_name:
        ldrb r12,[r1],#1
        cmp r12,#0
        beq copied
        cmp r12,#10
        beq copied
        cmp r2,#31
        bhs copied
        strb r12,[r0],#1
        cmp r12,#32
        cmpeq r2,#14
        subls r3,r0,#1
        add r2,r2,#1
        b copy_name
    copied:
        mov r12,#0
        strb r12,[r0]
        mov r7,#12
        cmp r2,#14
        bls local
        cmp r3,#0
        beq local
        mov r12,#10
        strb r12,[r3]
        mov r7,#24
    local:
        add r6,r6,#0x74
        str r8,[r6,#0x10]
        mov r0,#112
        str r0,[r6,#0x1c]
        mov r0,#0
        str r0,[r6,#0x20]
        str r7,[r6,#0x2c]
        str r7,[r6,#0x40]
        ldr r1,[r6,#0x68]
        add r1,r1,r7
        str r1,[r6,#0x70]
        mov r0,r6
        bl 0x020d393c
        mov r0,sp
        mov r1,r6
        mov r2,#1
        bl 0x020d5160
        str r11,[sp]
        mov r0,sp
        add r1,sp,#0x48
        bl 0x0215bb40
        ldr r0,[sp,#0x68]
        add sp,sp,#0x6c
        pop {r4-r11,pc}
    """
    encoded, _ = Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(assembly, ENTRY)
    payload = bytearray(encoded)
    assert len(payload) <= 0x600
    payload.extend(bytes(0x600 - len(payload)))
    callbacks = list(struct.unpack_from('<9I', source, 0x1603E4))
    assert callbacks[7] == BASE + 0xD501C
    callbacks[7] = ENTRY + 0x71C
    payload.extend(struct.pack('<9I', *callbacks))
    payload.extend(bytes(0x640 - len(payload)))
    payload.extend(b'Shortage\0')
    payload.extend(bytes(0x64C - len(payload)))
    payload.extend(b'Trending\0')
    payload.extend(bytes(0x680 - len(payload)))
    payload.extend(bytes(4))  # One persistent, initially null private header pointer.
    payload.extend(bytes(0x6A0 - len(payload)))
    payload.extend(b'%s\n  %s %d%%\0')
    payload.extend(bytes(0x71C - len(payload)))
    previous = origin_payload(source)
    payload.extend(previous[0x11C:])
    # Relocate the native single-glyph call inside the origin wrapper.
    struct.pack_into('<I', payload, 0x71C + 84,
                     branch_link(ENTRY + 0x71C + 84, BASE + 0xD501C))
    return bytes(payload)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    source = Path('work/analysis/commodity_lazy_canvas_v349/research_arm9.bin').read_bytes()
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    rom = NdsImage.open('out/all_routes_combined_v342_candidate.nds')
    overlays = loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.files[fid])
    payload = helper(source)
    for s in [*code.sections, *overlays.values()]:
        assert s.ramAddress + len(s.data) + s.bssSize <= ENTRY or ENTRY + len(payload) <= s.ramAddress
    code.sections.append(MainCodeFile.Section(payload, ENTRY, 0))
    fields = [0xC3E1C, 0xC3F98]
    for field in fields:
        assert struct.unpack_from('<I', source, field)[0] == branch_link(BASE + field, BASE + 0xD5404)
        struct.pack_into('<I', code.sections[0].data, field, branch_link(BASE + field, ENTRY))
    statuses = []
    for old, offset, meaning in [(0x15A064, 0x640, 'Shortage'), (0x15A06C, 0x64C, 'Trending')]:
        jp = source[old:source.index(0, old)].decode('cp932')
        refs = [f for f in range(0, len(before[0]) - 3, 4)
                if struct.unpack_from('<I', before[0], f)[0] == BASE + old]
        assert refs and jp == ('不足中' if meaning == 'Shortage' else '流行中')
        for field in refs:
            struct.pack_into('<I', code.sections[0].data, field, ENTRY + offset)
        statuses.append({'Japanese': jp, 'English': meaning, 'pointer_fields': refs})
    # A dangling percent in the legacy translated printf template let the native
    # formatter consume the next Japanese string beyond the format terminator.
    old_format = 0x15A058
    assert source[old_format:source.index(0, old_format)] == b'%s\n  %s %d%'
    format_fields = [f for f in range(0, len(before[0]) - 3, 4)
                     if struct.unpack_from('<I', before[0], f)[0] == BASE + old_format]
    assert format_fields
    for field in format_fields:
        struct.pack_into('<I', code.sections[0].data, field, ENTRY + 0x6A0)
    target = bytes(code.save())
    loaded = MainCodeFile(target, BASE)
    for i in (1, 2, 3):
        assert bytes(loaded.sections[i].data) == before[i]
    restored = bytearray(loaded.sections[0].data)
    for field in fields + format_fields + [f for r in statuses for f in r['pointer_fields']]:
        restored[field:field + 4] = before[0][field:field + 4]
    restored[code.codeSettingsOffs:code.codeSettingsOffs + 12] = before[0][code.codeSettingsOffs:code.codeSettingsOffs + 12]
    assert bytes(restored) == before[0]
    assert target[0xE45DC:0xE45E0] == source[0xE45DC:0xE45E0]
    (ROOT / 'research_arm9.bin').write_bytes(target)
    for variant in ['normal', 'long']:
        fixture = NdsImage.open('work/analysis/commodity_lazy_canvas_v349/research_only_' + variant + '_Maria.nds')
        old = fixture.read_file('/__arm9__.bin')
        arm = bytearray(target)
        arm[0x9F068] = old[0x9F068]
        for index in (42, 51, 62):
            field = 0x15EF18 + index * 12
            arm[field:field + 4] = old[field:field + 4]
        fixture.replace_file('/__arm9__.bin', bytes(arm))
        fixture.save(ROOT / ('research_only_' + variant + '_Maria.nds'))
    plan = {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(target),
            'new_ITCM_section': [ENTRY, ENTRY + len(payload)], 'payload_sha256': sha(payload),
            'scoped_calls': fields, 'statuses': statuses,
            'corrected_printf_fields': format_fields,
            'corrected_printf_template': '%s\n  %s %d%%',
            'name_category_integer_argument_order_preserved': True,
            'old_sections_overlay_bytes_and_heap_bounds_preserved': True,
            'original_shared_market_bitmap_header_and_pixels_not_changed': True,
            'private_image_dimensions': [184, 36], 'private_heap_allocation': 4096,
            'persistent_header_pointer_word': ENTRY + 0x680,
            'old_allocation_prototypes_not_for_handoff': True,
            'native_and_actual_verification_pending': True, 'full_goal_complete': False}
    (ROOT / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Prepared independent Goods Info/Local surfaces and source-faithful trade-status labels.')


if __name__ == '__main__':
    main()
