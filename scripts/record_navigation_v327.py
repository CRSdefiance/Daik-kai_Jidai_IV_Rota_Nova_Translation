"""Record actual Survey assignment and the unsuccessful first-route voyage."""

import json
from collections import Counter
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_plaque_release_v247 import find_mask

ROOT = Path('work/analysis/navigation_v327')
CAPTURE = Path('work/emulation_v193/auto_move_v327')
ROM = Path('out/all_routes_combined_v326_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def dark_text(font, text, image, region):
    colors = [color for color, _ in Counter(image.crop(region).get_flattened_data()).most_common()
              if max(color) < 80][:4]
    for color in colors:
        for y in range(region[1], region[3] - 10):
            for x in range(region[0], region[2] - len(text) * 6 + 1):
                try:
                    ink, bounds = complete_mask(font, text, image, x, y, color)
                    return {'text': text, 'bounds': bounds, 'ink_pixels': ink, 'color': color,
                            'complete_ink_and_blank_cells_exact': True}
                except ValueError:
                    pass
    raise ValueError('No complete observed dark text: ' + text)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    report_path = CAPTURE / 'capture_report.json'
    report = read(report_path)
    digest = sha(ROM.read_bytes())
    assert report['ROM_sha256'] == digest and report['cold_boot'] and not report['savestate_loaded']
    assert report['frames'] == 33100 and not report['callback_errors']
    donor = Path(report['battery_save_preloaded']['source'])
    assert sha(donor.read_bytes()) == report['battery_save_preloaded']['source_sha256']
    frames = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        if 'navigation' in row['path']:
            frames[row['frame']] = row
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    assignment = Image.open(frames[15600]['path']).convert('RGB')
    labels = [find_mask(font, 'Survey', assignment, (70, 20, 255, 45)),
              find_mask(font, 'Gerhard Ardelknatts', assignment, (70, 36, 255, 65))]
    confirm = dark_text(font, 'Confirm crew assignment?',
                        Image.open(frames[16000]['path']).convert('RGB'), (10, 292, 252, 322))
    no_route = Image.open(frames[19200]['path']).convert('RGB')
    route_lines = [dark_text(font, 'There is no route', no_route, (10, 292, 252, 317)),
                   dark_text(font, 'to that city.', no_route, (10, 308, 252, 337))]
    footer = []
    for number in (25200, 29000):
        image = Image.open(frames[number]['path']).convert('RGB')
        for text, region in [('Rotate', (15, 366, 88, 384)), ('Inspect', (110, 366, 199, 384)),
                             ('Sails', (198, 366, 256, 384))]:
            footer.append({'frame': number, **find_mask(font, text, image, region)})
    proof = {'candidate_unchanged': str(ROM), 'candidate_sha256': digest,
             'capture_report': str(report_path), 'capture_report_sha256': sha(report_path.read_bytes()),
             'ordinary_cold_boot_frames': report['frames'], 'savestate_loaded': False,
             'donor_save_source_unchanged': True, 'donor_save_provenance_unknown': True,
             'actual_gerhard_Survey_assignment': {'source_room': 'Mate', 'target_room': 'Survey',
                                                'displayed_skill': 124, 'displayed_requirement': 120,
                                                'selected_eligible_room_frame': 15200,
                                                'placed_frame': 15600, 'confirmed_by_A_at_frame': 16800,
                                                'complete_labels': labels, 'complete_confirmation': confirm},
             'actual_Hamburg_Auto_Move_request': {'destination_frame': 18400,
                                                  'source_coordinates_visually_observed': 'N53 E8',
                                                  'confirmation_frame': 18800, 'result_frame': 19200,
                                                  'result': 'There is no route to that city.',
                                                  'complete_result_lines': route_lines},
             'automatic_sailing_or_Stop_Auto_Move_actual_context_reached': False,
             'manual_sailing_reached': True, 'complete_retained_sailing_caption_masks': footer,
             'visually_observed_coordinate_checkpoints': [
                 {'frame': 25200, 'coordinates': [58, 18]}, {'frame': 26000, 'coordinates': [59, 22]},
                 {'frame': 27000, 'coordinates': [57, 20]}, {'frame': 28400, 'coordinates': [55, 18]},
                 {'frame': 29000, 'coordinates': [55, 16]}, {'frame': 29800, 'coordinates': [55, 14]},
                 {'frame': 31100, 'coordinates': [56, 14]}, {'frame': 32400, 'coordinates': [55, 14]}],
             'coordinate_numbers_visually_observed_not_independent_font_masks': True,
             'port_arrival_or_weapon_armor_acquisition': False,
             'terrain_stall_and_weather_interruptions_retained_as_unsuccessful_navigation': True,
             'later_Menu_attempts_did_not_open_no_crew_condition_or_save_credit': True,
             'all18_plaques_and_variants_remain_incomplete': True,
             'low_resolution_Online_images_exempt': True, 'ROM_modified': False,
             'full_goal_complete': False, 'documentation': 'docs/navigation_v327.md'}
    proof_path = ROOT / 'proof.json'
    proof_path.write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / name
        audit = read(path)
        assert audit['latest_candidate_sha256'] == digest
        assert not audit['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert all(not entry['fully_completed'] for entry in audit['plaque_style_v247']['ongoing_plaque_inventory'])
        audit['actual_Survey_assignment_navigation_v327'] = {**proof, 'proof': str(proof_path)}
        audit['current_goal_turn_classification'] = 'progress-actual-Survey-assignment-route-gate-and-manual-control-evidence'
        path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'actual_assignment': True, 'complete_footer_masks': len(footer),
                      'Auto_Move_started': False, 'port_arrival': False, 'ROM_unchanged': True}))


if __name__ == '__main__':
    main()
