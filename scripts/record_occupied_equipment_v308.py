"""Verify ordinary book equipment on V307; keep the broader plaque audit open."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_plaque_style_v247 import paper
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_short_equipment_release_v252 import numeric_field

ROOT = Path('work/analysis/occupied_equipment_v308')
CAPTURE = Path('work/emulation_v193/occupied_equipment_v308_corrected')
ROM = Path('out/all_routes_combined_v307_candidate.nds')
DIGEST = '61c64dba659daf74d6418842ef982f1517ddca8e4879deffda6da5b6c7980ff5'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    report_path = CAPTURE / 'capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256'] == DIGEST == sha(ROM.read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report['frames'] == 34400
    frames = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        if 'navigation' in row['path'] or 'final' in row['path']:
            frames[row['frame']] = row
    rom = NdsImage.open(ROM)
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    shot = Image.open(frames[34400]['path']).convert('RGB')
    label = 'Travels of Marco Polo'
    ink, bounds = complete_mask(font, label, shot, 96, 210, (0, 8, 0))
    assert ink == 223
    expected = {(96 + n * 6 + x, 210 + y) for n, c in enumerate(label)
                for y in range(11) for x in range(6) if font.decode(c).getpixel((x, y))}
    actual = {(x, y) for y in range(208, 224) for x in range(94, 224)
              if shot.getpixel((x, y)) == (0, 8, 0)}
    assert actual == expected
    palette = PxlImage.from_bytes(rom.read_file('/_pxl/towninfo.pxl')).palette
    tile = paper(130, 16, palette)
    for y in range(16):
        for x in range(130):
            point = (94 + x, 208 + y)
            rgb = (0, 8, 0) if point in expected else palette[tile[y * 130 + x]][:3]
            assert native5(shot.getpixel(point)) == native5(rgb), point
    atlas = PxlImage.from_bytes(rom.read_file('/_pxl/item.pxl')).render().convert('RGB')
    assert [native5(c) for c in shot.crop((112, 224, 144, 256)).get_flattened_data()] == [
        native5(c) for c in atlas.crop((0, 88 * 32, 32, 89 * 32)).get_flattened_data()]
    name = find_mask(font, 'Rafael Castor', shot, (82, 20, 255, 55))
    skills = []
    for text, x, y in [('Command', 16, 272), ('Sailing', 96, 272), ('Survey', 176, 272),
                       ('Finance', 16, 296), ('Observe', 96, 296), ('Vigor', 176, 296),
                       ('Aim', 16, 320), ('Swords', 96, 320), ('Speech', 176, 320), ('Guile', 16, 344)]:
        value = numeric_field(font, shot, x + 42, y)
        count, box = complete_mask(font, f'{text:>7}{value:3d}', shot, x, y, (230, 230, 230))
        skills.append({'text': text, 'value': value, 'bounds': box, 'complete_ink_pixels': count})
    plaques = []
    for number, batch_path in [(31600, 'translations/assign_sailors_graphics_v5.json'),
                               (34400, 'translations/person_info_graphics_v3.json')]:
        batch = read(batch_path)
        asset = PxlImage.from_bytes(rom.read_file(batch['file_path']))
        assert asset.source == NdsImage.open('out/all_routes_combined_v247_candidate.nds').read_file(batch['file_path'])
        image = Image.open(frames[number]['path']).convert('RGB')
        for row in batch['records']:
            left, top, right, bottom = row['plaque_box']
            for y in range(top, bottom):
                for x in range(left, right):
                    assert native5(image.getpixel((x, y))) == native5(asset.palette[asset.indices[y * asset.width + x]])
            plaques.append({'frame': number, 'English': row['text'], 'Japanese': row['source_japanese'],
                            'bounds': row['plaque_box'], 'whole_asset_pixels_exact': True, 'fully_completed': False})
    proof = {'candidate_unchanged': str(ROM), 'candidate_sha256': DIGEST,
             'capture_report': str(report_path), 'capture_report_sha256': sha(report_path.read_bytes()),
             'fresh_cold_boot_frames': 34400, 'savestate_loaded': False,
             'ordinary_Guild_purchase_and_inventory_Y_equip': True,
             'observed_purchase_confirmation_frame': 24400, 'observed_equipped_confirmation_frame': 30000,
             'book_source_item_index': 88, 'English': label, 'tooltip_bounds': [94, 208, 224, 224],
             'complete_tooltip_font_ink_pixels': ink, 'complete_tooltip_glyph_bounds': bounds,
             'exact_paper_lettering_and_corner_pixels': 2080, 'exact_original_book_icon_pixels': 1024,
             'complete_name': name, 'complete_skill_lines': skills, 'complete_plaque_instances': plaques,
             'current_Guild_stock_observed': ['Travels of Marco Polo', 'Sextant', 'map'],
             'weapon_and_armor_acquired_or_occupied_tooltips_verified': False,
             'failed_previous_navigation_retained_without_purchase_credit': 'work/emulation_v193/occupied_equipment_v308/capture_report.json',
             'all18_plaques_and_Armor_Weapon_variants_remain_incomplete': True,
             'low_resolution_Online_images_translation_exempt': True,
             'full_goal_complete': False, 'documentation': 'docs/occupied_equipment_v308.md'}
    proof_path = ROOT / 'live_proof.json'
    proof_path.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for filename in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / filename
        data = read(path)
        assert data['latest_candidate_sha256'] == DIGEST
        assert not data['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        group = data['plaque_style_v247']
        assert len(group['ongoing_plaque_inventory']) == 18 and not group['full_plaque_audit_complete']
        for row in group['ongoing_plaque_inventory']:
            assert not row['fully_completed']
            row['additional_V307_Rafael_purchase_context_proof'] = str(proof_path)
            for variant in row.get('observed_variants', []):
                assert not variant['fully_completed']
        data['occupied_equipment_audit_v308'] = {**proof, 'live_proof': str(proof_path)}
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    section = '''## V308: current occupied book and continued plaque audit

A fresh34,400-frame ordinary-input cold boot of V307 purchases and equips
Travels of Marco Polo. All223 tooltip ink pixels, all2,080 paper/glyph/corner
pixels, all1,024 original book icon pixels, Rafael Castor's full name, ten skill
lines and17 complete plaque surfaces pass exact pixel checks. No ROM change
is needed for these observed surfaces; V307 remains latest. All18 audit entries
and occupied Weapon/Armor contexts remain open. Equip confirmation splits
Marco across lines without losing letters; retain that word-wrap issue for
formatting review. Low resolution Online images remain exempt from translation.
See [V308 checkpoint](occupied_equipment_v308.md).

'''
    for filename in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs') / filename
        content = path.read_text(encoding='utf-8')
        if '## V308:' not in content:
            title, rest = content.split('\n\n', 1)
            path.write_text(title + '\n\n' + section + rest, encoding='utf-8')
    print(json.dumps({'candidate_unchanged': 'V307', 'tooltip_ink': ink, 'composite_pixels': 2080,
                      'book_icon_pixels': 1024, 'plaque_instances': len(plaques), 'skills': skills}))


if __name__ == '__main__':
    main()
