"""Clip native ASCII cells at the actual bitmap right edge.

The original modal painter pads an odd ASCII run with a space. A centered
five-letter label on 36 pixels therefore paints a sixth cell at x33. With
the retained Y+1 font offset, its last row can erase the adjacent image header.
Keep the original layout, glyphs and padding; bound each physical cell write.
"""
import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.square_font_scratch_20261027 import stack_painter
from scripts.probe_common_display_name_hook import branch_link

BASE = 0x02000000
SLOT = 0x01FFC200
CLIP = 0x01FFC300
END = 0x01FFC360
MODULE = 'dk4tool/patch/ascii_glyph_right_bounds.py'


def assemble(text, address):
    return bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(text, address)[0])


def propose(source):
    code = MainCodeFile(source, BASE)
    section = code.sections[4]
    if section.ramAddress != 0x01FFC000 or len(section.data) != 4096:
        raise ValueError('Exact existing ITCM helper allocation required')
    physical = source.find(bytes(section.data))
    if physical < 0 or source.find(bytes(section.data), physical + 1) >= 0:
        raise ValueError('Unique physical helper storage required')
    # This is the retired Square scratch, released by the per-call stack repair.
    # Require that repair before using its now-zero tail for immutable code.
    if bytes(section.data[0x388:0x504]) != stack_painter():
        raise ValueError('Square must no longer write the former static scratch')
    if bytes(section.data[0x300:0x360]) != bytes(96):
        raise ValueError('Released Square scratch tail is not empty')
    target = bytearray(source)
    patches = []

    def replace(at, old, new):
        if source[at:at + len(old)] != old or len(old) != len(new):
            raise ValueError(f'Unexpected original instruction span at {at:X}')
        target[at:at + len(new)] = new
        patches.append(dict(offset=at, before_hex=old.hex(), after_hex=new.hex()))

    # The original row count occupies only one byte. Keep the independent
    # clipped column count in its unused next byte, outside the 12-byte glyph.
    replace(physical + 0x21C, assemble('bx lr', SLOT + 0x1C),
            assemble(f'b {CLIP}', SLOT + 0x1C))
    for at, register in [(0x240, 'r1'), (0x250, 'r10')]:
        replace(physical + at, assemble(f'ldr ip,[sp,#0x18]; cmp {register},ip; bx lr', section.ramAddress + at),
                assemble(f'ldrb ip,[sp,#0x18]; cmp {register},ip; bx lr', section.ramAddress + at))
    for at, register in [(0x260, 'r5'), (0x270, 'r6')]:
        body = assemble(f'ldrb ip,[sp,#0x19]; cmp {register},ip; bx lr', section.ramAddress + at)
        replace(physical + at, bytes(len(body)), body)
    for at, register, helper in [(0xD1738, 'r5', SLOT + 0x60), (0xD17F4, 'r6', SLOT + 0x70)]:
        replace(at, assemble(f'cmp {register},#6', BASE + at),
                struct.pack('<I', branch_link(BASE + at, helper)))
    body = assemble(f'''
        ldr ip,[r6]
        cmp ip,#16
        ldr ip,[r6,#4]
        lslne ip,ip,#2
        sub ip,ip,r5
        cmp ip,#0
        ble no_columns
        cmp ip,#6
        movgt ip,#6
        strb ip,[sp,#0x19]
        bx lr
    no_columns:
        ldr pc,=0x020D1814
    ''', CLIP)
    if len(body) > END - CLIP:
        raise ValueError('Clip helper exceeds released scratch ownership')
    replace(physical + 0x300, bytes(len(body)), body)
    restored = bytearray(target)
    for patch in patches:
        at = patch['offset']
        restored[at:at + len(bytes.fromhex(patch['before_hex']))] = bytes.fromhex(patch['before_hex'])
    if restored != source or len(target) != len(source):
        raise ValueError('Repair changed unowned bytes or ARM9 size')
    return bytes(target), dict(source_ARM9_sha256=sha(source), target_ARM9_sha256=sha(target),
        patches=patches, helper_address=CLIP, helper_bytes=len(body),
        retired_Square_scratch_tail=[CLIP, END],
        original_Y_plus_one_font_layout_and_text_preserved=True,
        no_section_pool_heap_or_stack_growth=True,
        changed_records=['ASCII_GLYPH_RIGHT_EDGE_BOUND', 'ASCII_COLUMN_COUNT_STACK_BYTE',
                         'ASCII_BOUNDED_DIRECT_AND_PALETTED_COLUMNS'])


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-ascii-glyph-right-bounds-v1':
        raise ValueError('Unknown glyph right-bound release')
    from dk4tool.patch.ascii_right_bounds_builder_guard import validate_current
    validate_current(config)
    if sha(Path(MODULE).read_bytes()) != config['module_sha256'] or sha(source) != config['source_ARM9_sha256']:
        raise ValueError('Frozen module and exact complete predecessor required')
    target, proof = propose(source)
    if proof != config['proof'] or sha(target) != config['target_ARM9_sha256']:
        raise ValueError('Right-bound repair differs from registered result')
    return target, proof
