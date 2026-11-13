"""Verify unchanged V378 sailor plaques and an actual alternate voyage mood."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_short_equipment_release_v252 import numeric_field

ROOT = Path('work/analysis/plaque_voyage_v379')
CAPTURE = Path('work/emulation_v193/plaque_voyage_v379')
ROM = Path('out/all_routes_combined_v378_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    report_path = CAPTURE / 'capture_report.json'
    report = read(report_path)
    digest = sha(ROM.read_bytes())
    assert digest == report['ROM_sha256'] == read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 15600
    for entry in report['frames_captured']:
        assert sha(Path(entry['path']).read_bytes()) == entry['PNG_sha256']
    rom = NdsImage.open(ROM)
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    batch = read('translations/person_info_graphics_v3.json')
    art = PxlImage.from_bytes(rom.read_file(batch['file_path']))
    cases = []
    for frame, name, mood in [
        (12000, 'Hodram Joakim Bergstrom', 'Normal'),
        (13200, 'Gerhard Ardelknatts', 'Upset'),
        (14400, 'Manuel Almeida', 'Normal'),
        (15600, 'Charles Jean Rochefort', 'Normal'),
    ]:
        path = CAPTURE / f'frame_{frame:06d}_navigation.png'
        image = Image.open(path).convert('RGB')
        assert image.size == (256, 384)
        regions = []
        for row in batch['records']:
            x0, y0, x1, y1 = row['plaque_box']
            for y in range(y0, y1):
                for x in range(x0, x1):
                    expected = art.palette[art.indices[y * 256 + x]][:3]
                    assert tuple(c // 8 for c in image.getpixel((x, y))) == tuple(c // 8 for c in expected)
            regions.append(row['plaque_box'])
        statuses = []
        for label, text, y in [('Health', 'Healthy', 108), ('Mood', mood, 128)]:
            ink, bounds = complete_mask(font, text, image, 56, y, (230, 230, 230))
            statuses.append({'label': label, 'text': text, 'ink_pixels': ink, 'bounds': bounds})
        skills = []
        for label, x, y in [
            ('Command', 16, 272), ('Sailing', 96, 272), ('Survey', 176, 272),
            ('Finance', 16, 296), ('Observe', 96, 296), ('Vigor', 176, 296),
            ('Aim', 16, 320), ('Swords', 96, 320), ('Speech', 176, 320), ('Guile', 16, 344),
        ]:
            value = numeric_field(font, image, x + 42, y)
            ink, bounds = complete_mask(font, f'{label:>7}{value:3d}', image, x, y, (230, 230, 230))
            skills.append({'label': label, 'value': value, 'ink_pixels': ink, 'bounds': bounds})
        name_mask = find_mask(font, name, image, (80, 26, 256, 48))
        cases.append({'frame': frame, 'name': name, 'name_mask': name_mask, 'capture': str(path),
                      'PNG_sha256': sha(path.read_bytes()), 'statuses': statuses,
                      'all10_plaque_regions_exact': regions, 'all10_skill_lines_exact': skills})
    plaques = read('translations/graphics_completion_campaign_v1.json')['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not p['fully_completed'] for p in plaques)
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
             'capture_report': str(report_path), 'capture_report_sha256': sha(report_path.read_bytes()),
             'cold_boot_normal_controller_inputs_no_savestate_or_state_injection': True,
             'battery_save_history_unknown': True, 'cases': cases,
             'actual_alternate_mood_Upset_complete': True,
             'specific_action_causing_Upset_not_proven': True,
             'health_states_observed': ['Healthy'], 'mood_states_observed': ['Normal', 'Upset'],
             'complete_status_composites': 8, 'complete_plaque_composites': 40,
             'complete_skill_lines': 40, 'ROM_unchanged_no_new_candidate': True,
             'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'display_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('4 actual officers: full names, 8 status masks, 40 plaques and 40 skill lines pass; Upset observed.')


if __name__ == '__main__':
    main()
