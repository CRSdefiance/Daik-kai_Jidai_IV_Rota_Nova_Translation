"""Actual complete Sea Map footer and inherited scene/control preservation."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_footer_v318 import ROOT
from scripts.verify_footer_release_v318 import ROM, read
from scripts.verify_plaque_release_v247 import find_mask


def main():
    proof = read(ROOT / 'release_proof.json')
    report_path = Path('work/emulation_v193/footer_measurement_v318/capture_report.json')
    report = read(report_path)
    source = read('work/emulation_v193/footer_measurement_v318_parent/capture_report.json')
    assert report['ROM_sha256'] == proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 32800 and report['scripted_input_schedule'] == source['scripted_input_schedule']
    frames = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        frames[row['frame']] = row
    font = GameAsciiFont.from_arm9((ROOT / 'research_arm9.bin').read_bytes())
    complete = []
    sails = []
    for number in (30400, 30800):
        image = Image.open(frames[number]['path']).convert('RGB')
        case = find_mask(font, 'Sea Map', image, (110, 366, 199, 384))
        complete.append({'frame': number, **case})
        for region in ((15, 366, 88, 384), (198, 366, 256, 384)):
            sails.append({'frame': number, **find_mask(font, 'Sails', image, region)})
    changed, unchanged, seen, animation = [], [], set(), []
    for row in source['frames_captured']:
        number = row['frame']
        if number not in frames or number in seen:
            continue
        seen.add(number)
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        before, after = Image.open(row['path']).convert('RGB'), Image.open(frames[number]['path']).convert('RGB')
        delta = [(x, y) for y in range(384) for x in range(256) if before.getpixel((x, y)) != after.getpixel((x, y))]
        if delta:
            outside = [(x, y) for x, y in delta if y < 356]
            if outside:
                assert number in (30400, 31600, 32000, 32400)
                assert before.crop((0, 192, 64, 216)).tobytes() == after.crop((0, 192, 64, 216)).tobytes()
                animation.append({'frame': number, 'nonfooter_pixels': len(outside),
                                  'sailing_HUD_date_strip_exact': True,
                                  'other_HUD_counts_visually_reviewed_not_all_pixels_claimed_exact': True,
                                  'captured_Sea_View_frames_visually_reviewed': True})
            changed.append({'frame': number, 'changed_pixels': len(delta), 'outside_footer_pixels': len(outside)})
        else:
            unchanged.append(number)
    assert changed and unchanged
    proof.update({'actual_complete_sailing_footer_pending': False, 'actual_Sea_Map_complete_font_cases': complete,
                  'actual_both_Sails_captions_complete_font_cases': sails,
                  'actual_Auto_Move_Stop_context_still_pending': True,
                  'actual_cold_boot_title_New_Game_opening_town_and_sailing_replayed': True,
                  'unchanged_comparable_whole_frames': unchanged, 'changed_comparable_frames': changed,
                  'capture_report': str(report_path), 'capture_report_sha256': sha(report_path.read_bytes()),
                  'comparison_exact_V316_parent_same_cold_boot_schedule': True,
                  'animated_Sea_View_frame_differences_not_claimed_as_footer_only': animation,
                  'no_savestate_progress_flag_patch_or_live_RAM_injection': True,
                  'all18_plaques_and_variants_remain_incomplete': True,
                  'low_resolution_Online_images_exempt': True, 'experimental_user_acceptance_pending': True,
                  'documentation': 'docs/footer_measurement_v318.md'})
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / name
        data = read(path)
        assert all(not r['fully_completed'] for r in data['plaque_style_v247']['ongoing_plaque_inventory'])
        assert not data['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        data['footer_measurement_release_v318'] = {**proof, 'release_proof': str(ROOT / 'release_proof.json')}
        data['latest_candidate'], data['latest_candidate_sha256'] = str(ROM), proof['candidate_sha256']
        data['current_goal_turn_classification'] = 'progress-integrated-footer-wide-last-cell-fix-and-actual-complete-Sea-Map'
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'Sea_Map_complete_native_cases': complete, 'changed_footer_frames': len(changed),
                      'unchanged_whole_frames': len(unchanged), 'candidate': str(ROM)}))


if __name__ == '__main__':
    main()
