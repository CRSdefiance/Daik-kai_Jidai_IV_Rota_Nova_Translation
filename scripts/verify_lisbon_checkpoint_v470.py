"""Normal Lisbon recovery/save and a cold-loaded Relaxed occupied-Armor context."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_plaque_style_v247 import paper
from scripts.record_navigation_v327 import dark_text
from scripts.verify_commodity_layout_v346 import mask
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_occupied_armor_v469 import state
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_portrait_native_pixels_v202 import native5

ROM = Path('out/all_routes_combined_v468_candidate.nds')
ROOT = Path('work/analysis/weapon_clues_v470')
CAPTURE = Path('work/emulation_v193/weapon_voyage_v470')
RELOAD = Path('work/emulation_v193/lisbon_reload_v470')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    digest = sha(ROM.read_bytes())
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    reports = []
    for folder, frames in [(CAPTURE, 30840), (RELOAD, 3800)]:
        p = folder / 'capture_report.json'
        r = read(p)
        assert r['ROM_sha256'] == digest and r['frames'] == frames
        assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
        for row in r['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        reports.append((p, r))
    donor = Path(reports[0][1]['battery_save_preloaded']['source'])
    assert sha(donor.read_bytes()) == reports[0][1]['battery_save_preloaded']['source_sha256']
    saved = Path(reports[0][1]['battery_save_preloaded']['destination'])
    copied = ROOT / 'lisbon_test_copy.dsv'
    assert saved.read_bytes() == copied.read_bytes()
    assert sha(copied.read_bytes()) == reports[1][1]['battery_save_preloaded']['source_sha256']
    messages = []
    for frame, lines in [(4075, ['Admiral, rats are all over the ship!', 'Our food is in danger!']),
                         (4535, ['The expedition found nothing nearby.']),
                         (4735, ["We've run out", 'of Food!']), (4955, ["We've run out", 'of Water!']),
                         (6240, ['Shall we call at Lisbon?']),
                         (10540, ['Ship fixed. Debt paid. Thanks.']),
                         (14540, ['Sir Rocco Alemkel.']),
                         (26740, ['Overwrite existing data?', 'Continue?'])]:
        image = Image.open(CAPTURE / f'frame_{frame:06d}_navigation.png').convert('RGB')
        messages.extend({'frame': frame, 'mask': dark_text(font, text, image, (8, 292, 253, 350))}
                        for text in lines)
    fatigue = []
    for frame, value in [(13840, '64'), (21640, '54'), (24440, '0')]:
        image = Image.open(CAPTURE / f'frame_{frame:06d}_navigation.png').convert('RGB')
        fatigue.append({'frame': frame, 'mask': find_mask(font, value, image, (150, 344, 220, 366))})
    town = Image.open(RELOAD / 'frame_003200_navigation.png').convert('RGB')
    town_masks = {'name': find_mask(font, 'Lisbon', town, (0, 10, 256, 40)),
                  'coordinates': find_mask(font, '(N38 W8)', town, (0, 10, 256, 40)),
                  'goods': [mask(town, font, text, y) for text, y in
                            [('Salt', 88), ('Olive Oil', 104), ('Saffron', 120), ('Almond', 136), ('Guns', 152)]],
                  'zero_indicator': find_mask(font, '0', town, (150, 344, 220, 366))}
    shot = Image.open(RELOAD / 'frame_003800_final.png').convert('RGB')
    owner = find_mask(font, 'Hodram Joakim Bergstrom', shot, (80, 16, 256, 60))
    mood = find_mask(font, 'Relaxed', shot, (48, 120, 125, 150))
    ink, bounds = complete_mask(font, 'Blue Oak Shield', shot, 66, 210, (0, 8, 0))
    assert ink == 182 and bounds == [66, 210, 156, 221]
    expected = {(66 + n * 6 + x, 210 + y) for n, c in enumerate('Blue Oak Shield')
                for y in range(11) for x in range(6) if font.decode(c).getpixel((x, y))}
    palette = PxlImage.from_bytes(rom.read_file('/_pxl/towninfo.pxl')).palette
    tile = paper(94, 16, palette)
    for y in range(16):
        for x in range(94):
            p = 64 + x, 208 + y
            rgb = (0, 8, 0) if p in expected else palette[tile[y * 94 + x]][:3]
            assert native5(shot.getpixel(p)) == native5(rgb)
    atlas = PxlImage.from_bytes(rom.read_file('/_pxl/item.pxl')).render().convert('RGB')
    assert [native5(c) for c in shot.crop((64, 224, 96, 256)).get_flattened_data()] == [
        native5(c) for c in atlas.crop((0, 49 * 32, 32, 50 * 32)).get_flattened_data()]
    batch = read(Path('translations/person_info_graphics_v3.json'))
    asset = PxlImage.from_bytes(rom.read_file(batch['file_path']))
    for row in batch['records']:
        x0, y0, x1, y1 = row['plaque_box']
        assert all(native5(shot.getpixel((x, y))) == native5(asset.palette[asset.indices[y * asset.width + x]][:3])
                   for y in range(y0, y1) for x in range(x0, x1))
    armor = state(arm, RELOAD / 'final_arm9_ram.bin')
    assert (armor['found_flag'], armor['category'], armor['owner_descriptor_type'], armor['owner_index_if_equipped']) == (2, 3, 2, 1)
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'ROM_changed': False,
             'reports': [{'path': str(p), 'sha256': sha(p.read_bytes()), 'capture_count': len(r['frames_captured'])}
                         for p, r in reports], 'complete_shortage_search_and_Lisbon_scene_messages': messages,
             'normal_Inn_one_night64_to54_then30_nights_to0_complete_masks': fatigue,
             'normal_Lisbon_arrival_and_saved_town': town_masks,
             'departure_About38_days_observed_after_recovery_not_independent_supply_arithmetic': True,
             'reloaded_Hodram_Relaxed_Armor_context': {'owner': owner, 'mood': mood, 'tooltip_bounds': bounds,
                                                      'tooltip_ink': ink, 'paper_pixels': 1504, 'icon_pixels': 1024,
                                                      'all10_person_plaques_exact': True},
             'original_reloaded_Armor_state': armor,
             'normal_slot6_save_completed_with4100_extra_frames_then_cold_loaded': True,
             'saved_battery': str(copied), 'saved_battery_sha256': sha(copied.read_bytes()),
             'original_equipped_Armor_donor_unchanged': True,
             'Janus_loan_and_Rocco_scenes_normal_gameplay_no_weapon_acquisition_claim': True,
             'weapon_owned_or_occupied_verified': False, 'all18_plaques_incomplete': True,
             'all22_historical_requirements_retained': True, 'hardware_verification': False, 'full_goal_complete': False}
    (ROOT / 'lisbon_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Lisbon normal recovery/save/reload,shortage and scene text,64->54->0 masks and Relaxed occupied Armor pixels pass.')


if __name__ == '__main__':
    main()
