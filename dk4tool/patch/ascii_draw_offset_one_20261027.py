"""Compile the one-pixel offset from the unchanged improved-font predecessor."""

import json
import struct
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.ascii_draw_offset_20261027_v2 import propose as compile_guarded_painter
from dk4tool.patch.grand_race_menu_release import sha


def propose(source):
    # Reuse the frozen guarded painter compiler, not any revoked ROM as input.
    compiled, proof = compile_guarded_painter(source)
    target = bytearray(compiled)
    at = proof['helper_file_offset']
    if struct.unpack_from('<I', target, at)[0] != 0xE2834002:
        raise ValueError('Expected exact ADD r4,r3,#2 painter entry')
    struct.pack_into('<I', target, at, 0xE2834001)
    if GameAsciiFont.from_arm9(target).glyphs != GameAsciiFont.from_arm9(source).glyphs:
        raise ValueError('Improved letter shapes changed')
    proof['target_ARM9_sha256'] = sha(target)
    proof['ASCII_drawing_offset_y'] = 1
    proof['helper_sha256'] = sha(target[at:at + proof['helper_bytes']])
    proof['changed_records'][0] = 'ASCII_DRAW_Y_PLUS_1'
    proof['font_height_plus_offset_fits_original_12_pixel_cells'] = True
    proof['biography_line_spacing_and_all_layout_instructions_unchanged'] = True
    proof['one_pixel_difference_from_guarded_two_pixel_compiler'] = dict(
        offset=at, before=0xE2834002, after=0xE2834001)
    return bytes(target), proof


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-ascii-draw-offset-one-20261027-v1':
        raise ValueError('Unsupported one-pixel drawing-offset release')
    for name, digest in config['dependencies'].items():
        if sha(Path(name).read_bytes()) != digest:
            raise ValueError('One-pixel offset dependency changed: ' + name)
    if sha(source) != config['source_ARM9_sha256']:
        raise ValueError('Exact complete improved-font predecessor required')
    target, proof = propose(source)
    if proof != config['proof'] or sha(target) != config['target_ARM9_sha256']:
        raise ValueError('One-pixel compiled successor differs from registered proof')
    return target, proof
