"""Bind viewed B170 planes, original figure/pause/effects and paired town return."""
import re
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B170_transition_review_v4294')
ACTUAL = Path('work/analysis/lil_B170_actual_v4293/actual_all33_pause_resources_A000_C200_and_first_end.json')
FONT = Path('work/analysis/lil_B170_native_approval_v4278/all33_native_progressive_and_source_reconciliation.json')
BASE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')

if __name__ == '__main__':
    assert not ROOT.exists()
    actual, font = map(read, [ACTUAL, FONT])
    assert not actual['failures'] and not actual['paired_region_differences']
    assert actual['fresh_actual_unique_speech_panels'] == actual['complete_matching_observations'] == 33
    assert not actual['offline_only_display_IDs']
    views = []
    for frame, note in [(3130, 'Original Yifa full-figure transition during the collision; complete Lil portrait and Ah reaction.'),
                        (3250, 'Original full figure, changed background and cleared lower panel during the source2000 pause.'),
                        (8410, 'Complete Yifa Sol portrait/name and Taoist-training speech; teacher gender remains unspecified.'),
                        (11290, 'Normal initialized Amsterdam town return after final encouragement, source A000 hex1019/2001, C200 and first end1852.')]:
        path = BASE / 'lil_B170_display_v4292_reviewed_English' / f'frame_{frame:06d}_cold_boot.png'
        assert Image.open(path).size == (256, 384)
        views.append(dict(frame=frame, path=str(path), sha256=sha(path.read_bytes()), review='Viewed complete full screen. ' + note))
    source_views, returns = [], []
    for frame in [3250, 8410, 11290]:
        jp = BASE / 'lil_B170_display_v4292_clean_Japanese' / f'frame_{frame:06d}_cold_boot.png'
        en = BASE / 'lil_B170_display_v4292_reviewed_English' / f'frame_{frame:06d}_cold_boot.png'
        a, b = [Image.open(p).convert('RGB') for p in [jp, en]]
        source_views.append(dict(frame=frame, path=str(jp), sha256=sha(jp.read_bytes()), review='Viewed complete Japanese-content counterpart: same original figure/pause, character/scene or town return.'))
        assert a.crop((0, 0, 256, 294)).tobytes() == b.crop((0, 0, 256, 294)).tobytes()
        if frame in [3250, 11290]:
            assert a.tobytes() == b.tobytes()
            returns.append(dict(frame=frame, source=str(jp), source_sha256=sha(jp.read_bytes()), English=str(en), English_sha256=sha(en.read_bytes()), whole_RGB_equal=True, case='pause' if frame == 3250 else 'town_return'))
    sheets = []
    for sheet in actual['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
        sheets.append({**sheet, 'review': 'Viewed complete actual sheet: all first/internal/final glyphs, Lil/Yifa portraits and full native nameplates. Collision, irritation, apology, flattery, Admiral/FO explanation, teacher/Taoist training, resolve, explicit passage request and final encouragement read coherently. No translation-specific display finding.'})
    assert len(sheets) == 6
    for version in actual['versions']:
        assert version['fixture_exit_frame'] == 11257 and len(version['selected_B22_command_pairs']) == 53
        assert version['selected_B22_command_pairs'][-1]['result_words'] == [0, 0]
        assert version['actual_source_A000_hex1019_2001']['result_words'] == [3, 0]
        assert version['actual_C200']['result_words'] == [3, 0]
        assert [(p['start'], p['returned']) for p in version['actual_pause_and_resume']] == [(3200, 3332), (3332, 3576)]
        assert version['source_first_end_offset'] == 1852
    doc = read('translations/lil_B170_editorial_manuscript_v5.json')
    ids = {row['id'] for row in actual['actual_panels']}
    macro_counts = {macro: sum(len(re.findall(r'\{MACRO:' + macro + r'\}', row['english'])) for row in doc['records'] if row['id'] in ids) for macro in ['FI', 'FA', 'FO']}
    assert macro_counts == {'FI': 1, 'FA': 0, 'FO': 1}
    reports = [read(BASE / ('lil_B170_display_v4292_' + case) / 'capture_report.json') for case in ['clean_Japanese', 'reviewed_English']]
    jp_photos = {p['frame']: p for p in reports[0]['frames_captured']}
    region_checks, later_differences = [], []
    for photo in reports[1]['frames_captured']:
        source = jp_photos[photo['frame']]
        for p in [source, photo]:
            assert sha(Path(p['path']).read_bytes()) == p['PNG_sha256']
        a, b = [Image.open(p['path']).convert('RGB') for p in [source, photo]]
        equal = a.crop((0, 0, 256, 294)).tobytes() == b.crop((0, 0, 256, 294)).tobytes()
        region_checks.append(dict(frame=photo['frame'], source=source['path'], source_sha256=source['PNG_sha256'], English=photo['path'], English_sha256=photo['PNG_sha256'], upper_and_portrait_name_regions_equal=equal))
        if not equal:
            points = [(x, y) for y in range(384) for x in range(256) if a.getpixel((x, y)) != b.getpixel((x, y))]
            assert photo['frame'] >= 16090 and all(192 <= y < 294 for x, y in points)
            later_differences.append(dict(frame=photo['frame'], differing_RGB_pixels=len(points), bounds=[min(x for x, y in points), min(y for x, y in points), max(x for x, y in points) + 1, max(y for x, y in points) + 1], difference_after_B170_exit_and_subsequent_B120_exit=True))
    assert len(region_checks) == 299 and len(later_differences) == 67
    assert all(p['upper_and_portrait_name_regions_equal'] for p in region_checks if p['frame'] <= 16053)
    following = []
    for report in reports:
        trace = read(Path(report['output']) / 'observer/commands.json') if 'output' in report else None
        # Capture folder is derived from the already hash-bound first photograph.
        if trace is None:
            trace = read(Path(report['frames_captured'][0]['path']).parent / 'observer/commands.json')
        rows = trace['rows']
        pairs = []
        for row in rows:
            if row['kind'] != 'after_command':
                continue
            entry = rows[row['entry_row']]
            if entry['source']['block'] == 120:
                pairs.append(dict(offset=entry['source']['instruction_offset'], start=entry['frame'], returned=row['frame'], extent=row['decoded_length'], result_words=row['result_words']))
        assert pairs and pairs[-1]['offset'] == 2312 and pairs[-1]['returned'] == 16053
        following.append(pairs)
    assert following[0] == following[1]
    ROOT.mkdir(parents=True)
    save(ROOT / 'all6_sheets_figure_pause_effect_C200_and_paired_return_review.json', dict(
        actual_proof=str(ACTUAL), actual_proof_sha256=sha(ACTUAL.read_bytes()), all6_actual_sheets_viewed=sheets,
        English_full_screen_views=views, Japanese_full_screen_views=source_views, paired_source_English_whole_RGB_pause_and_returns=returns,
        all33_actual_progressive_panels_complete=True, actual_Lil_Yifa_original_nameplates_portraits_full_figure_and_figure_removal_verified=True,
        actual_FI1_FA0_FO1_expansions_verified_by_complete_native_masks=macro_counts,
        actual_pause3200_to3332_and_resume_observed=True, original_resources_and_presentation_transitions_preserved=True,
        original_A000_hex1019_2001_after_encouragement_C200_and_first_end_return_normally=True,
        source_effect_operand_hex_words=['1019', '2001'], source_effect_packed_semantics_not_inferred=True,
        first_end1852_actual_second_end1856_stored_and_native_decoder_only=True,
        all299_paired_capture_region_checks=region_checks, later67_SeaView_RGB_differences=later_differences,
        later_difference_scope='After both B170 returns11257 and byte-identical subsequent B120 command sequences ending16053. Viewed paired Sea View16090: differences occupy only the lower scene region, while the upper map/UI and all text planes agree. Record without masking or retiming; do not claim whole-frame identity for these67 later frames. No translation-specific glyph/control defect observed.',
        following_B120_original_command_pairs=following[0], following_B120_captured_not_fresh_editorial_completion=True,
        source_and_English_timing_recorded_without_false_later_SeaView_whole_frame_equality=True,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True, no_open_translation_specific_display_or_control_finding=True,
        source_event170_eligibility_earned_flag_full_playthrough_or_hardware_test_not_claimed=True,
        no_B170_source_command_omitted_or_forced=True, original_B22_four_A000_initialization_commands_retained=True,
        all2_runs_cold_boot20001_frames_no_savestate_no_RAM_fixture=True, new_emulator_runs_added_by_this_review=0,
        evidence={str(p): sha(p.read_bytes()) for p in [ACTUAL, FONT, Path(__file__)]}, full_goal_complete=False))
    print('Viewed6 actual sheets,4 English and3 Japanese full screens;33 exact panels,pause,source effect,C200 and RGB-identical town return.67 later SeaView differences retained separately.')
