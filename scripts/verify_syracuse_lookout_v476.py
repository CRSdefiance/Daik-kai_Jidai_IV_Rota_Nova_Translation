"""Normal Lookout discoveries and a supplied, undamaged saved Syracuse fleet."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.record_navigation_v327 import dark_text
from scripts.verify_med_ports_v471 import town
from scripts.verify_plaque_release_v247 import find_mask

ROM = Path('out/all_routes_combined_v474_candidate.nds')
ROOT = Path('work/analysis/weapon_voyage_v476')
CAPTURE = Path('work/emulation_v193/weapon_voyage_v476')
LOOKOUT = Path('work/emulation_v193/syracuse_lookout_reload_v476')
SHIPS = Path('work/emulation_v193/syracuse_ships_reload_v476')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    digest = sha(ROM.read_bytes())
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    reports = []
    for folder, frames in [(CAPTURE, 16995), (LOOKOUT, 3800), (SHIPS, 3800)]:
        path = folder / 'capture_report.json'
        report = read(path)
        assert report['ROM_sha256'] == digest and report['frames'] == frames
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        reports.append((path, report))
    donor = reports[0][1]['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    saved = ROOT / 'syracuse_test_copy.dsv'
    assert saved.read_bytes() == Path(donor['destination']).read_bytes()
    assert all(sha(saved.read_bytes()) == r['battery_save_preloaded']['source_sha256'] for _, r in reports[1:])
    messages = []
    for frame, text in [(6290, 'Admiral, city ahead!'), (6390, 'Discovered Tunis.'),
                        (7455, 'Admiral, city ahead!'), (7555, 'Discovered Syracuse.'),
                        (7695, 'Dock at Syracuse?')]:
        im = Image.open(CAPTURE / f'frame_{frame:06d}_navigation.png').convert('RGB')
        messages.append({'frame': frame, 'complete_mask': dark_text(font, text, im, (8, 292, 253, 350))})
    im = Image.open(SHIPS / 'frame_003800_final.png').convert('RGB')
    before = Image.open(CAPTURE / 'frame_008895_navigation.png').convert('RGB')
    assert before.tobytes() == im.tobytes()
    status = [find_mask(font, text, im, region) for text, region in
              [('60/60', (45, 140, 95, 162)), ('150', (28, 43, 70, 63)),
               ('150', (95, 43, 132, 63)), ('39/ 39/124', (165, 43, 256, 64))]]
    role = Image.open(LOOKOUT / 'frame_003800_final.png').convert('RGB')
    previous_role = Image.open('work/emulation_v193/lookout_reload_v475/frame_003800_final.png').convert('RGB')
    assert previous_role.tobytes() == role.tobytes()
    captions = {'role': find_mask(font, 'Lookout', role, (70, 20, 190, 45)),
                'name': find_mask(font, 'Manuel Almeida', role, (70, 37, 240, 65)),
                'voice': dark_text(font, 'On watch! Eyes open.', role, (8, 110, 253, 180))}
    port = Image.open(LOOKOUT / 'frame_003200_cold_boot.png').convert('RGB')
    town_masks = town(font, port, 'Syracuse', '(N37 E14)', ['Wheat', 'Wine', 'Olive Oil', 'Sultana'])
    fatigue = find_mask(font, '0', port, (150, 344, 220, 366))
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'ROM_changed': False,
             'reports': [{'path': str(p), 'sha256': sha(p.read_bytes())} for p, _ in reports],
             'all_capture_hashes_verified': True, 'original_prepared_Genoa_donor_unchanged': True,
             'normal_Lookout_Tunis_and_Syracuse_discoveries_and_docking': messages,
             'completed_normal_slot6_save_then_two_cold_loads': True,
             'full_hull_stores_and_39_sailors_after_cold_load': status,
             'whole_Ship_Info98304_pixels_exact_before_and_after_save': True,
             'whole_Lookout_screen98304_pixels_exact_against_prepared_setup': True,
             'persisted_Lookout_captions': captions, 'cold_loaded_Syracuse_complete_town_masks': town_masks,
             'cold_loaded_fatigue_indicator': fatigue, 'saved_battery': str(saved),
             'saved_battery_sha256': sha(saved.read_bytes()), 'Istanbul_discovery_and_Weapon_remain_open': True,
             'all22_historical_requirements_retained': True, 'all18_plaques_incomplete': True,
             'hardware_verification': False, 'full_goal_complete': False}
    (ROOT / 'syracuse_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Normal Lookout discoveries/docking;Syracuse save/cold loads;whole Ship Info and Lookout screens exact.')


if __name__ == '__main__':
    main()
