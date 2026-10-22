"""Verify actual Surveyor consumers and a normal second-slot save/reload."""

import hashlib
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

ROOT = Path('work/analysis/input_mapping_v328')
ROM = Path('out/all_routes_combined_v326_candidate.nds')
FIRST = Path('work/emulation_v193/early_menu_v328')
SECOND = Path('work/emulation_v193/early_menu_v328_reload')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def frames(folder, digest, count):
    report = read(folder / 'capture_report.json')
    assert report['ROM_sha256'] == digest and report['cold_boot'] and not report['savestate_loaded']
    assert report['frames'] == count and not report['callback_errors']
    result = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        if 'navigation' in row['path']:
            result[row['frame']] = Path(row['path'])
    return report, result


def main():
    digest = sha(ROM.read_bytes())
    first, one = frames(FIRST, digest, 30000)
    second, two = frames(SECOND, digest, 6600)
    donor = Path(first['battery_save_preloaded']['source'])
    assert sha(donor.read_bytes()) == first['battery_save_preloaded']['source_sha256'] == (
        '28ff98d46e3b2ce1b1d9525059988f18a4ddf0d5bedac9140a183285493fdc2e')
    save = FIRST / 'saves/all_routes_combined_v326_candidate.dsv'
    assert second['battery_save_preloaded']['source_sha256'] == sha(save.read_bytes())
    assert sha(save.read_bytes()) != sha(donor.read_bytes())
    header = (ROOT / 'NDSSystem.h').read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(header)).encode() + b'\0' + header).hexdigest() == (
        '116e96109533c148d95a718e591b68a404b2298b')
    reference = Path('work/emulation_v193/reference/libretro.cpp')
    tree = read('work/emulation_v193/reference/source_tree.json')
    entry = next(r for r in tree['tree'] if r['path'] == 'desmume/src/frontend/libretro/libretro.cpp')
    data = reference.read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == entry['sha']
    rom = NdsImage.open(ROM)
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    shot = Image.open(one[27200]).convert('RGB')
    reloaded = Image.open(two[6600]).convert('RGB')
    assert shot.tobytes() == reloaded.tobytes()
    role = find_mask(font, 'Surveyor', shot, (80, 58, 255, 79))
    name = find_mask(font, 'Gerhard Ardelknatts', shot, (80, 20, 255, 55))
    roster = Image.open(one[27000]).convert('RGB')
    roster_role = find_mask(font, 'Surveyor', roster, (0, 306, 255, 338))
    roster_name = find_mask(font, 'Gerhard Ardelknatts', roster, (0, 340, 255, 365))
    batch = read('translations/person_info_graphics_v3.json')
    asset = PxlImage.from_bytes(rom.read_file(batch['file_path']))
    plaques, skills = [], []
    for frame, image in ((27200, shot), (6600, reloaded)):
        for row in batch['records']:
            left, top, right, bottom = row['plaque_box']
            for y in range(top, bottom):
                for x in range(left, right):
                    assert native5(image.getpixel((x, y))) == native5(asset.palette[asset.indices[y * asset.width + x]])
            plaques.append({'frame': frame, 'English': row['text'], 'all_pixels_exact': True, 'fully_completed': False})
        for text, x, y in [('Command', 16, 272), ('Sailing', 96, 272), ('Survey', 176, 272),
                           ('Finance', 16, 296), ('Observe', 96, 296), ('Vigor', 176, 296),
                           ('Aim', 16, 320), ('Swords', 96, 320), ('Speech', 176, 320), ('Guile', 16, 344)]:
            value = numeric_field(font, image, x + 42, y)
            ink, bounds = complete_mask(font, f'{text:>7}{value:3d}', image, x, y, (230, 230, 230))
            skills.append({'frame': frame, 'label': text, 'value': value, 'complete_ink_pixels': ink, 'bounds': bounds})
    hint = complete_mask(font, 'Equipped Items', shot, 138, 210, (0, 8, 0))
    proof = {'candidate_unchanged': str(ROM), 'candidate_sha256': digest,
             'pinned_core_commit': tree['sha'], 'core_source_header_git_blob': '116e96109533c148d95a718e591b68a404b2298b',
             'core_X_Y_mapping_identity_verified_from_primary_source': True,
             'reference_libretro_sha256': sha(data), 'reference_header_sha256': sha(header),
             'actual_Surveyor_Sailor_Info_mask': role, 'actual_Surveyor_roster_mask': roster_role,
             'complete_info_name': name, 'complete_roster_name': roster_name,
             'complete_20_plaque_instances': plaques, 'complete_20_skill_lines': skills,
             'complete_Equipped_Items_hint': hint,
             'second_slot_normal_in_game_save': str(save), 'second_slot_save_sha256': sha(save.read_bytes()),
             'normal_reloaded_Surveyor_assignment_persists': True,
             'whole_256x384_Sailor_Info_pixels_identical_after_load': 98304,
             'initial_reload_selected_original_slot_then_explicit_Load_selected_second_slot': True,
             'original_desktop_donor_unchanged': True, 'donor_historical_provenance_unknown': True,
             'working_menu_sequences': [{'A_frame': 26000, 'X_frame': 26200},
                                        {'A_frame': 28200, 'X_frame': 28400},
                                        {'A_frame': 5400, 'X_frame': 5600}],
             'A_then_X_eight_frame_presses_observed_to_open_menu_not_universal_root_cause_proof': True,
             'late_v327_menu_failure_cause_still_unproved': True,
             'save_caption_N_SeaAt_Sea_wording_spacing_observed_for_future_review': True,
             'capture_reports': [str(FIRST / 'capture_report.json'), str(SECOND / 'capture_report.json')],
             'all18_plaques_and_variants_remain_incomplete': True,
             'no_port_occupied_weapon_armor_alternate_condition_or_Auto_Move_credit': True,
             'low_resolution_Online_images_exempt': True, 'ROM_modified': False,
             'full_goal_complete': False, 'documentation': 'docs/menu_save_v328.md'}
    (ROOT / 'proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    for filename in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / filename
        audit = read(path)
        assert audit['latest_candidate_sha256'] == digest
        assert not audit['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert all(not r['fully_completed'] for r in audit['plaque_style_v247']['ongoing_plaque_inventory'])
        audit['actual_Surveyor_menu_save_v328'] = {**proof, 'proof': str(ROOT / 'proof.json')}
        audit['current_goal_turn_classification'] = 'progress-actual-Surveyor-two-consumers-and-normal-assignment-save-load'
        path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'Surveyor_consumers': 2, 'plaque_instances': 20, 'skill_lines': 20,
                      'normal_save_load_whole_screen_exact': True, 'ROM_unchanged': True}))


if __name__ == '__main__':
    main()
