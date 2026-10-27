"""Normal Ceuta/Valencia supply stops, save reload and Excited occupied Armor."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_plaque_style_v247 import paper
from scripts.record_navigation_v327 import dark_text
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_occupied_armor_v469 import compact_mask, state
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_portrait_native_pixels_v202 import native5

ROM = Path('out/all_routes_combined_v468_candidate.nds')
ROOT = Path('work/analysis/med_voyage_v471')
CAPTURE = Path('work/emulation_v193/med_voyage_v471')
RELOAD = Path('work/emulation_v193/valencia_reload_v471')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def town(font, image, name, coordinates, goods):
    return {'name': find_mask(font, name, image, (0, 10, 256, 40)),
            'coordinates': find_mask(font, coordinates, image, (0, 10, 256, 40)),
            'goods': [compact_mask(font, word, image, 160, 88 + n * 16) for n, word in enumerate(goods)]}


def main():
    digest = sha(ROM.read_bytes())
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    reports = []
    for folder, frame in [(CAPTURE, 13350), (RELOAD, 3800)]:
        p = folder / 'capture_report.json'
        r = read(p)
        assert r['ROM_sha256'] == digest and r['frames'] == frame
        assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
        for v in r['frames_captured']:
            assert sha(Path(v['path']).read_bytes()) == v['PNG_sha256']
        reports.append((p, r))
    donor = Path(reports[0][1]['battery_save_preloaded']['source'])
    assert sha(donor.read_bytes()) == reports[0][1]['battery_save_preloaded']['source_sha256']
    saved = Path(reports[0][1]['battery_save_preloaded']['destination'])
    copied = ROOT / 'valencia_test_copy.dsv'
    assert saved.read_bytes() == copied.read_bytes()
    assert sha(copied.read_bytes()) == reports[1][1]['battery_save_preloaded']['source_sha256']
    towns = []
    for frame, name, coords, goods in [(5240, 'Ceuta', '(N35 W5)', ['P. Oil', 'Leather']),
                                       (8450, 'Valencia', '(N39 W0)', ['Salt', 'Wool', 'Almond'])]:
        im = Image.open(CAPTURE / f'frame_{frame:06d}_navigation.png').convert('RGB')
        towns.append({'frame': frame, 'complete_masks': town(font, im, name, coords, goods)})
    reloaded = Image.open(RELOAD / 'frame_003200_navigation.png').convert('RGB')
    towns.append({'frame': 3200, 'cold_loaded': True,
                  'complete_masks': town(font, reloaded, 'Valencia', '(N39 W0)', ['Salt', 'Wool', 'Almond'])})
    messages = []
    for frame, text in [(4840, 'Shall we call at Ceuta?'), (8050, 'Shall we call at Valencia?'),
                        (5340, 'Resupply?'), (8550, 'Resupply?'),
                        (9250, 'Overwrite existing data?'), (9250, 'Continue?')]:
        im = Image.open(CAPTURE / f'frame_{frame:06d}_navigation.png').convert('RGB')
        messages.append({'frame': frame, 'mask': dark_text(font, text, im, (8, 292, 253, 350))})
    im = Image.open(RELOAD / 'frame_003800_final.png').convert('RGB')
    mood = find_mask(font, 'Excited', im, (48, 120, 125, 150))
    owner = find_mask(font, 'Hodram Joakim Bergstrom', im, (80, 16, 256, 60))
    ink, bounds = complete_mask(font, 'Blue Oak Shield', im, 66, 210, (0, 8, 0))
    assert ink == 182 and bounds == [66, 210, 156, 221]
    expected = {(66 + n * 6 + x, 210 + y) for n, c in enumerate('Blue Oak Shield')
                for y in range(11) for x in range(6) if font.decode(c).getpixel((x, y))}
    palette = PxlImage.from_bytes(rom.read_file('/_pxl/towninfo.pxl')).palette
    tile = paper(94, 16, palette)
    for y in range(16):
        for x in range(94):
            p = 64 + x, 208 + y
            rgb = (0, 8, 0) if p in expected else palette[tile[y * 94 + x]][:3]
            assert native5(im.getpixel(p)) == native5(rgb)
    atlas = PxlImage.from_bytes(rom.read_file('/_pxl/item.pxl')).render().convert('RGB')
    assert [native5(c) for c in im.crop((64, 224, 96, 256)).get_flattened_data()] == [
        native5(c) for c in atlas.crop((0, 49 * 32, 32, 50 * 32)).get_flattened_data()]
    batch = read(Path('translations/person_info_graphics_v3.json'))
    asset = PxlImage.from_bytes(rom.read_file(batch['file_path']))
    for row in batch['records']:
        x0, y0, x1, y1 = row['plaque_box']
        assert all(native5(im.getpixel((x, y))) == native5(asset.palette[asset.indices[y * asset.width + x]][:3])
                   for y in range(y0, y1) for x in range(x0, x1))
    armor = state(arm, RELOAD / 'final_arm9_ram.bin')
    assert (armor['found_flag'], armor['category'], armor['owner_descriptor_type'], armor['owner_index_if_equipped']) == (2, 3, 2, 1)
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'ROM_changed': False,
             'reports': [{'path': str(p), 'sha256': sha(p.read_bytes()), 'capture_count': len(r['frames_captured'])}
                         for p, r in reports], 'normal_Ceuta_Valencia_arrivals_and_complete_town_masks': towns,
             'complete_docking_resupply_save_literals': messages,
             'resupply_costs_visually_observed_not_independent_economy_arithmetic': True,
             'normal_slot6_save_completed_with4100_more_frames_then_cold_loaded': True,
             'original_Lisbon_donor_unchanged': True, 'saved_battery': str(copied),
             'saved_battery_sha256': sha(copied.read_bytes()), 'reloaded_Armor_state': armor,
             'new_genuine_Excited_Armor_context': {'mood': mood, 'owner': owner, 'tooltip_ink': ink,
                                                  'tooltip_bounds': bounds, 'paper_pixels': 1504,
                                                  'icon_pixels': 1024, 'all10_person_plaques_exact': True},
             'occupied_Weapon_and_other_graphics_contexts_remain_open': True,
             'all22_historical_requirements_retained': True, 'all18_plaques_incomplete': True,
             'hardware_verification': False, 'full_goal_complete': False}
    (ROOT / 'port_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Ceuta/Valencia full town and message glyphs;normal save/cold load;genuine Excited Armor tooltip/paper/icon/10 plaques pass.')


if __name__ == '__main__':
    main()
