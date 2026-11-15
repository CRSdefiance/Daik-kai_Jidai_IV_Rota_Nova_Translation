"""Lower the revised live alphabet; give footer tails owned storage and bounds."""

import json
import struct
from pathlib import Path

from keystone import Ks, KS_ARCH_ARM, KS_MODE_ARM
from ndspy.code import MainCodeFile

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_common_display_name_hook import branch_link

BASE, SLOT, SLOT_END = 0x02000000, 0x01FFC200, 0x01FFC300
ROW1, ROW10, FOOTER = SLOT + 0x40, SLOT + 0x50, SLOT + 0x80
FONT = 'b1f6279176e85fa97b62013e92a964826074dcbceb05cce0935a006e2c96e0d4'


def helper():
    asm = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    result = bytearray(SLOT_END - SLOT)
    programs = {
        SLOT: '''add r4,r3,#2
            ldr ip,[r6,#8]
            subs ip,ip,r4
            ble no_rows
            cmp ip,#11
            movgt ip,#11
            str ip,[sp,#0x18]
            bx lr
        no_rows:
            ldr pc,=0x020D1814''',
        ROW1: 'ldr ip,[sp,#0x18]; cmp r1,ip; bx lr',
        ROW10: 'ldr ip,[sp,#0x18]; cmp r10,ip; bx lr',
        FOOTER: '''push {r0,r2,r3,r4,ip,lr}
            ldr r1,cache
            cmp r1,#0
            bne cached
            mov r0,#0x700
            bl 0x020051A0
            mov r1,r0
            str r1,cache
            mov r2,#0
            mov r3,#0x700
            mov ip,r1
        clear:
            str r2,[ip],#4
            subs r3,r3,#4
            bne clear
        cached:
            sub r1,r1,r4
            pop {r0,r2,r3,r4,ip,pc}
        cache:
            .word 0''',
    }
    for address, text in programs.items():
        body = bytes(asm.asm(text, addr=address)[0])
        offset = address - SLOT
        if offset + len(body) > len(result) or any(result[offset:offset + len(body)]):
            raise ValueError('Font helper storage overlaps or exceeds its reserved slot')
        result[offset:offset + len(body)] = body
    return bytes(result)


def propose(source):
    if sha(GameAsciiFont.from_arm9(source).glyphs) != FONT:
        raise ValueError('Exact improved v2 alphabet required')
    code = MainCodeFile(source, BASE)
    section = code.sections[4]
    if section.ramAddress != 0x01FFC000 or len(section.data) != 4096:
        raise ValueError('Existing fixed ITCM autoload extent differs')
    section_bytes = bytes(section.data)
    offset = source.find(section_bytes)
    if offset < 0 or source.find(section_bytes, offset + 1) >= 0:
        raise ValueError('Existing helper section must have unique physical storage')
    start = offset + SLOT - section.ramAddress
    body = helper()
    if source[start:start + len(body)] != bytes(len(body)):
        raise ValueError('Declared helper slot is no longer reserved blank storage')
    changes = [
        (0xD16CC, 0xE1A04003, branch_link(BASE + 0xD16CC, SLOT)),
        (0xD1748, 0xE351000B, branch_link(BASE + 0xD1748, ROW1)),
        (0xD1804, 0xE35A000B, branch_link(BASE + 0xD1804, ROW10)),
        (0xCA7AC, 0xE3A0000C, 0xE3A0000E),  # text view14 rows
        (0xCAA64, 0xE3A0300C, 0xE3A0300E),  # backing header14 rows
        (0xCA610, 0xE3A0100C, 0xE3A0100E),  # complete final blit14 rows
        (0xCAA74, 0xE0411004, branch_link(BASE + 0xCAA74, FOOTER)),
    ]
    target = bytearray(source)
    for at, old, new in changes:
        if struct.unpack_from('<I', source, at)[0] != old:
            raise ValueError(f'Original font/footer instruction differs at {at:X}')
        struct.pack_into('<I', target, at, new)
    target[start:start + len(body)] = body
    restored = bytearray(target)
    for at, old, _ in changes:
        struct.pack_into('<I', restored, at, old)
    restored[start:start + len(body)] = source[start:start + len(body)]
    if restored != source or GameAsciiFont.from_arm9(target).glyphs != GameAsciiFont.from_arm9(source).glyphs:
        raise ValueError('Unowned ARM9 or revised font bytes change')
    return bytes(target), dict(
        source_ARM9_sha256=sha(source), target_ARM9_sha256=sha(target),
        font_sha256=FONT, ASCII_drawing_offset_y=2,
        instruction_changes=[dict(offset=at, before=old, after=new) for at, old, new in changes],
        helper_address=SLOT, helper_file_offset=start, helper_bytes=len(body), helper_sha256=sha(body),
        footer_surface=[256, 14], footer_final_screen_y=[178, 192],
        footer_heap_bytes=1792, footer_allocation='one cached zeroed native-new allocation per cold boot',
        original_DTCM_footer_storage_and_adjacent_SDK_globals_untouched=True,
        native_cell_and_advance_and_line_spacing_and_font_pixels_unchanged=True,
        row_count_bounded_by_actual_backing_image_height=True,
        all_ROM_autoload_extents_and_staged_pool_unchanged=True,
        changed_records=['ASCII_DRAW_Y_PLUS_2', 'ASCII_DRAW_DIRECT_ROW_BOUND', 'ASCII_DRAW_PALETTED_ROW_BOUND',
            'FOOTER_TEXT_VIEW_14', 'FOOTER_BACKING_HEIGHT_14', 'FOOTER_COMPLETE_BLIT_14',
            'FOOTER_OWNED_1792_BYTE_SCRATCH', 'ASCII_DRAW_OFFSET_RESERVED_HELPER'])


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-ascii-draw-offset-20261027-v1':
        raise ValueError('Unsupported drawing-offset release')
    for name, digest in config['dependencies'].items():
        if sha(Path(name).read_bytes()) != digest:
            raise ValueError('Drawing-offset dependency changed: ' + name)
    if sha(source) != config['source_ARM9_sha256']:
        raise ValueError('Exact complete predecessor font-test stack required')
    target, proof = propose(source)
    if proof != config['proof'] or sha(target) != config['target_ARM9_sha256']:
        raise ValueError('Drawing-offset successor differs from registered proof')
    return target, proof
