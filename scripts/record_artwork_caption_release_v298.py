"""Record the verified caption candidate and scoped ordinary cold-boot evidence."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_artwork_caption_release_v298 import ROOT, read
from scripts.verify_artwork_caption_release_v298 import ROM


def main():
    proof = read(ROOT / 'release_proof.json')
    capture_path = Path('work/emulation_v193/artwork_captions_v298/capture_report.json')
    capture = read(capture_path)
    assert capture['ROM_sha256'] == proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert capture['cold_boot'] and not capture['savestate_loaded'] and not capture['callback_errors']
    assert capture['frames'] == 20000
    assert capture['scripted_input_schedule'] == read(ROOT / 'town_inputs.json')
    for row in capture['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    assert sha(Path(capture['read_only_RAM_snapshot']['path']).read_bytes()) == capture['read_only_RAM_snapshot']['sha256']
    old = read('work/emulation_v193/actor_integrity_v296_rafael/capture_report.json')
    old_frames = {r['frame']: r for r in old['frames_captured'] if 'cold_boot' in r['path']}
    frames = {r['frame']: r for r in capture['frames_captured'] if 'cold_boot' in r['path']}
    unchanged_title = []
    for n in (1, 60, 180, 400, 800, 1200):
        assert frames[n]['PNG_sha256'] == old_frames[n]['PNG_sha256']
        unchanged_title.append(n)
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    town = Image.open('work/emulation_v193/artwork_captions_v298/frame_020000_final.png').convert('RGB')
    lines = []
    for text, x, y in [('Bulk trade? Try the trade', 22, 296), ('house.', 22, 312)]:
        expected = {(x + n * 6 + gx, y + gy) for n, char in enumerate(text)
                    for gy in range(11) for gx in range(6) if font.decode(char).getpixel((gx, gy))}
        actual = {(gx, gy) for gy in range(y, y + 11) for gx in range(16, 248)
                  if max(town.getpixel((gx, gy))) < 20}
        assert actual == expected, (text, len(expected), len(actual))
        lines.append({'text': text, 'origin': [x, y], 'complete_native_ink_pixels': len(expected),
                      'all_first_internal_final_letters_and_bounds_exact': True})
    current_parent = Path('out/all_routes_combined_v296_candidate.nds').read_bytes()
    for path in ('work/analysis/reviewed_names_v297/v296_before_caption_builder_change.nds',
                 'work/analysis/artwork_caption_release_v298/v296_after_caption_builder_change.nds'):
        assert Path(path).read_bytes() == current_parent
    proof.update({'actual_targeted_cold_boot_pending': False,
                  'cold_boot_report': str(capture_path), 'cold_boot_report_sha256': sha(capture_path.read_bytes()),
                  'cold_boot_frames': capture['frames'],
                  'title_New_Game_Lil_selection_opening_Amsterdam_signs_and_shopkeeper_traversed': True,
                  'ordinary_inputs_no_loaded_state_no_RAM_injection': True,
                  'exact_unchanged_title_frames': unchanged_title,
                  'actual_shopkeeper_complete_lines': lines,
                  'screens_inspected': [1200, 2000, 6000, 20000],
                  'full_V296_reproduction_exact_before_and_after_builder_change': True,
                  'older_Kamil_nameplate_is_pending_V297_name_integration': True,
                  'full_goal_complete': False})
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    checkpoint = {k: proof[k] for k in (
        'candidate', 'candidate_sha256', 'patch', 'patch_sha256', 'profile', 'canonical_base',
        'all_inherited_batches', 'changed_vs_V296', 'all_original_native_actor_fields_preserved',
        'all_native_selector_centering_font_clear_overlay_bounds_and_guards_pass',
        'exact_clean_patch_reconstruction_pass', 'all_graphics_fonts_route_files_ARM7_and_overlays_exactV296',
        'cold_boot_frames', 'title_New_Game_Lil_selection_opening_Amsterdam_signs_and_shopkeeper_traversed',
        'ordinary_inputs_no_loaded_state_no_RAM_injection', 'actual_shopkeeper_complete_lines',
        'full_V296_reproduction_exact_before_and_after_builder_change',
        'unlocked_Gallery_and_original_deep_scene_navigation_pending',
        'V297_full_route_naming_integration_pending', 'all18_plaque_hint_entries_and_variants_incomplete',
        'older_Kamil_nameplate_is_pending_V297_name_integration', 'experimental_user_acceptance_pending',
        'full_goal_complete')}
    checkpoint.update({'documentation': 'docs/artwork_caption_release_v298.md',
                       'release_proof': str(ROOT / 'release_proof.json'),
                       'native_scene_cases': 328, 'native_Gallery_composite_cases': 8,
                       'updated_scene_captions': 15, 'updated_Gallery_descriptions': 1,
                       'low_resolution_Online_images_exempt': True})
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / name
        data = read(path)
        assert not data['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        plaques = data['plaque_style_v247']['ongoing_plaque_inventory']
        assert len(plaques) == 18 and all(not p['fully_completed'] for p in plaques)
        data['artwork_caption_release_v298'] = checkpoint
        data['latest_candidate'], data['latest_candidate_sha256'] = str(ROM), proof['candidate_sha256']
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    section = '''## V298: reviewed artwork captions integrated

The registered combined candidate integrates 15 scene captions and one Gallery
description using locked Rafael/Camille spellings. All 467 inherited batches,
graphics, fonts, route files, ARM7 and overlays are retained; only ARM9 caption
pointers and the owned pool/startup bookkeeping change versus V296. All 328 scene
selector/font cases and eight Gallery composites pass, plus exact clean-patch
reconstruction. Full V296 reproduces exactly before and after the builder edit.
A fresh ordinary-input 20,000-frame cold boot traverses title, New Game, Lil's
selection/opening and Amsterdam UI; the complete shopkeeper lines have exact
native font pixels and aligned margins. Experimental; unlocked Gallery/deep
scene navigation, V297 full naming integration and all 18 plaque audits remain
open. Low-resolution Online images remain exempt.
See [V298 release evidence](artwork_caption_release_v298.md).

'''
    for name in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if '## V298:' not in text:
            title, rest = text.split('\n\n', 1)
            path.write_text(title + '\n\n' + section + rest, encoding='utf-8')
    print(f'V298 recorded: 16 captions, 336 native composites, cold boot20000, {sum(r["complete_native_ink_pixels"] for r in lines)} actual complete ink pixels.')


if __name__ == '__main__':
    main()
