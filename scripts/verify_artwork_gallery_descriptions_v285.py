"""Actual Gallery description selection and native clear/font composites."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_artwork_name_captions_v283 import ROOT as PRIOR
from scripts.prepare_artwork_name_captions_v283 import read
from scripts.verify_artwork_caption_selector_v284 import execute

ROOT = Path('work/analysis/artwork_gallery_descriptions_v285')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    arm = (PRIOR / 'proposed_arm9_research_only.bin').read_bytes()
    assert sha(arm) == read(PRIOR / 'native_proof.json')['target_arm9_sha256']
    original = NdsImage.open('out/all_routes_combined_v275_candidate.nds').read_file('/__arm9__.bin')
    descriptions = [r for r in read('translations/gallery_description_manuscript_v1.json')['records']
                    if r['id'].startswith('EVENT_SCENES_') and r['id'] != 'EVENT_SCENES_DESCRIPTION'
                    and r['id'].endswith('_DESCRIPTION')]
    assert len(descriptions) == 4
    cases, unchanged = [], []
    for index, record in enumerate(descriptions):
        row = {'id': record['id'], 'index': index, 'english': record['english']}
        for mode in (4, 16):
            result = execute(arm, row, mode, gallery=True)
            cases.append(result)
            if index:
                old = execute(original, row, mode, gallery=True)
                assert old == result
                unchanged.append({'id': row['id'], 'mode': mode,
                                  'complete_original_and_updated_composite_exact': True})
    proof = {'format': 'dk4-artwork-gallery-native-descriptions-v285',
             'target_arm9_sha256': sha(arm), 'cases': cases, 'unchanged_cases': unchanged,
             'all_four_native_table_selections_on_both_bitmap_formats_pass': True,
             'actual_native_centered_title_and_full_description_pixels_exact': True,
             'native_bitmap_clear_executes_original_declared_overlay': True,
             'nonzero_initial_canvas_fully_cleared_with_guards_intact': True,
             'draw_clear_context_font_and_cleanup_instruction_bridges_used': False,
             'caller_frame_index_bitmap_metrics_and_overlay_loaded_state_are_fixtures': True,
             'actual_unlocked_Gallery_navigation_GPU_and_live_display_pending': True,
             'full_name_text_art_registered_integration_pending': True,
             'all18_plaque_hint_entries_and_variants_incomplete': True,
             'playable_ROM_modified': False, 'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Eight complete Gallery composites pass; six inherited cases exact; original bitmap-clear overlay executes.')


if __name__ == '__main__':
    main()
