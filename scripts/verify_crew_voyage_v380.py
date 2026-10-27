"""Verify complete saved-fleet Endurance values and seven plaque composites."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_plaque_release_v247 import find_mask

ROOT = Path('work/analysis/crew_voyage_v380')
CAPTURE = Path('work/emulation_v193/crew_voyage_v380')
ROM = Path('out/all_routes_combined_v378_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    report_path = CAPTURE / 'capture_report.json'
    report = read(report_path)
    digest = sha(ROM.read_bytes())
    assert digest == report['ROM_sha256'] == read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 8000
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    battery = report['battery_save_preloaded']
    assert sha(Path(battery['source']).read_bytes()) == battery['source_sha256']
    rom = NdsImage.open(ROM)
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    batch = read('translations/assign_sailors_graphics_v5.json')
    art = PxlImage.from_bytes(rom.read_file(batch['file_path']))
    cases = []
    for frame, action, caption, crew, reserve in [
        (7200, 'Opened Crew Setup', '~60 days', '19', '0'),
        (7600, 'Lo (L)', '~999 days', '0', '19'),
        (8000, 'Hi (R)', '~60 days', '19', '0'),
    ]:
        path = CAPTURE / f'frame_{frame:06d}_navigation.png'
        shot = Image.open(path).convert('RGB')
        assert shot.size == (256, 384)
        plaques = []
        for row in batch['records']:
            left, top, right, bottom = row['plaque_box']
            for y in range(top, bottom):
                for x in range(left, right):
                    expected = art.palette[art.indices[y * art.width + x]][:3]
                    assert tuple(c >> 3 for c in shot.getpixel((x, y))) == tuple(c >> 3 for c in expected)
            plaques.append({'label': row['text'], 'bounds': row['plaque_box'], 'all_pixels_exact': True})
        endurance = find_mask(font, caption, shot, (85, 37, 230, 61))
        fleet = find_mask(font, crew, shot, (90, 18, 126, 37))
        unassigned = find_mask(font, reserve, shot, (216, 18, 256, 37))
        cases.append({'frame': frame, 'action': action, 'endurance': endurance,
                      'fleet_crew': fleet, 'unassigned': unassigned, 'plaques': plaques,
                      'capture': str(path), 'PNG_sha256': sha(path.read_bytes())})
    assert cases[0]['endurance']['bounds'][:2] == cases[2]['endurance']['bounds'][:2]
    audit = read('translations/graphics_completion_campaign_v1.json')
    plaques = audit['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not p['fully_completed'] for p in plaques)
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
             'capture_report': str(report_path), 'capture_report_sha256': sha(report_path.read_bytes()),
             'cold_boot_normal_input_no_savestate_or_state_injection': True,
             'battery_save_history_unknown': True, 'cases': cases,
             'complete_actual_nonzero_Endurance_values': [60, 999],
             'complete_plaque_composites': 21, 'complete_count_masks': 6,
             'ROM_unchanged_no_new_candidate': True, 'all18_plaques_incomplete': True,
             'full_goal_complete': False, 'physical_device_verification': False}
    (ROOT / 'display_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('3 actual crew states: complete ~60/~999 days, 6 count masks and 21 plaque composites pass.')


if __name__ == '__main__':
    main()
