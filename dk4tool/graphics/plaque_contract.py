"""Protect the reviewed plaque material at the end of an integrated build.

This preserves review-pending artwork. It cannot establish visual acceptance or
recover the original background hidden by Japanese lettering.
"""

import hashlib
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan

TILE_POINTER = 0x0239B440
TILE_WIDTH, TILE_HEIGHT, TILE_PERIOD = 44, 16, 40


def digest(data):
    return hashlib.sha256(data).hexdigest()


def config(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def complete_ink(image, row, font):
    left, top, right, bottom = row['draw_box']
    text = row['english']
    origin_x = left + (right - left - len(text) * 5) // 2
    origin_y = top + (bottom - top - 11) // 2
    expected = set()
    for n, char in enumerate(text):
        glyph = font.decode(char)
        if glyph.crop((5, 0, 6, 11)).getbbox():
            raise ValueError('Final plaque font exceeds its five-pixel advance: ' + char)
        expected.update((origin_x + n * 5 + x, origin_y + y)
                        for y in range(11) for x in range(5) if glyph.getpixel((x, y)))
    l, t, r, b = row['plaque_box']
    actual = {(x, y) for y in range(t, b) for x in range(l, r)
              if image.indices[y * image.width + x] == row['ink_palette_index']}
    if actual != expected or any(not (l <= x < r and t <= y < b) for x, y in expected):
        raise ValueError('Final plaque lost, clipped or added glyph pixels: ' + row['id'])
    return len(expected)


def source_hint_tile(donor):
    """Independent source coordinate model for V581's 40-column wood period."""
    result = bytearray()
    for y in range(TILE_HEIGHT):
        for x in range(TILE_WIDTH):
            if 2 <= x < 42 and 2 <= y < 14:
                sx, sy = x + 1, y + 60
            else:
                # Original 40x16 plaque frame, extended at the existing geometry.
                dx = x if x < 2 else x - 4 if x >= 42 else 2 + (x - 2) % 36
                sx, sy = 8 + dx, 20 + y
            rgb = donor.palette[donor.indices[sy * donor.width + sx]][:3]
            r, g, b = ((v * 31 + 127) // 255 for v in rgb)
            result.extend(struct.pack('<H', 0x8000 | r | (g << 5) | (b << 10)))
    return bytes(result)


def verify_final_plaque_material(candidate, clean, profile):
    """Read only; check final bytes after every registered stage has finished."""
    local_path = profile.get('local_plaque_texture')
    join_path = profile.get('equipment_grain_join')
    result = {'applicable': bool(local_path or join_path), 'static_files': [],
              'all18_entries_remain_incomplete_visual_acceptance_not_inferred': True}
    if local_path:
        local = config(local_path)
        grain = config(profile['source_plaque_grain'])
        if local['format'] != 'dk4-local-plaque-texture-v1':
            raise ValueError('Final plaque contract needs a reviewed local material config')
        source_rows = {g['file_path']: g['records'] for g in grain['files']}
        font = GameAsciiFont.from_arm9(candidate.read_file('/__arm9__.bin'))
        for group in local['files']:
            path = group['file_path']
            raw, original = candidate.read_file(path), clean.read_file(path)
            if digest(original) != group['clean_sha256']:
                raise ValueError('Final plaque original source differs: ' + path)
            image, source = PxlImage.from_bytes(raw), PxlImage.from_bytes(original)
            if raw[:image.pixels_offset] != original[:source.pixels_offset]:
                raise ValueError('Final plaque metadata, palette or geometry differs: ' + path)
            if digest(raw) != group['target_sha256']:
                raise ValueError('Final plaque material differs from reviewed reconstruction: ' + path)
            rows = source_rows[path]
            glyphs = [{'id': row['id'], 'english': row['english'],
                       'complete_ink_pixels': complete_ink(image, row, font)} for row in rows]
            result['static_files'].append({'file_path': path, 'sha256': digest(raw),
                'complete_glyph_masks': glyphs,
                'whole_reviewed_material_borders_and_unowned_pixels_exact': True,
                'original_metadata_palette_geometry_exact': True})
        result['static_config_sha256'] = digest(Path(local_path).read_bytes())
        result['glyph_config_sha256'] = digest(Path(profile['source_plaque_grain']).read_bytes())
    if join_path:
        join = config(join_path)
        grain = config(profile['source_plaque_grain'])
        if (join['format'] != 'dk4-equipment-grain-join-v1' or
                join['source_blank_bounds'] != [3, 62, 43, 74] or join['period'] != TILE_PERIOD):
            raise ValueError('Final equipment wood period/source bounds need explicit review')
        donor_raw = clean.read_file(grain['donor_file'])
        if digest(donor_raw) != grain['donor_file_sha256']:
            raise ValueError('Final equipment wood original donor differs')
        expected = source_hint_tile(PxlImage.from_bytes(donor_raw))
        arm = candidate.read_file('/__arm9__.bin')
        plan = cache_plan(arm)
        code = MainCodeFile(arm, BASE)
        section = code.sections[3]
        if (not plan or section.ramAddress != STAGE or
                not (plan['pool_span'][0] <= TILE_POINTER and
                     TILE_POINTER + len(expected) <= plan['pool_span'][1])):
            raise ValueError('Final equipment material is outside the verified startup-copy payload')
        offset = TILE_POINTER - POOL
        actual = bytes(section.data[offset:offset + len(expected)])
        if actual != expected:
            raise ValueError('Final equipment wood/frame differs from original source model')
        result['equipment_hint'] = {'tile_pointer': TILE_POINTER, 'bytes': len(expected),
            'sha256': digest(actual), 'source_blank_bounds': [3, 62, 43, 74],
            'period': TILE_PERIOD, 'complete_source_derived_frame_and_interior_exact': True,
            'native_startup_copy_destination_and_staged_payload_checked': True,
            'join_config_sha256': digest(Path(join_path).read_bytes())}
    return result
