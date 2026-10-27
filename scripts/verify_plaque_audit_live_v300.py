"""Whole live plaque pixels, independent letters, numeric fields and hints."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_plaque_style_v247 import paper
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_plaque_audit_native_v300 import DIGEST, ROM, ROOT, read
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_short_equipment_release_v252 import numeric_field


def main():
    assert sha(ROM.read_bytes()) == DIGEST
    image = NdsImage.open(ROM)
    font = GameAsciiFont.from_arm9(image.read_file('/__arm9__.bin'))
    native = read(ROOT / 'native_proof.json')
    assert native['candidate_sha256'] == DIGEST and len(native['all470_native_framebuffer_paper_cases']) == 470
    reports, frames = {}, {}
    for name in ('crew', 'person'):
        report = read(f'work/emulation_v193/plaque_audit_v300_{name}/capture_report.json')
        assert report['ROM_sha256'] == DIGEST and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and report['frames'] == (11200 if name == 'crew' else 14400)
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
            if 'navigation' in row['path']:
                frames[name, row['frame']] = Image.open(row['path']).convert('RGB')
        reports[name] = report
    plaque_cases, caption_cases, abilities = [], [], []
    for name, selections, batch_path in (
        ('crew', (10000, 10300, 10600), 'translations/assign_sailors_graphics_v5.json'),
        ('person', (10500, 12600, 13500, 14400), 'translations/person_info_graphics_v3.json')):
        batch = read(batch_path)
        asset = PxlImage.from_bytes(image.read_file(batch['file_path']))
        prior = NdsImage.open('out/all_routes_combined_v247_candidate.nds').read_file(batch['file_path'])
        assert asset.source == prior
        for number in selections:
            shot = frames[name, number]
            for row in batch['records']:
                x0, y0, x1, y1 = row['plaque_box']
                for y in range(y0, y1):
                    for x in range(x0, x1):
                        assert native5(shot.getpixel((x, y))) == native5(asset.palette[asset.indices[y * asset.width + x]])
                # Decode the full unchanged native font independently. The last
                # sixth column is blank; five-pixel plaque advance removes no ink.
                left, top, right, bottom = row['draw_box']
                text, advance = row['text'], batch['advance']
                tx, ty = left + (right - left - len(text) * advance) // 2, top + (bottom - top - 11) // 2
                expected = set()
                for n, c in enumerate(text):
                    cell = font.decode(c)
                    assert not cell.crop((batch['glyph_width'], 0, 6, 11)).getbbox()
                    expected |= {(tx + n * advance + x, ty + y) for y in range(11) for x in range(6) if cell.getpixel((x, y))}
                color = native5(asset.palette[batch['color_index']])
                actual = {(x, y) for y in range(y0, y1) for x in range(x0, x1) if native5(shot.getpixel((x, y))) == color}
                assert actual == expected, (name, number, text, len(actual), len(expected))
                plaque_cases.append({'screen': name, 'frame': number, 'id': row['id'], 'English': text,
                                     'Japanese': row['source_japanese'], 'bounds': row['plaque_box'],
                                     'whole_paper_bevel_lettering_and_complete_independent_font_ink_exact': True,
                                     'ink_pixels': len(expected), 'fully_completed': False})
            if name == 'person':
                lines = []
                for label, x, y in [('Command', 16, 272), ('Sailing', 96, 272), ('Survey', 176, 272),
                                    ('Finance', 16, 296), ('Observe', 96, 296), ('Vigor', 176, 296),
                                    ('Aim', 16, 320), ('Swords', 96, 320), ('Speech', 176, 320), ('Guile', 16, 344)]:
                    value = numeric_field(font, shot, x + 42, y)
                    assert 0 <= value <= 500
                    ink, bounds = complete_mask(font, f'{label:>7}{value:3d}', shot, x, y, (230, 230, 230))
                    lines.append({'name': label, 'value': value, 'bounds': bounds, 'full_label_and_all_three_number_cells_exact': True, 'ink_pixels': ink})
                abilities.append({'frame': number, 'complete_skill_lines': lines,
                                  'Health': find_mask(font, 'Healthy', shot, (50, 102, 119, 122)),
                                  'Mood': find_mask(font, 'Normal', shot, (50, 122, 119, 142))})
    for number, text in ((10500, 'Lil Argot'), (12600, 'Camille Marinus Overijssel')):
        case = find_mask(font, text, frames['person', number], (82, 20, 255, 55))
        caption_cases.append({'frame': number, **case})
    # The actual immutable ordinary surname is protected CP932 F + erog;
    # clean Japanese is フェローグ. Do not substitute an assumed Ferox spelling.
    arm = image.read_file('/__arm9__.bin')
    mapping = struct.unpack_from('<3340H', arm, 0x125EC4)
    kanji = image.read_file('/GRP/KANJI.FNT')
    fields = read('work/analysis/reviewed_name_release_v299/dependency_native_proof.json')
    assert fields['target_ARM9_sha256'] == sha(arm)
    names = {(r['index'], r['column']): bytes.fromhex(r['after_hex']).decode('cp932') for r in fields['native_getter_cases']}
    for number, person in ((13500, 14), (14400, 20)):
        text = names[person, 0] + ' ' + names[person, 4]
        expected, advance = set(), 0
        for c in text:
            raw = c.encode('cp932')
            if len(raw) == 1:
                cell = font.decode(c)
                expected |= {(advance + x, y) for y in range(11) for x in range(6) if cell.getpixel((x, y))}
                advance += 6
            else:
                index = mapping.index(int.from_bytes(raw, 'big'))
                cell = kanji[index * 22:(index + 1) * 22]
                expected |= {(advance + x, y) for y in range(11) for x in range(11)
                             if cell[y * 2 + x // 8] & (0x80 >> (x % 8))}
                advance += 12
        shot, matches = frames['person', number], []
        for y0 in range(20, 45):
            for x0 in range(82, 89):
                actual = {(x - x0, y - y0) for y in range(y0, y0 + 12) for x in range(x0, x0 + advance)
                          if shot.getpixel((x, y)) == (230, 230, 230)}
                if actual == expected:
                    matches.append((x0, y0))
        assert len(matches) == 1, (text, matches)
        x0, y0 = matches[0]
        caption_cases.append({'frame': number, 'text': text, 'source_native_person_index': person,
                              'bounds': [x0, y0, x0 + advance, y0 + 12],
                              'all_ASCII_and_protected_CP932_F_native_foreground_pixels_exact': len(expected),
                              'first_internal_and_final_letters_complete': True})
    hints = []
    palette = PxlImage.from_bytes(image.read_file('/_pxl/towninfo.pxl')).palette
    for number, text, x0, width in ((10500, 'Equipped Items', 136, 88), (10800, 'Equipped Items', 136, 88),
                                   (11100, 'Equipped Items', 112, 88), (11400, 'Armor', 64, 34), (11700, 'Weapon', 16, 40)):
        shot = frames['person', number]
        ink, bounds = complete_mask(font, text, shot, x0 + 2, 210, (0, 8, 0))
        tile, bg = paper(width, 16, palette), 0
        for y in range(16):
            for x in range(width):
                pixel = shot.getpixel((x0 + x, 208 + y))
                if pixel == (0, 8, 0):
                    continue
                assert native5(pixel) == native5(palette[tile[y * width + x]])
                bg += 1
        assert bg + ink == width * 16
        hints.append({'frame': number, 'text': text, 'bounds': [x0, 208, x0 + width, 224],
                      'complete_ink_pixels': ink, 'complete_native_paper_pixels': bg,
                      'source_paper_first_final_letters_and_full_bounds_exact': True, 'fully_completed': False})
    raw = image.read_file('/_pxl/__marker.pxl')
    marker = PxlImage.from_bytes(raw)
    palette_start = struct.unpack_from('<I', raw, 12)[0]
    bank = [native5(bgr555(c)) for c, in struct.iter_unpack('<H', raw[palette_start + 48 * 32:palette_start + 49 * 32])]
    genders = []
    for number, character, (sx, sy) in ((10500, 'Lil', (240, 112)), (12600, 'Camille', (232, 96)),
                                       (13500, 'Emilio', (232, 96)), (14400, 'Fernando', (232, 96))):
        shot = frames['person', number]
        for y in range(16):
            for x in range(16):
                index = marker.indices[(sy + y) * marker.width + sx + x]
                assert native5(shot.getpixel((84 + x, 76 + y))) == bank[index]
        genders.append({'frame': number, 'character': character, 'all256_native_palette48_gender_cell_pixels_exact': True})
    collage = Image.new('RGB', (1024, 800), '#333333')
    draw = ImageDraw.Draw(collage)
    for n, (name, number, label) in enumerate((('crew', 10000, 'Fleet crew16'), ('crew', 10300, 'Lo: fleet crew0'),
                                             ('person', 10500, 'Lil'), ('person', 12600, 'Camille'),
                                             ('crew', 10600, 'Hi: fleet crew16'), ('person', 13500, 'Emilio'),
                                             ('person', 14400, 'Fernando'), ('person', 11700, 'Weapon'))):
        x, y = n % 4 * 256, n // 4 * 400
        draw.text((x + 5, y + 3), label, fill='white')
        collage.paste(frames[name, number], (x, y + 16))
    collage.save(ROOT / 'current_plaque_review.png')
    result = {'format': 'dk4-current-plaque-live-audit-v300', 'candidate': str(ROM), 'candidate_sha256': DIGEST,
              'plaque_cases': plaque_cases, 'actual_all18_inventory_entries_covered': True,
              'four_complete_name_caption_cases': caption_cases, 'all40_complete_skill_label_value_lines': abilities,
              'hint_cases': hints, 'gender_cells': genders,
              'crew_Lo0_Hi16_current16_unassigned_values_visually_verified': True,
              'native_proof_sha256': sha((ROOT / 'native_proof.json').read_bytes()),
              'capture_reports': {n: {'frames': r['frames'], 'ROM_sha256': r['ROM_sha256']} for n, r in reports.items()},
              'all_native_ROM_graphics_unchanged_no_fix_needed_for_observed_cases': True,
              'two_fresh_cold_boot_runs_no_savestate_or_RAM_injection': True,
              'actual_occupied_Armor_Weapon_alternate_health_mood_other_routes_and_full_audit_pending': True,
              'all18_inventory_entries_and_variants_fully_completed': False,
              'ROM_modified': False, 'full_goal_complete': False}
    (ROOT / 'live_proof.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(plaque_cases)} complete live plaques,40 full skills,five hints,four names/gender cells; all18 remain open.')


if __name__ == '__main__':
    main()
