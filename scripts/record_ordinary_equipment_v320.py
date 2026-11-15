"""Verify actual V318 Sextant and four ordinary Sailor Info contexts."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_short_equipment_release_v252 import numeric_field

ROOT = Path('work/analysis/ordinary_equipment_v320')
CAPTURE = Path('work/emulation_v193/ordinary_equipment_v320')
ROM = Path('out/all_routes_combined_v318_candidate.nds')
DIGEST = '45b549eafee6a9cf3ff2d8a4e637f8722ebd52fb61dfa9b1dc5adab2fe6d1007'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    report_path = CAPTURE / 'capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256'] == DIGEST == sha(ROM.read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded']
    assert report['frames'] == 32000 and not report['callback_errors']
    assert report['battery_save_preloaded']['source_sha256'] == (
        '58d7c0d4cc43a43579cc218ef2a391a4a71fec83e77803924189b6d023ca8af0')
    frames = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        if 'navigation' in row['path']:
            frames[row['frame']] = Path(row['path'])
    rom = NdsImage.open(ROM)
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    batch = read('translations/person_info_graphics_v3.json')
    asset = PxlImage.from_bytes(rom.read_file(batch['file_path']))
    skills = [('Command', 16, 272), ('Sailing', 96, 272), ('Survey', 176, 272),
              ('Finance', 16, 296), ('Observe', 96, 296), ('Vigor', 176, 296),
              ('Aim', 16, 320), ('Swords', 96, 320), ('Speech', 176, 320),
              ('Guile', 16, 344)]
    cases = []
    for number, name, survey in [(22000, 'Julio Erneco', 110),
                                 (24000, 'Janus Pasar', 100),
                                 (25200, 'Claudio Manaus', 63),
                                 (26400, 'Rafael Castor', 80)]:
        shot = Image.open(frames[number]).convert('RGB')
        name_mask = find_mask(font, name, shot, (82, 20, 255, 55))
        labels = []
        for row in batch['records']:
            left, top, right, bottom = row['plaque_box']
            for y in range(top, bottom):
                for x in range(left, right):
                    assert native5(shot.getpixel((x, y))) == native5(
                        asset.palette[asset.indices[y * asset.width + x]])
            labels.append({'English': row['text'], 'Japanese': row['source_japanese'],
                           'bounds': row['plaque_box'], 'all_pixels_exact': True})
        values = []
        for text, x, y in skills:
            value = numeric_field(font, shot, x + 42, y)
            ink, bounds = complete_mask(font, f'{text:>7}{value:3d}', shot,
                                        x, y, (230, 230, 230))
            values.append({'label': text, 'value': value, 'bounds': bounds,
                           'ink_pixels': ink, 'ink_and_blank_cells_exact': True})
        assert next(v['value'] for v in values if v['label'] == 'Survey') == survey
        cases.append({'frame': number, 'name': name_mask, 'plaques': labels,
                      'skill_lines': values, 'fully_completed': False})
    tooltip_shot = Image.open(frames[22800]).convert('RGB')
    ink, bounds = complete_mask(font, 'Sextant', tooltip_shot, 114, 210, (213, 64, 16))
    tooltip = {'English': 'Sextant', 'frame': 22800, 'bounds': bounds,
               'color': [213, 64, 16], 'complete_ink_pixels': ink,
               'all_ink_and_blank_cells_exact': True}
    equipped_hint = complete_mask(font, 'Equipped Items',
                                 Image.open(frames[22000]).convert('RGB'),
                                 138, 210, (0, 8, 0))
    shop_shot = Image.open(frames[13600]).convert('RGB')
    icon = [native5(p) for p in shop_shot.crop((16, 24, 48, 56)).get_flattened_data()]
    assert rom.read_file('/_pxl/item.pxl') == NdsImage.open('work/clean.nds').read_file('/_pxl/item.pxl')
    atlas = PxlImage.from_bytes(rom.read_file('/_pxl/item.pxl')).render().convert('RGB')
    matches = [i for i in range(atlas.height // 32) if icon == [native5(p) for p in
               atlas.crop((0, i * 32, 32, (i + 1) * 32)).get_flattened_data()]]
    assert len(matches) == 1
    occupied_icon = [native5(p) for p in tooltip_shot.crop((112, 224, 144, 256)).get_flattened_data()]
    occupied_equal = sum(a == b for a, b in zip(icon, occupied_icon))
    assert occupied_equal == 864
    save = CAPTURE / 'saves/all_routes_combined_v318_candidate.dsv'
    assert len(save.read_bytes()) == 262266
    assert sha(save.read_bytes()) != report['battery_save_preloaded']['source_sha256']
    # Original input save is immutable; only the runner's isolated copy is saved.
    original = Path(report['battery_save_preloaded']['source'])
    assert sha(original.read_bytes()) == report['battery_save_preloaded']['source_sha256']
    reload_dir = Path('work/emulation_v193/ordinary_equipment_v320_reload')
    reload_report_path = reload_dir / 'capture_report.json'
    reload_report = read(reload_report_path)
    assert reload_report['ROM_sha256'] == DIGEST
    assert reload_report['cold_boot'] and not reload_report['savestate_loaded']
    assert reload_report['frames'] == 6400 and not reload_report['callback_errors']
    assert reload_report['battery_save_preloaded']['source_sha256'] == sha(save.read_bytes())
    for row in reload_report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    reload_shot = Image.open(reload_dir / 'frame_006400_navigation.png').convert('RGB')
    assert reload_shot.tobytes() == tooltip_shot.tobytes()
    proof = {'current_ROM_unchanged': str(ROM), 'ROM_sha256': DIGEST,
             'capture_report': str(report_path), 'capture_report_sha256': sha(report_path.read_bytes()),
             'ordinary_cold_boot_frames': 32000, 'savestate_loaded': False,
             'purchase_cost': 2500, 'observed_funds_after_purchase': 27400,
             'equipped_character': 'Julio Erneco', 'confirmation_frame': 19200,
             'Sextant_tooltip': tooltip, 'Equipped_Items_hint': equipped_hint,
             'original_item_icon_index': matches[0], 'exact_icon_pixels': 1024,
             'exact_unobscured_icon_frame': 13600,
             'occupied_icon_source_exact_pixels': occupied_equal,
             'occupied_icon_overlay_pixels': 1024 - occupied_equal,
             'occupied_icon_overlay_native_composition_not_certified': True,
             'Sailor_Info_contexts': cases,
             'ordinary_saved_progress': {'path': str(save), 'sha256': sha(save.read_bytes()),
                                         'original_source_save_unchanged': True,
                                         'reload_verification_pending': False,
                                         'reload_capture_report': str(reload_report_path),
                                         'reload_report_sha256': sha(reload_report_path.read_bytes()),
                                         'fresh_reload_frames': 6400,
                                         'occupied_Sextant_whole_screen_pixels_exact': 98304},
             'Auto_Move_unlocked': False, 'occupied_Weapon_Armor_verified': False,
             'low_resolution_Online_images_exempt': True, 'full_goal_complete': False,
             'limits': 'Targeted actual display checks. No voyage, weapon/armor, alternate mood or whole-game claim.'}
    proof_path = ROOT / 'live_proof.json'
    proof_path.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for filename in ['graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json']:
        path = Path('translations') / filename
        audit = read(path)
        assert audit['latest_candidate_sha256'] == DIGEST
        assert not audit['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        group = audit['plaque_style_v247']
        assert len(group['ongoing_plaque_inventory']) == 18
        assert not group['full_plaque_audit_complete']
        for row in group['ongoing_plaque_inventory']:
            assert not row['fully_completed']
            for variant in row.get('observed_variants', []):
                assert not variant['fully_completed']
        audit['ordinary_equipment_v320'] = {**proof, 'proof': str(proof_path)}
        path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'contexts': len(cases), 'plaque_instances': sum(len(c['plaques']) for c in cases),
                      'skill_lines': sum(len(c['skill_lines']) for c in cases),
                      'Sextant_complete_ink': ink, 'icon_index': matches[0],
                      'goal_complete': False}))


if __name__ == '__main__':
    main()
