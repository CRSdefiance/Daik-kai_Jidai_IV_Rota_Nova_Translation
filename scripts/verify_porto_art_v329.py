"""Current Porto title lettering and independent source protection checks."""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_embedded_graphics_v151 import decode
from scripts.porto_title_copies_v176 import FONT, SPECS, asset, batch_path, latin_gold, nearest

ROOT = Path('work/analysis/porto_review_v329')
ROM = Path('out/all_routes_combined_v326_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def plane(row):
    left, top, right, bottom = row['box']
    proof = row['artwork_proof']
    assert sha(FONT.read_bytes()) == proof['font_sha256']
    font = ImageFont.truetype(str(FONT), proof['font_size'])
    ink = Image.new('L', (right - left, bottom - top))
    painter = ImageDraw.Draw(ink)
    for line in proof['lines']:
        text, box = line['text'], line['full_glyph_box']
        b = font.getbbox(text)
        x, y = box[0] - left - b[0], box[1] - top - b[1]
        if proof['kind'] == 'caption':
            first, second = text.split(' ')
            painter.text((x, y), first, font=font, fill=255)
            painter.text((x + font.getlength(first + ' ') + 3, y), second, font=font, fill=255)
        else:
            painter.text((x, y), text, font=font, fill=255)
    assert sha(ink.tobytes()) == proof['ink_mask_sha256']
    return ink


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    cases = []
    negatives = []
    source_checks = []
    for spec in SPECS:
        original_raw, raw = clean.read_file(spec['path']), current.read_file(spec['path'])
        assert len(original_raw) == len(raw)
        if 'block' in spec:
            original_archive, current_archive = IlnkContainer.parse(original_raw), IlnkContainer.parse(raw)
            assert len(original_archive.blocks) == len(current_archive.blocks)
            for index, (a, b) in enumerate(zip(original_archive.blocks, current_archive.blocks)):
                if index != spec['block']:
                    assert a == b
            a, b = original_archive.blocks[spec['block']], current_archive.blocks[spec['block']]
            descriptor = decode(a)
            offset, length = descriptor['pixels_offset'], descriptor['pixels_bytes']
            assert a[:offset] == b[:offset] and a[offset + length:] == b[offset + length:]
        else:
            a, b = PxlImage.from_bytes(original_raw), PxlImage.from_bytes(raw)
            assert original_raw[:a.pixels_offset] == raw[:b.pixels_offset]
        width, height, old, palette = asset(spec, original_raw)
        w, h, new, colors = asset(spec, raw)
        assert (w, h, colors) == (width, height, palette)
        batch = read(batch_path(spec))
        assert sha(original_raw) == batch['source_file_sha256']
        allowed = set()
        protected_pixels = set()
        for row in batch['records']:
            left, top, right, bottom = row['box']
            allowed.update(y * width + x for y in range(top, bottom) for x in range(left, right))
            protected = Image.new('L', (right - left, bottom - top))
            protected.putdata([255 if latin_gold(spec, x, y, palette[old[y * width + x]]) else 0
                               for y in range(top, bottom) for x in range(left, right)])
            protected = protected.filter(ImageFilter.MaxFilter(3))
            for y in range(top, bottom):
                for x in range(left, right):
                    rgb = palette[old[y * width + x]][:3]
                    if protected.getpixel((x - left, y - top)) and not (rgb[2] > rgb[0] + 8 and rgb[2] > rgb[1] + 8):
                        protected_pixels.add(y * width + x)
            ink = plane(row)
            outline = ink.filter(ImageFilter.MaxFilter(3))
            blue = nearest(palette, (16, 40, 205 if row['artwork_proof']['kind'] == 'main' else 155))
            edge = nearest(palette, (235, 232, 217))
            expected = {}
            for y in range(ink.height):
                for x in range(ink.width):
                    value = ink.getpixel((x, y))
                    border = outline.getpixel((x, y))
                    if value >= 128 or border >= 128:
                        expected[(top + y) * width + left + x] = blue if value >= 128 else edge
            assert expected and all(new[index] == value for index, value in expected.items())
            line_results = []
            for line in row['artwork_proof']['lines']:
                x0, y0, x1, y1 = line['full_glyph_box']
                assert left <= x0 < x1 <= right and top <= y0 < y1 <= bottom
                points = [index for index in expected if x0 <= index % width < x1 and y0 <= index // width < y1
                          and expected[index] == blue]
                assert points
                for side, edge_x in [('first', min(i % width for i in points)),
                                     ('last', max(i % width for i in points))]:
                    changed = bytearray(new)
                    erased = [i for i in points if i % width == edge_x]
                    assert erased
                    for i in erased:
                        changed[i] = edge
                    assert not all(changed[index] == value for index, value in expected.items())
                    negatives.append({'record': row['id'], 'text': line['text'], 'side': side,
                                      'erased_edge_ink_pixels': len(erased), 'full_plane_check_rejects_erasure': True})
                line_results.append({'text': line['text'], 'declared_full_bounds': line['full_glyph_box'],
                                     'complete_quantized_ink_pixels': len(points)})
            cases.append({'resource': spec['path'], 'record': row['id'],
                          'Japanese': row['source_japanese'], 'English': row['english'],
                          'whole_ink_outline_pixels_exact': len(expected), 'lines': line_results,
                          'reconstruction': row['artwork_proof']['reconstruction']})
        assert all(a == b for i, (a, b) in enumerate(zip(old, new)) if i not in allowed)
        gold = [i for i, index in enumerate(old) if latin_gold(spec, i % width, i // width, palette[index])]
        assert gold and all(new[i] == old[i] for i in gold)
        assert all(new[i] == old[i] for i in protected_pixels)
        source_checks.append({'resource': spec['path'], 'dimensions': [width, height],
                              'original_palette_and_dimensions_exact': True,
                              'original_headers_flags_extents_and_other_archive_blocks_exact': True,
                              'all_pixels_outside_declared_rectangles_exact': True,
                              'all_original_gold_indices_exact': len(gold),
                              'all_declared_gold_bevel_adjacent_shadow_pixels_exact': len(protected_pixels),
                              'source_sha256': sha(original_raw), 'current_sha256': sha(raw)})
    assert len(cases) == 6 and len(negatives) == 18
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'source_protection': source_checks, 'complete_word_planes': cases,
             'first_last_ink_erasure_negative_cases': negatives,
             'source_and_current_three_full_artwork_pairs_visually_reviewed': True,
             'main_title_retains_established_Uncharted_Waters_IV_localization': True,
             'subtitle_uses_existing_original_Latin_Porto_Estado_name': True,
             'scenery_hidden_under_original_glyphs_remains_approximate': True,
             'actual_legacy_consumer_crops_palette_alpha_and_GPU_still_open': True,
             'all18_plaque_entries_and_variants_remain_incomplete': True,
             'low_resolution_Online_images_exempt': True, 'ROM_modified': False,
             'full_goal_complete': False, 'documentation': 'docs/porto_review_v329.md'}
    path = ROOT / 'proof.json'
    path.write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        target = Path('translations') / name
        audit = read(target)
        assert audit['latest_candidate_sha256'] == proof['candidate_sha256']
        assert not audit['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert all(not r['fully_completed'] for r in audit['plaque_style_v247']['ongoing_plaque_inventory'])
        audit['Porto_Estado_current_art_review_v329'] = {**proof, 'proof': str(path)}
        audit['current_goal_turn_classification'] = 'progress-Porto-source-restoration-review-and-complete-quantized-letter-planes'
        target.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'artwork_pairs': 3, 'complete_regions': len(cases), 'edge_erasure_negatives': len(negatives),
                      'complete_ink_outline_pixels': sum(c['whole_ink_outline_pixels_exact'] for c in cases),
                      'ROM_modified': False, 'goal_complete': False}))


if __name__ == '__main__':
    main()
