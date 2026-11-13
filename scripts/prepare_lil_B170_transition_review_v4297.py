"""Preserve the strict later-region failure and bind focused state/PRNG evidence."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B170_transition_tools_v4297')

if __name__ == '__main__':
    assert not ROOT.exists()
    old = Path('scripts/review_lil_B170_transitions_v4294.py').read_text(encoding='utf-8')
    old_scope = next(line for line in old.splitlines() if line.startswith('        later_difference_scope='))
    new_scope = "        later_difference_scope='All67 later paired SeaView differences remain recorded without masking or retiming. Both scenes reach the same B170 return11257 and following B120 return16053. Viewed16090 departure pair and both20001 final depletion screens: later world outcomes differ. Focused repeats reproduce each same-ROM screen exactly; source/English persistent component fingerprints match at3250,8410,11290 and16090 while the shared PRNG first differs at8410. Original wait/yield/generator spans are source-exact and rebound to the documented scheduler-entropy cause. This supports the same mechanism as an inference, not a fresh B170 every-RAND-call causal trace or equal-random-outcome claim.',"
    supplement = '''    repeat = read(REPEAT)
    assert repeat['paired_post_B170_town11290_whole1A04_actor_models_and_captain2_equal']
    assert repeat['cross_language_command_order_results_and_first_end_equal']
    assert len(repeat['cross_language_speech_timing_differences']) == 22
    assert not any(repeat['same_ROM_later_differing_frames'].values())
    assert all(all(row['component_equality'].values()) for row in repeat['paired_native_persistent_state_and_PRNG_samples'] if row['frame'] <= 16090)
    later_views = []
    for case in ['clean_Japanese', 'reviewed_English']:
        report = read(BASE / ('lil_B170_display_v4292_' + case) / 'capture_report.json')
        photos = {p['frame']: p for p in report['frames_captured']}
        for frame in [16090, 20001]:
            p = photos[frame]
            later_views.append(dict(case=case, frame=frame, path=p['path'], sha256=p['PNG_sha256'], review='Viewed complete diagnostic SeaView: first departure holds share text/UI with lower scene differences; final source water-depletion and English food-depletion screens differ. These later outcomes are explicitly not claimed equal.'))
'''
    tool = derive('scripts/review_lil_B170_transitions_v4294.py', 'scripts/review_lil_B170_transitions_v4297.py', {
        'transition_review_v4294': 'transition_review_v4297',
        "BASE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')": "BASE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')\nREPEAT = Path('work/analysis/lil_B170_repeat_verification_v4296d/post_B170_actor_captain_and_same_ROM_repeat_comparison.json')",
        "assert photo['frame'] >= 16090 and all(192 <= y < 294 for x, y in points)": "assert photo['frame'] >= 16090",
        old_scope: new_scope,
        '    ROOT.mkdir(parents=True)': supplement + '    ROOT.mkdir(parents=True)',
        'all2_runs_cold_boot20001_frames_no_savestate_no_RAM_fixture=True': "all4_runs_cold_boot20001_frames_no_savestate_no_RAM_fixture=True, additional_focused_repeat_proof=str(REPEAT), additional_focused_repeat_proof_sha256=sha(REPEAT.read_bytes()), later_diagnostic_full_screen_views=later_views, original_strict_later_region_failure_preserved='scripts/review_lil_B170_transitions_v4294.py'",
        '[ACTUAL, FONT, Path(__file__)]': '[ACTUAL, FONT, REPEAT, Path(__file__)]',
    })
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tool=tool,
        correction='The original strict reviewer incorrectly limited every later SeaView difference to y192..293. Actual later frames include map, supplies and message changes. Preserve the producer/failure and all67 differences; bind the focused state, PRNG and same-ROM repeat evidence without equal-outcome or direct-causal-trace claims.',
        no_new_emulator_run=True, full_goal_complete=False))
