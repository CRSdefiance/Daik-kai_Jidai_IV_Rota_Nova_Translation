"""Verify all current village-caption cells and the uninterpreted source fragment."""

import json
from collections import deque
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/image207_review_v330')
ROM = Path('out/all_routes_combined_v326_candidate.nds')
IDS = (168, 169, 170, 171, 206, 207, 208, 209)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    clean, current = NdsImage.open('work/clean.nds'), NdsImage.open(ROM)
    font = GameAsciiFont.from_arm9(current.read_file('/__arm9__.bin'))
    cases, negatives = [], []
    for number in IDS:
        path = f'/evstill/evstill{number}.pxl'
        original, target = clean.read_file(path), current.read_file(path)
        source, new = PxlImage.from_bytes(original), PxlImage.from_bytes(target)
        assert len(original) == len(target) and original[:source.pixels_offset] == target[:new.pixels_offset]
        assert (source.width, source.height, source.bits_per_pixel) == (256, 192, 8)
        assert (new.width, new.height, new.bits_per_pixel, new.palette) == (
            source.width, source.height, source.bits_per_pixel, source.palette)
        batch = read(f'translations/village_caption_evstill{number}_graphics_v{2 if number == 207 else 1}.json')
        assert sha(original) == batch['source_file_sha256']
        row = batch['records'][0]
        text, color, advance = row['text'], batch['color_index'], batch['advance']
        assert advance == batch['glyph_width'] == 6
        left, top, right, bottom = row['box']
        x, y = left + (right - left - len(text) * 6) // 2, top + (bottom - top - 11) // 2
        assert left <= x < x + len(text) * 6 <= right and top <= y < y + 11 <= bottom
        expected = bytearray([255] * (256 * 192))
        if number == 207:
            expected[:256 * 20] = source.indices[:256 * 20]
        glyphs = []
        for index, letter in enumerate(text):
            mask = font.decode(letter)
            points = [((y + yy) * 256 + x + index * 6 + xx) for yy in range(11) for xx in range(6)
                      if mask.getpixel((xx, yy))]
            for point in points:
                expected[point] = color
            glyphs.append(points)
        assert bytes(expected) == bytes(new.indices)
        for index in (0, len(text) - 1):
            changed = bytearray(new.indices)
            assert glyphs[index]
            for point in glyphs[index]:
                changed[point] = 255
            assert bytes(changed) != bytes(expected)
            negatives.append({'image': number, 'letter': text[index], 'index': index,
                              'erased_character_ink_pixels': len(glyphs[index]), 'whole_plane_check_rejects_erasure': True})
        cases.append({'image': number, 'Japanese': row['source_japanese'], 'English': text,
                      'bounds': [x, y, x + len(text) * 6, y + 11], 'complete_character_cells': len(text),
                      'complete_ink_pixels': sum(len(p) for p in glyphs), 'every_ink_blank_and_background_pixel_exact': True,
                      'original_header_flags_palette_and_extent_exact': True,
                      'source_sha256': sha(original), 'current_sha256': sha(target)})
    src = PxlImage.from_bytes(clean.read_file('/evstill/evstill207.pxl'))
    now = PxlImage.from_bytes(current.read_file('/evstill/evstill207.pxl'))
    points = [(i % 256, i // 256) for i, value in enumerate(src.indices[:256 * 20]) if value != 255]
    assert points and min(y for _, y in points) == 0
    assert src.indices[:256 * 20] == now.indices[:256 * 20]
    nonwhite = {i for i, value in enumerate(src.indices) if value != 255}
    connected = set()
    pending = deque(i for i in nonwhite if i // 256 == 0)
    while pending:
        point = pending.popleft()
        if point in connected:
            continue
        connected.add(point)
        x, y = point % 256, point // 256
        for yy in range(max(0, y - 1), min(192, y + 2)):
            for xx in range(max(0, x - 1), min(256, x + 2)):
                neighbor = yy * 256 + xx
                if neighbor in nonwhite and neighbor not in connected:
                    pending.append(neighbor)
    assert len(connected) == len(points) == 279
    assert max(i // 256 for i in connected) == 19
    assert all(src.indices[i] == now.indices[i] for i in connected)
    assert all(value == 255 for value in src.indices[20 * 256:21 * 256])
    mark = {'source_nonwhite_pixels': len(points), 'bounds': [min(x for x, _ in points), min(y for _, y in points),
                                                           max(x for x, _ in points) + 1, max(y for _, y in points) + 1],
            'touches_original_top_edge': True, 'whole_top20_rows_source_exact': True,
            'complete8_connected_top_edge_ink_component_pixels': len(connected),
            'blank_source_row20_separates_fragment_from_caption_beginning_row21': True,
            'decision': 'Retain the clipped source ink fragment verbatim. No unambiguous extra word/numeral is established; do not invent or erase a reading.',
            'identity_and_actual_scene_context_not_established': True}
    proof = {'candidate_unchanged': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'all_eight_full_source_current_pairs_visually_reviewed': True,
             'original_assets_are_white_cards_with_handwritten_scene_labels_not_painted_village_scenery': True,
             'New_World_Village_context_from_readable_paired169_explicit': True,
             'image208_island_distinction_retained': True, 'image168_numeral1_retained': True,
             'cases': cases, 'first_final_character_erasure_negatives': negatives, 'image207_fragment': mark,
             'actual_consumer_scene_reachability_crops_palette_alpha_and_GPU_still_open': True,
             'all18_plaque_entries_and_variants_remain_incomplete': True,
             'low_resolution_Online_images_exempt': True, 'ROM_modified': False,
             'full_goal_complete': False, 'documentation': 'docs/village_cards_v330.md'}
    out = ROOT / 'proof.json'
    out.write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / name
        audit = read(path)
        assert audit['latest_candidate_sha256'] == proof['candidate_sha256']
        assert not audit['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert all(not r['fully_completed'] for r in audit['plaque_style_v247']['ongoing_plaque_inventory'])
        audit['village_caption_source_fragment_review_v330'] = {**proof, 'proof': str(out)}
        audit['current_goal_turn_classification'] = 'progress8-village-source-context-reviews-and-complete-native-character-planes'
        path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'cards': len(cases), 'character_cells': sum(r['complete_character_cells'] for r in cases),
                      'full_ink_pixels': sum(r['complete_ink_pixels'] for r in cases),
                      'first_final_negatives': len(negatives), 'mark': mark, 'goal_complete': False}))


if __name__ == '__main__':
    main()
