"""Verify actual complete Inspect footer and the ordinary target-information action."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_sea_inspect_v322 import ROOT
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_sea_inspect_v322 import ROM, read


def main():
    proof = read(ROOT / 'release_proof.json')
    report_path = Path('work/emulation_v193/sea_inspect_v322/capture_report.json')
    report = read(report_path)
    assert report['ROM_sha256'] == proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 31200
    assert report['scripted_input_schedule'] == read(ROOT / 'cold_boot_inputs.json')
    frames = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        frames[row['frame']] = row
    font = GameAsciiFont.from_arm9((ROOT / 'research_arm9.bin').read_bytes())
    captions = []
    for number in (30400, 30800):
        image = Image.open(frames[number]['path']).convert('RGB')
        captions.append({'frame': number, **find_mask(font, 'Inspect', image, (110, 366, 199, 384))})
        for region in ((15, 366, 88, 384), (198, 366, 256, 384)):
            captions.append({'frame': number, **find_mask(font, 'Sails', image, region)})
    info = Image.open(frames[31200]['path']).convert('RGB')
    info_labels = [find_mask(font, 'Info Mode', info, (0, 0, 256, 25)),
                   find_mask(font, 'View information about the cities and', info, (0, 25, 256, 49)),
                   find_mask(font, 'ships on screen. Select a target.', info, (0, 40, 256, 70))]
    original_report = read('work/emulation_v193/ordinary_voyage_v321/capture_report.json')
    observed = next(row for row in original_report['frames_captured'] if row['frame'] == 11600)
    assert sha(Path(observed['path']).read_bytes()) == observed['PNG_sha256']
    assert info.crop((0, 0, 256, 192)).tobytes() == Image.open(observed['path']).convert('RGB').crop((0, 0, 256, 192)).tobytes()
    proof.update({'actual_display_verification_pending': False,
                  'actual_complete_Inspect_and_both_Sails_captions': captions,
                  'actual_button_enters_Info_Mode': True, 'Info_Mode_full_text_masks': info_labels,
                  'Info_Mode_upper_screen_exact_to_prechange_observed_action': True,
                  'fresh_title_New_Game_character_opening_town_and_sailing_exercised': True,
                  'cold_boot_frames': report['frames'], 'capture_report': str(report_path),
                  'capture_report_sha256': sha(report_path.read_bytes()),
                  'no_savestate_progress_flag_patch_or_live_RAM_injection': True,
                  'actual_Auto_Move_Stop_context_still_pending': True,
                  'all18_plaques_and_variants_remain_incomplete': True,
                  'low_resolution_Online_images_exempt': True,
                  'documentation': 'docs/sea_inspect_v322.md'})
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / name
        audit = read(path)
        assert not audit['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        for row in audit['plaque_style_v247']['ongoing_plaque_inventory']:
            assert not row['fully_completed']
            for variant in row.get('observed_variants', []):
                assert not variant['fully_completed']
        audit['sea_inspect_caption_v322'] = {**proof, 'release_proof': str(ROOT / 'release_proof.json')}
        audit['latest_candidate'], audit['latest_candidate_sha256'] = str(ROM), proof['candidate_sha256']
        audit['current_goal_turn_classification'] = 'progress-contextual-sailing-Inspect-caption-integrated-and-actual-action-verified'
        path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'complete_live_caption_masks': len(captions), 'Info_Mode_masks': len(info_labels),
                      'goal_complete': False, 'candidate': str(ROM)}))


if __name__ == '__main__':
    main()
