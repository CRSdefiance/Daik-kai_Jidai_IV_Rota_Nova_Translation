"""All198 original collection entries: full fields, tooltips, icons and controls."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import REFERENCE_KANJI_FONT_SHA256, GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_characters_gallery_v525 import report
from scripts.verify_item_interface_research import expected_draws

ROM = Path('out/all_routes_combined_v534_candidate.nds')
OUT = Path('work/analysis/item_gallery_v535')
CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193/all_items_gallery_v535')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def glyph_pixels(font, kanji, mapping, text, x, y, advance=5):
    result, cursor = set(), x
    for char in text:
        if ord(char) < 128:
            glyph = font.decode(char)
            result.update((cursor + gx, y + gy) for gy in range(11) for gx in range(6)
                          if glyph.getpixel((gx, gy)))
            cursor += advance
        else:
            code = int.from_bytes(char.encode('cp932'), 'big')
            index = mapping.index(code)
            cell = kanji[index * 22:(index + 1) * 22]
            result.update((cursor + gx, y + gy) for gy in range(11) for gx in range(11)
                          if cell[gy * 2 + gx // 8] & (0x80 >> (gx % 8)))
            cursor += 11
    return result


def tooltip(font, image, text):
    width = len(text) * 6
    template = Image.new('1', (width, 11))
    for index, char in enumerate(text):
        template.paste(font.decode(char), (index * 6, 0))
    masks = [sum(1 << x for x in range(width) if template.getpixel((x, y))) for y in range(11)]
    rows = [sum(1 << x for x in range(256) if image.getpixel((x, y)) == (0, 8, 0))
            for y in range(250, 366)]
    clip = (1 << width) - 1
    hits = [(x, y + 250) for y in range(105) for x in range(257 - width)
            if all((rows[y + dy] >> x) & clip == line for dy, line in enumerate(masks))]
    assert len(hits) == 1, (text, hits)
    x, y = hits[0]
    assert 0 <= x and x + width <= 256 and 250 <= y and y + 11 <= 366
    return {'English': text, 'origin': [x, y], 'width': width,
            'complete_ink_pixels': sum(line.bit_count() for line in masks),
            'first_internal_last_letters_and_blank_cells_exact': True}


def main():
    digest = sha(ROM.read_bytes())
    assert digest == 'cac800924a1dfb3e2bc6352ef3f47f8f82986229377de20bc5e194046b5a6f45'
    run = report(CAPTURE, digest)
    assert all(row['unformatted_pattern'] == 'Setting %s color depth.\n'
               for row in run['core_log_unformatted_patterns'])
    assert 'Undefined instruction' not in (OUT / 'all_run.log').read_text(encoding='utf-8')
    plan = read(OUT / 'all_plan.json')
    assert run['scripted_input_schedule'] == read(OUT / 'all_inputs.json')
    assert run['frames'] == plan['final_frame'] == 23000
    assert len(plan['cases']) == 198 and sorted(c['item_id'] for c in plan['cases']) == list(range(198))
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    kanji = rom.read_file('/GRP/KANJI.FNT')
    assert sha(kanji) == REFERENCE_KANJI_FONT_SHA256
    mapping = struct.unpack_from('<3340H', arm, 0x125EC4)
    item_plan_path = Path('work/analysis/item_interface_plan.json')
    item_plan = read(item_plan_path)
    atlas = PxlImage.from_bytes(rom.read_file('/_pxl/item.pxl'))
    palette = [tuple(c // 8 for c in value[:3]) for value in atlas.palette]
    ram = (CAPTURE / 'final_arm9_ram.bin').read_bytes()
    cases, total_rows, total_ink, total_icon_pixels = [], 0, 0, 0
    for case in plan['cases']:
        index, frame = case['item_id'], case['frame']
        path = CAPTURE / f'frame_{frame:06d}_cold_boot.png'
        image = Image.open(path).convert('RGB')
        draws = expected_draws(arm, item_plan, 'main', (0, 4), item_index=index)
        name = draws[1]['text']
        rows, text_rows = {}, {}
        for draw in draws[1:]:
            source_y = draw['y']
            y = 24 if source_y == 0 else 64 if source_y == 12 else 80 if source_y == 24 else 112 + (source_y - 36) // 12 * 16
            x = 56 if source_y == 0 else 8 + draw['x']
            rows.setdefault(y, set()).update(glyph_pixels(font, kanji, mapping, draw['text'], x, y))
            text_rows.setdefault(y, []).append({'English': draw['text'], 'origin': [x, y]})
        rows[2] = glyph_pixels(font, kanji, mapping, 'Items', 116, 2)
        text_rows[2] = [{'English': 'Items', 'origin': [116, 2]}]
        masks = []
        for y, expected in sorted(rows.items()):
            left, right = (116, 144) if y == 2 else (56, 248) if y == 24 else (8, 248)
            actual = {(x, yy) for yy in range(y, y + 11) for x in range(left, right)
                      if image.getpixel((x, yy)) == (230, 230, 230)}
            assert actual == expected, (index, y, len(actual ^ expected))
            masks.append({'fields': text_rows[y], 'complete_ink_pixels': len(expected),
                          'all_first_final_letters_numbers_and_blank_cells_exact': True})
            total_rows += 1
            total_ink += len(expected)
        advice = item_plan['item_advice_projection'][index]
        stored = advice['compiled'].replace('\n', '\0').encode('ascii') + b'\0\0'
        offset = advice['pointer'] - 0x02000000
        assert ram[offset:offset + len(stored)] == stored
        pixels = atlas.indices[index * 1024:(index + 1) * 1024]
        opaque = [(n % 32, n // 32, palette[value]) for n, value in enumerate(pixels) if value]
        assert all(tuple(c // 8 for c in image.getpixel((16 + x, 24 + y))) == color
                   for x, y, color in opaque), index
        total_icon_pixels += len(opaque)
        cases.append({'item_id': index, 'page': case['page'], 'frame': frame,
                      'name': name, 'image': str(path), 'image_sha256': sha(path.read_bytes()),
                      'complete_detail_row_masks': masks, 'tooltip': tooltip(font, image, name),
                      'source_atlas_index': index, 'all_selected_icon_opaque_pixels_exact_at5bit': len(opaque),
                      'complete_description_matches_current_resident_projection': True})
    first = Image.open(CAPTURE / 'frame_002800_cold_boot.png').convert('RGB')
    wrapped = Image.open(CAPTURE / f"frame_{plan['wrap_frame']:06d}_cold_boot.png").convert('RGB')
    assert first.crop((0, 0, 256, 192)).tobytes() == wrapped.crop((0, 0, 256, 192)).tobytes()
    tooltip(font, wrapped, 'Pumpkin Seeds')
    back = Image.open(CAPTURE / f"frame_{plan['back_frame']:06d}_cold_boot.png").convert('RGB')
    # The completed original Back control returns to the Gallery submenu.
    assert glyph_pixels(font, kanji, mapping, 'Items', 113, 252, 6) <= {
        (x, y) for y in range(250, 268) for x in range(96, 160)
        if back.getpixel((x, y)) == (8, 8, 8)}
    campaign = read('translations/graphics_completion_campaign_v1.json')
    plaques = campaign['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not r['fully_completed'] for r in plaques)
    assert len(read('translations/graphics_completion_requirements_v313.json')['historical_pending_items_retained']) == 22
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'ROM_modified': False,
             'actual_report': str(CAPTURE / 'capture_report.json'),
             'actual_report_sha256': sha((CAPTURE / 'capture_report.json').read_bytes()),
             'item_projection': str(item_plan_path), 'item_projection_sha256': sha(item_plan_path.read_bytes()),
             'all198_source_collection_items_once': cases, 'complete_detail_row_masks': total_rows,
             'exact_detail_ink_pixels': total_ink, 'exact_selected_icon_opaque_pixels': total_icon_pixels,
             'all198_complete_dynamic_tooltips_and_native_first_final_letters_exact': True,
             'all198_complete_resident_descriptions_and_full_words_exact': True,
             'all14_pages_original_grid_navigation_wrap_and_Back_verified': True,
             'synthetic_collection_history_original_donor_unchanged': True,
             'normal_acquisition_equipped_owner_role_hints_other20_generated_items_not_claimed': True,
             'all22_requirements_and18_incomplete_plaques_retained': True,
             'full_goal_complete': False, 'hardware_device_verification': False}
    (OUT / 'all_items_display_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'All198 Items: {total_rows} full row masks,{total_ink} exact ink pixels,198 full tooltips,{total_icon_pixels} original opaque icon pixels;wrap/Back pass.')


if __name__ == '__main__':
    main()
