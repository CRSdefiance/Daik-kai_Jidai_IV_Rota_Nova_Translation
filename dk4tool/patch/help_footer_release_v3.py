"""Full English Help captions, compact spacing only for its exact native caller."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha

PREDICATE, HELPERS, TABLE = 0x01FFC980, 0x01FFCB70, 0x02119308


def transform(source):
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000
    assert len(before[4]) == 4096
    assert before[0][0x11B4FC:0x11B504] == '最初'.encode('cp932').ljust(8, b'\0')
    for offset, text in ((0x11B574, b'Prev\0'), (0x11B53C, b'Next\0')):
        assert before[0][offset:offset + len(text)] == text
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    predicate = bytes(ks.asm(f'''
        push {{r0}}
        ldr r1,table
        cmp ip,r1
        beq caller
        ldr r0,[ip,#8]
        ldr r1,index_label
        cmp r0,r1
        beq caller
        ldr r0,[ip,#12]
        ldr r1,first_label
        cmp r0,r1
        bne wrong
    caller:
        ldr r1,first
        sub r3,r3,r1
        cmp r3,#140
        bhi wrong
    again:
        cmp r3,#0
        beq good
        subs r3,r3,#28
        bhs again
    wrong:
        mov r3,#1
        cmp r3,#0
        pop {{r0}}
        bx lr
    good:
        pop {{r0}}
        bx lr
    table:.word {TABLE}
    first:.word 0x020CA930
    index_label:.word 0x0211B524
    first_label:.word 0x0211B4FC
    ''', PREDICATE)[0])
    measure = bytes(ks.asm(f'''
        ldr ip,[sp,#0x8c]
        ldr r3,[sp,#0xa4]
        mov r2,lr
        bl {PREDICATE}
        addeq r1,r0,r0,lsl #2
        andeq ip,r0,#1
        addeq r1,r1,ip
        addne r1,r0,r0,lsl #1
        lslne r1,r1,#1
        bx r2
    ''', HELPERS)[0])
    draw_address = HELPERS + len(measure)
    draw = bytes(ks.asm(f'''
        str r2,[sp,#0x68]
        ldr ip,[sp,#0x8c]
        ldr r3,[sp,#0xa4]
        mov r2,lr
        bl {PREDICATE}
        mvneq r1,#0
        streq r1,[sp,#0x5c]
        mov r1,r8
        bx r2
    ''', draw_address)[0])
    gap_address = draw_address + len(draw)
    gap = bytes(ks.asm(f'''
        ldr ip,[sp]
        ldr r3,[sp,#24]
        mov r2,lr
        bl {PREDICATE}
        subeq r0,r0,#2
        subne r0,r0,#8
        bx r2
    ''', gap_address)[0])
    payload = measure + draw + gap
    assert len(predicate) <= 128 and len(payload) <= 144
    for address, raw, limit in ((PREDICATE, predicate, 0x01FFCA00), (HELPERS, payload, 0x01FFCC00)):
        offset = address - 0x01FFC000
        assert address + len(raw) <= limit and not any(before[4][offset:offset + len(raw)])
        code.sections[4].data[offset:offset + len(raw)] = raw
    edits = []

    def edit(offset, expected, replacement):
        assert before[0][offset:offset + len(expected)] == expected
        code.sections[0].data[offset:offset + len(expected)] = replacement
        edits.append({'offset': offset, 'expected_hex': expected.hex(), 'replacement_hex': replacement.hex()})

    for offset, old, target in ((0xCA7A8, 0xE0801080, HELPERS),
                                (0xCA808, 0xE58D2068, draw_address),
                                (0xCA864, 0xE2400008, gap_address)):
        edit(offset, struct.pack('<I', old), bytes(ks.asm(f'bl {target}', 0x02000000 + offset)[0]))
    edit(0xCA7B0, struct.pack('<I', 0xE1A04081), struct.pack('<I', 0xE1A04001))
    edit(0x7CE14, struct.pack('<I', 0x0211B4EC), struct.pack('<I', 0x0211B53C))
    edit(0x7CE18, struct.pack('<I', 0x0211B4F0), struct.pack('<I', 0x0211B574))
    edit(0x11B4FC, before[0][0x11B4FC:0x11B504], b'First\0\0\0')
    target = bytes(code.save())
    parsed = MainCodeFile(target, 0x02000000)
    assert len(target) == len(source)
    assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2, 3))
    restored = bytearray(parsed.sections[0].data)
    for row in edits:
        old = bytes.fromhex(row['expected_hex'])
        restored[row['offset']:row['offset'] + len(old)] = old
    assert bytes(restored) == before[0]
    restored = bytearray(parsed.sections[4].data)
    for address, raw in ((PREDICATE, predicate), (HELPERS, payload)):
        off = address - 0x01FFC000
        restored[off:off + len(raw)] = before[4][off:off + len(raw)]
    assert bytes(restored) == before[4]
    return target, {'main_edits': edits, 'predicate': [PREDICATE, len(predicate)],
                    'helpers': [HELPERS, len(payload)], 'Help_table': TABLE,
                    'only_exact_six_native_footer_call_returns_and_original_or_unique_copied_Help_descriptor_scoped': True,
                    'Help_caption_advance': 5, 'Help_gap': 2,
                    'Help_storage_width_and_every_caption_source_x_even_for_four_bit_copy': True,
                    'other_caption_advance_and_gap_preserved': True,
                    'all_font_pixels_palettes_and_borders_preserved': True,
                    'no_main_pool_arena_ROM_or_4096_byte_ITCM_growth': True,
                    'changed_records': ['HELP_FOOTER_PREV_NEXT_FIRST', 'HELP_FOOTER_COMPLETE_LABEL_FIT']}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-help-footer-release-v3' and sha(source) == config['source_arm9_sha256']
    target, report = transform(source)
    assert sha(target) == config['target_arm9_sha256']
    return target, report
