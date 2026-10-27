"""Record full migration and fresh production/declared-test route display checks."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_reviewed_name_release_v299 import ROOT, read
from scripts.verify_reviewed_name_release_v299 import ROM


def glyphs(font, image, text, x, y, color, bounds):
    expected = {(x + n * 6 + gx, y + gy) for n, c in enumerate(text)
                for gy in range(11) for gx in range(6) if font.decode(c).getpixel((gx, gy))}
    x0, x1 = bounds
    actual = {(gx, gy) for gy in range(y, y + 11) for gx in range(x0, x1)
              if (image.getpixel((gx, gy)) == color if color else max(image.getpixel((gx, gy))) < 20)}
    assert actual == expected, (text, len(actual), len(expected))
    return {'text': text, 'origin': [x, y], 'complete_native_ink_pixels': len(expected),
            'complete_first_internal_final_letters_and_bounds_verified': True}


def main():
    proof = read(ROOT / 'release_proof.json')
    fixture = read(ROOT / 'cold_boot_fixture_manifest.json')
    captures = []
    for name in ('rafael', 'hodram', 'lil', 'maria', 'help_navigation'):
        path = Path(f'work/emulation_v193/reviewed_names_v299_{name}/capture_report.json')
        report = read(path)
        digest = fixture['Maria_test_ROM_sha256'] if name == 'maria' else proof['candidate_sha256']
        assert report['ROM_sha256'] == digest and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors']
        assert report['frames'] == (20000 if name == 'lil' else 30400 if name == 'help_navigation' else 6000)
        if name == 'help_navigation':
            assert all(event['duration'] == 8 for event in report['scripted_input_schedule'] if event['start'] > 20000)
        else:
            assert report['scripted_input_schedule'] == read(ROOT / f'{name}_inputs.json')
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        snapshot = report['read_only_RAM_snapshot']
        assert snapshot['read_only_export'] and sha(Path(snapshot['path']).read_bytes()) == snapshot['sha256']
        captures.append({'route': name, 'frames': report['frames'], 'capture_report': str(path),
                         'capture_report_sha256': sha(path.read_bytes()),
                         'cold_boot_no_savestate_callback_errors_or_RAM_injection': True,
                         'Maria_is_declared_test_selection_not_legitimate_unlock': name == 'maria'})
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    lil = Image.open('work/emulation_v193/reviewed_names_v299_lil/frame_006000_cold_boot.png').convert('RGB')
    actual = [glyphs(font, lil, 'Camille Overijssel', 16, 276, (98, 97, 98), (8, 130))]
    rafael = Image.open('work/emulation_v193/reviewed_names_v299_rafael/frame_006000_final.png').convert('RGB')
    actual.append(glyphs(font, rafael, 'Hey! Wait up, Rafael!', 16, 296, None, (16, 248)))
    town = Image.open('work/emulation_v193/reviewed_names_v299_lil/frame_020000_final.png').convert('RGB')
    actual.append(glyphs(font, town, 'We only sell retail.', 22, 296, None, (16, 248)))
    # Compare every reviewed HELP page against its previously independently
    # verified actual capture, including clicked continuation/return destinations.
    previous = read('work/analysis/help_display_v282/final_navigation_display_proof.json')
    old_report = read('work/emulation_v193/help_navigation_v282_final/capture_report.json')
    new_report = read('work/emulation_v193/reviewed_names_v299_help_navigation/capture_report.json')
    old_frames = {r['frame']: r for r in old_report['frames_captured'] if 'cold_boot' in r['path']}
    new_frames = {r['frame']: r for r in new_report['frames_captured'] if 'navigation' in r['path']}
    frame_mapping = {21200: 24000, 21400: 24400, 21800: 25200, 22000: 25600,
                     22400: 26400, 23000: 28400, 23200: 29200, 23600: 30000}
    page_cases = []
    for row in previous['page_cases']:
        frame, new_frame = row['frame'], frame_mapping[row['frame']]
        assert sha(Path(old_frames[frame]['path']).read_bytes()) == old_frames[frame]['PNG_sha256']
        old, new = Image.open(old_frames[frame]['path']).convert('RGB'), Image.open(new_frames[new_frame]['path']).convert('RGB')
        # Navigation history changes the L/R footer state. Compare the complete
        # title and all ten HELP rows, retaining every glyph and link highlight.
        assert new.crop((0, 0, 256, 352)).tobytes() == old.crop((0, 0, 256, 352)).tobytes(), (frame, new_frame)
        page_cases.append({'frame': new_frame, 'previous_page_case': row,
                           'complete_title_and_all_HELP_rows_exact_previous_independent_native_glyph_proof': True,
                           'history_dependent_L_R_footer_not_claimed_identical': True})
    for before_frame, return_frame in ((25600, 28000), (28400, 30400)):
        a = Image.open(new_frames[before_frame]['path']).convert('RGB')
        b = Image.open(new_frames[return_frame]['path']).convert('RGB')
        assert a.crop((0, 0, 256, 352)).tobytes() == b.crop((0, 0, 256, 352)).tobytes()
    proof.update({'current_actual_cold_boot_and_HELP_navigation_pending': False,
                  'fresh_cold_boot_runs': captures, 'actual_complete_name_dialogue_town_glyphs': actual,
                  'HELP_actual_page_cases': page_cases,
                  'all_previous_reviewed_HELP_actual_title_and_complete_body_rows_exact': True,
                  'both_article_start_return_links_restore_complete_body_pixels': True,
                  'first_HELP_replay_failed_to_enter_HELP_and_is_not_display_evidence': 'work/emulation_v193/reviewed_names_v299_help/capture_report.json',
                  'full_V298_reproduction_before_and_after_builder_changes_exact': True,
                  'experimental_user_acceptance_pending': True, 'full_goal_complete': False})
    assert Path('work/analysis/reviewed_names_v297/v298_before_name_builder_change.nds').read_bytes() == Path('out/all_routes_combined_v298_candidate.nds').read_bytes()
    assert (ROOT / 'v298_after_name_builder_change.nds').read_bytes() == Path('out/all_routes_combined_v298_candidate.nds').read_bytes()
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    checkpoint = {k: v for k, v in proof.items() if k != 'HELP_actual_page_cases'}
    checkpoint.update({'documentation': 'docs/reviewed_name_release_v299.md',
                       'release_proof': str(ROOT / 'release_proof.json'),
                       'HELP_actual_verified_page_frames': len(page_cases),
                       'remaining_untranslated_HELP_topics': 8, 'remaining_generic_HELP_entries': 79,
                       'low_resolution_Online_images_exempt': True})
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / name
        audit = read(path)
        assert not audit['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        assert len(audit['plaque_style_v247']['ongoing_plaque_inventory']) == 18
        assert all(not p['fully_completed'] for p in audit['plaque_style_v247']['ongoing_plaque_inventory'])
        audit['reviewed_name_release_v299'] = checkpoint
        audit['latest_candidate'], audit['latest_candidate_sha256'] = str(ROM), proof['candidate_sha256']
        path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    section = '''## V299: full reviewed naming/text/art migration integrated

All 444 reviewed route paragraphs, five shared names, six COMMON messages and
eight HELP pages join the inherited artwork captions in a registered candidate.
All 467 inherited batches and graphics/fonts/ARM7/overlays remain. All 19,254
actors, 444 complete native bodies, 5,604 expanded copies, 621 getters, 18 COMMON
copies and 24 modal glyph cases pass. All 336 artwork caption composites remain
exact V298. Clean patch reconstruction and full V298 reproduction before/after
builder changes are exact. Three production route cold boots and a declared
Maria test-selection run pass; actual Camille/Rafael letters and town text match
independent font pixels. A fresh production HELP run preserves every previously
reviewed page body and continuation/return navigation. Experimental; deep
scenes/unlocked Gallery, broader graphics contexts and all 18 plaques remain
open. Eight Japanese HELP topics and 79 generic entries remain unfinished;
this migration does not claim full HELP localization. Online images stay exempt.
See [V299 release evidence](reviewed_name_release_v299.md).

'''
    for name in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if '## V299:' not in text:
            title, rest = text.split('\n\n', 1)
            path.write_text(title + '\n\n' + section + rest, encoding='utf-8')
    print(f'V299 full migration recorded; five cold boots; {len(page_cases)} actual HELP frames; complete Camille/Rafael/town glyphs.', flush=True)


if __name__ == '__main__':
    main()
