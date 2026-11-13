"""Actual legitimate save/Ruins popup and corrected native Gallery text."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_gallery_menu_v307 import ROOT
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_gallery_release_v307 import ROM, read


def main():
    proof = read(ROOT / 'release_proof.json')
    report_path = Path('work/emulation_v193/gallery_menu_v307/capture_report.json')
    report = read(report_path)
    assert proof['candidate_sha256'] == report['ROM_sha256'] == sha(ROM.read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and report['frames'] == 31200
    assert report['scripted_input_schedule'] == read('work/analysis/gallery_access_v306/saved_route_inputs.json')
    frames = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        if 'cold_boot' in row['path']:
            frames[row['frame']] = row
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    popup = Image.open(frames[26000]['path']).convert('RGB')
    cases = []
    for text in ('Items', 'Ruins'):
        matches = []
        for y in range(265, 309):
            for x in range(100, 144):
                try:
                    ink, bounds = complete_mask(font, text, popup, x, y, (8, 8, 8))
                    matches.append((ink, bounds))
                except ValueError:
                    pass
        assert len(matches) == 1, (text, matches)
        ink, bounds = matches[0]
        assert 94 <= bounds[0] < bounds[2] <= 164 and 262 <= bounds[1] < bounds[3] <= 314
        cases.append({'text': text, 'bounds': bounds, 'all_first_internal_final_letter_pixels': ink,
                      'complete_blank_and_ink_cells_fit_original_native_popup': True})
    proof.update({'actual_legitimate_save_and_Ruins_popup_pending': False,
                  'current_cold_boot_frames': 31200, 'ordinary_new_save_and_title_gallery_access': True,
                  'capture_report': str(report_path), 'capture_report_sha256': sha(report_path.read_bytes()),
                  'actual_popup_label_cases': cases,
                  'source_native_unlock_flags_and_current_save_operation_unchanged': True,
                  'actual_hidden_Characters_Event_Scenes_unlock_and_full_popup_context_pending': True,
                  'actual_Items_Ruins_collection_is_empty_not_art_display_evidence': True,
                  'no_savestate_or_ROM_progress_flag_patches_or_RAM_injection': True,
                  'title_save_Gallery_popup_and_empty_collection_frames_visually_reviewed': [22400, 22800, 25200, 26000, 29600, 30800],
                  'experimental_user_acceptance_pending': True, 'full_goal_complete': False})
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    checkpoint = {**proof, 'documentation': 'docs/gallery_access_labels_v307.md',
                  'release_proof': str(ROOT / 'release_proof.json'),
                  'all16_native_gate_combinations_and_three_complete_label_rasters_verified': True,
                  'low_resolution_Online_images_exempt': True}
    access = read('work/analysis/gallery_access_v306/access_proof.json')
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / name
        data = read(path)
        assert not data['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert all(not r['fully_completed'] for r in data['plaque_style_v247']['ongoing_plaque_inventory'])
        data['actual_Gallery_access_v306'] = access
        data['Gallery_menu_labels_v307'] = checkpoint
        data['latest_candidate'], data['latest_candidate_sha256'] = str(ROM), proof['candidate_sha256']
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    section = '''## V306/V307: legitimate Gallery access and three missing menu labels

An ordinary new in-game save enables Continue/Grand Race/Gallery. This required
no ROM unlock patch or loaded state. Items/Ruins are available but currently
empty; Characters/Event Scenes remain gated by native system bits. Native source
menu labels were still Japanese:史跡/登場人物/イベントシーン. V307 translates them
as Ruins/Characters/Event Scenes inside original8/12/16-byte slots, with sole
pointer ownership and every native gate unchanged. All16 low-bit flag cases and
three complete glyph rasters pass. A fresh31200-frame ordinary save/title sequence
shows complete Items/Ruins popup pixels in the original bounds. All470 inherited
batches/art/data stay intact; only three ARM9 string slots change. Full V305
reproduces before/after the builder edit and the clean patch reconstructs exactly.
Experimental; hidden-view actual unlocks/collections, legacy display and all18
plaques remain open. Online images exempt. See [V307 evidence](gallery_access_labels_v307.md).

'''
    for name in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if '## V306/V307:' not in text:
            title, rest = text.split('\n\n', 1)
            path.write_text(title + '\n\n' + section + rest, encoding='utf-8')
    print(f'V307 actual source-gated Gallery popup recorded; Items/Ruins complete{sum(r["all_first_internal_final_letter_pixels"] for r in cases)} ink pixels; hidden views stay open.')


if __name__ == '__main__':
    main()
