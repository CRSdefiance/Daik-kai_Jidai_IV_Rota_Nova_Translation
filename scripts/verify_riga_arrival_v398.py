"""Normal Riga arrival/resupply and actual battery save/reload with complete labels."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.record_navigation_v327 import dark_text
from scripts.verify_commodity_layout_v346 import mask
from scripts.verify_plaque_release_v247 import find_mask

ROOT = Path('work/analysis/port_navigation_v396')
ROM = Path('out/all_routes_combined_v388_candidate.nds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def capture(folder, digest):
    path = folder / 'capture_report.json'
    report = read(path)
    assert report['ROM_sha256'] == digest
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    return path, report


def town(font, image):
    return {'header': [find_mask(font, text, image, region) for text, region in
                       [('Riga', (0, 10, 256, 40)), ('(N57 E23)', (0, 10, 256, 40)),
                        ('Bergstrom Fleet', (0, 80, 160, 110))]],
            'specialties': [mask(image, font, text, y) for text, y in
                            [('Wheat', 88), ('Furs', 104), ('Wax', 120)]]}


def main():
    digest = sha(ROM.read_bytes())
    assert digest == read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    original_path, original = capture(Path('work/emulation_v193/port_navigation_v396'), digest)
    reload_path, reload = capture(Path('work/emulation_v193/riga_reload_v398'), digest)
    assert original['frames'] == 12800 and reload['frames'] == 3200
    donor = original['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    saved = Path(donor['destination'])
    saved_digest = sha(saved.read_bytes())
    assert saved_digest != donor['source_sha256']
    assert reload['battery_save_preloaded']['source_sha256'] == saved_digest
    assert reload['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    inputs = original['scripted_input_schedule']
    assert {'start': 6001, 'duration': 2000, 'buttons': ['RIGHT']} in inputs
    assert {'start': 8001, 'duration': 250, 'buttons': ['DOWN', 'RIGHT']} in inputs
    assert {'start': 8251, 'duration': 90, 'buttons': ['DOWN']} in inputs
    assert {'start': 12001, 'duration': 8, 'buttons': ['A']} in inputs
    assert {'start': 12401, 'duration': 8, 'buttons': ['A']} in inputs
    assert reload['scripted_input_schedule'] == read(ROOT / 'reload_default_inputs.json')
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    folder = original_path.parent
    dock = Image.open(folder / 'frame_008340_navigation.png').convert('RGB')
    supply = Image.open(folder / 'frame_009200_navigation.png').convert('RGB')
    labels = [dark_text(font, 'Dock at Riga?', dock, (8, 292, 200, 320)),
              dark_text(font, 'Resupply?', supply, (8, 292, 200, 312)),
              dark_text(font, 'coins.', supply, (8, 310, 180, 340))]
    town_image = Image.open(folder / 'frame_008800_navigation.png').convert('RGB')
    reloaded = Image.open(reload_path.parent / 'frame_003200_final.png').convert('RGB')
    towns = [town(font, town_image), town(font, reloaded)]
    price = dark_text(font, 'Depart', Image.open(folder / 'frame_009600_navigation.png').convert('RGB'),
                      (70, 250, 180, 280))
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
             'arrival_report': str(original_path), 'arrival_report_sha256': sha(original_path.read_bytes()),
             'reload_report': str(reload_path), 'reload_report_sha256': sha(reload_path.read_bytes()),
             'normal_sailing_and_actual_Riga_docking': True, 'normal_resupply_confirmation': True,
             'actual_complete_prompt_masks': labels, 'actual_complete_depart_menu': price,
             'actual_arrival_and_reloaded_town_masks': towns,
             'funds_visually_observed_before': 44700, 'funds_visually_observed_after': 44552,
             'price_visually_observed': 148,
             'price_numeric_glyph_mask_and_independent_economy_arithmetic_not_proven': True,
             'new_save_through_normal_Save_menu': True, 'new_save_slot': 3,
             'saved_battery': str(saved), 'saved_battery_sha256': saved_digest,
             'original_donor_battery_unchanged_sha256': donor['source_sha256'],
             'initial_reload_v397_used_wrong_slot_not_credited': True,
             'reload_v398_default_remembered_slot3_reaches_Riga': True,
             'no_savestate_RAM_injection_or_synthetic_progression': True,
             'occupied_weapon_armor_and_unlocked_gallery_still_pending': True,
             'ROM_changed': False, 'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'arrival_reload_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Actual Riga arrival, resupply and Save/reload pass complete prompt/town/commodity labels; original donor unchanged.')


if __name__ == '__main__':
    main()
