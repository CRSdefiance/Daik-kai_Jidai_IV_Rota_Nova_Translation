"""Normal repair/save/reload and complete Ship Info plaque lettering."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_med_ports_v471 import town
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_portrait_native_pixels_v202 import native5

ROM = Path('out/all_routes_combined_v468_candidate.nds')
ROOT = Path('work/analysis/hull_recovery_v473')
CAPTURE = Path('work/emulation_v193/hull_recovery_v473')
RELOAD = Path('work/emulation_v193/genoa_repaired_reload_v473')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    rom = NdsImage.open(ROM)
    digest = sha(ROM.read_bytes())
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    reports = []
    for folder, count in [(CAPTURE, 23170), (RELOAD, 3800)]:
        path = folder / 'capture_report.json'
        report = read(path)
        assert report['ROM_sha256'] == digest and report['frames'] == count
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        reports.append((path, report))
    donor = reports[0][1]['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    saved = ROOT / 'genoa_repaired_test_copy.dsv'
    assert saved.read_bytes() == Path(donor['destination']).read_bytes()
    assert sha(saved.read_bytes()) == reports[1][1]['battery_save_preloaded']['source_sha256']
    before = Image.open(CAPTURE / 'frame_004200_navigation.png').convert('RGB')
    after = Image.open(CAPTURE / 'frame_014670_navigation.png').convert('RGB')
    loaded = Image.open(RELOAD / 'frame_003800_final.png').convert('RGB')
    hull = [find_mask(font, text, image, (45, 140, 95, 162))
            for text, image in [('36/60', before), ('60/60', after), ('60/60', loaded)]]
    plaques = read(Path('translations/ships_submenu_graphics_v2.json'))
    art = PxlImage.from_bytes(rom.read_file(plaques['file_path']))
    color = native5(art.palette[plaques['color_index']][:3])
    letters = []
    for image_name, image in [('damaged_Valencia', before), ('repaired_Genoa', after), ('cold_loaded_Genoa', loaded)]:
        for row in plaques['records']:
            x0, y0, x1, y1 = row['box']
            ink = {(x, y) for y in range(y0, y1) for x in range(x0, x1)
                   if art.indices[y * art.width + x] == plaques['color_index']}
            assert ink and all(native5(image.getpixel(p)) == color for p in ink)
            letters.append({'context': image_name, 'label': row['text'], 'bounds': row['box'],
                            'all_source_label_ink_pixels_preserved': len(ink)})
    supplies = [find_mask(font, '150', loaded, region) for region in [(28, 43, 70, 63), (95, 43, 132, 63)]]
    ports = []
    for frame, name, coords, goods in [
        (9440, 'Marseille', '(N43 E4)', ['Cheese', 'Salt', 'Saffron', 'Inlaid Ware']),
        (12070, 'Genoa', '(N44 E8)', ['Cheese', 'WoolCl.', 'Armor']),
    ]:
        image = Image.open(CAPTURE / f'frame_{frame:06d}_navigation.png').convert('RGB')
        ports.append({'frame': frame, 'complete_masks': town(font, image, name, coords, goods)})
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'ROM_changed': False,
             'reports': [{'path': str(p), 'sha256': sha(p.read_bytes())} for p, _ in reports],
             'all_capture_hashes_verified': True, 'normal_repair_36_to60_then_completed_save_cold_loaded': hull,
             'all33_Ship_Info_label_ink_instances_preserved': letters,
             'full_paper_composition_not_claimed_where_native_values_overlay_art': True,
             'full_water_food_numeric_masks_after_cold_load': supplies,
             'normal_Marseille_Genoa_town_masks': ports, 'original_Valencia_donor_unchanged': True,
             'saved_battery': str(saved), 'saved_battery_sha256': sha(saved.read_bytes()),
             'repair_message_word_wait_splits_across_lines_pending_followup': True,
             'prior_claims_Valencia_Marseille_lacked_Yard_not_established': True,
             'occupied_Weapon_remains_open': True, 'all22_historical_requirements_retained': True,
             'all18_plaques_incomplete': True, 'hardware_verification': False, 'full_goal_complete': False}
    (ROOT / 'hull_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Normal repaired hull/save/cold load,33 complete plaque ink instances and Marseille/Genoa labels pass.')


if __name__ == '__main__':
    main()
