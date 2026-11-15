"""Prepare completion producers with33 pending reviews and no premature credit."""
import re
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/lil_B170_completion_tools_v4307b')
NEW = Path('scripts/complete_lil_B170_v4307b.py')

if __name__ == '__main__':
    assert not ROOT.exists() and not NEW.exists()
    old = Path('scripts/complete_lil_B169_v4255b.py')
    text = old.read_text(encoding='utf-8')
    changes = {
        'B169': 'B170', 'lil_B169': 'lil_B170',
        'completion_v4255': 'completion_v4307', 'completion_text_v4255': 'completion_text_v4307',
        'editorial_manuscript_v5': 'editorial_manuscript_v6',
        'release_v4252': 'release_v4304', 'startup_v4254': 'startup_v4306',
        'actual_v4244/actual_progressive_three_predicates_full_effect_and_return': 'actual_v4293/actual_all33_pause_resources_A000_C200_and_first_end',
        'transition_review_v4245/all6_sheets_source_effect_and_paired_return_review': 'transition_review_v4297/all6_sheets_figure_pause_effect_C200_and_paired_return_review',
        'reference_checkpoint_v4247': 'reference_checkpoint_v4299', 'registration_v4250b': 'registration_v4302b',
        "'Lil-B169-Mikhail-Proof-legend-clues-ruins-tavern-give-and-take36'": "'Lil-B170-Yifa-collision-apology-Taoist-training-resolve-joining33'",
        "OFFLINE = {'DK4_MES_B169_R0067', 'DK4_MES_B169_R0082', 'DK4_MES_B169_R0097'}": 'OFFLINE = set()',
        'all545_manifest_batches_and114_accepted_layers_present': 'all546_manifest_batches_and114_accepted_layers_present',
        'all_current_requested_and_final_framebuffers_equal_V4204': 'all_current_requested_and_final_framebuffers_equal_V4251',
        "assert set(sample['offline_only_display_IDs']) == OFFLINE and sample['three_conditional_remarks_not_actual_or_byte_identical_reuse']": "assert not sample['offline_only_display_IDs'] and sample['actual33_progressive_panels_figure_pause_resources_A000_C200_first_end_and_normal_town_return_pass']",
        '[169]': '[170]', 'block=169': 'block=170', 'actual_source_event169_selected': 'actual_source_event170_selected',
        'actual_selected_B169_source_events': 'actual_selected_B170_source_events',
        'source_prose_credit_already_recorded_in_V4231': 'source_prose_credit_already_recorded_in_V4279',
        'all36_exact_source_predecessor_runtime_logical_and_integrated_references_bound': 'all33_exact_source_predecessor_runtime_logical_and_integrated_references_bound',
        "# Current editorial handoff - V4247": '# Current editorial handoff - V4299',
        'B170-B180': 'B171-B180', 'remaining_B170_B180': 'remaining_B171_B180',
        "['lil_B169_v4231']": "['lil_B170_v4279']", "['lil_B169_v4255']": "['lil_B170_v4307']",
        'unfinished_editorial_scope_v4247': 'unfinished_editorial_scope_v4299',
        'unfinished_editorial_scope_v4255': 'unfinished_editorial_scope_v4307',
        'lil_B169_completed_v4255': 'lil_B170_completed_v4307',
        "Path(doc['source_effect_operand_notation_amendment'])": "Path(doc['focused_repeat_proof'])",
        "Path('scripts/lil_B169_completion_text_v4255.py')": "Path('scripts/lil_B170_completion_text_v4307.py'), Path('work/analysis/lil_B170_release_tools_v4303/regression_test_results.json')",
        'V4255': 'V4307', 'V4251': 'V4303',
        'all36-source-native-reference-representative-release-checks-pass': 'all33-source-native-reference-representative-release-checks-pass',
        'all_jobs_terminal=True': 'all_jobs_terminal=True',
        'manifest_batches=545': 'manifest_batches=546',
        'new_actual_emulator_runs=4': 'new_actual_emulator_runs=6', 'new_emulator_runs=4': 'new_emulator_runs=6',
        'new_actual_fixture_runs=2, new_registered_startup_runs=2': 'new_actual_fixture_runs=2, new_focused_repeat_runs=2, new_registered_startup_runs=2',
        'new_current_candidate_emulator_runs=2, new_explicit_display_fixture_runs=2': 'new_current_candidate_emulator_runs=2, new_explicit_display_fixture_runs=2, new_focused_repeat_runs=2',
        "'promoted_main_build_v4226']": "'promoted_main_build_v4226', 'promoted_main_build_v4289']",
    }
    for key in changes:
        assert key in text, key
    text = re.sub('|'.join(re.escape(k) for k in sorted(changes, key=len, reverse=True)), lambda m: changes[m.group()], text)
    # Counts are replaced simultaneously: old completed5692 is not itself
    # recursively transformed after the old parent completion5656 becomes5692.
    counts = {'5656': '5692', '5692': '5725', '5695': '5728', '3614': '3635', '2078': '2090',
              '3839': '3872', '4093': '4126', '36': '33', '19': '21', '17': '12', '55': '63', '231': '198'}
    text = re.sub(r'(?<!\d)(?:' + '|'.join(re.escape(k) for k in sorted(counts, key=len, reverse=True)) + r')(?!\d)', lambda m: counts[m.group()], text)
    # V4251 is still the promoted pointer in copied preservation keys; only
    # this producer's release labels change to V4303. Main records are not edited.
    assert 'B169' not in text and 'lil_B169' not in text and 'source_effect_operand_notation_amendment' not in text
    assert 'B120' not in text and '[120]' not in text and 'B170' in text
    compile(text, str(NEW), 'exec')
    NEW.write_text(text, encoding='utf-8', newline='\n')
    tools = [dict(previous=str(old), previous_sha256=sha(old.read_bytes()), successor=str(NEW), successor_sha256=sha(NEW.read_bytes()))]
    assert Path('scripts/apply_lil_B170_completion_v4307.py').exists() and Path('scripts/seal_lil_B170_completion_v4307.py').exists()
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tools=tools, expected_completed=5725, expected_pending=0,
        expected_source_prose_unchanged=5728, revised=21, retained=12, new_completed_records=33,
        required_atomic_negative_count=63, required_registered_startup_pairs=31, expected_emulator_runs_in_family=6,
        copied_native_actual_proofs_not_reexecuted=True, unexecuted_predecessor_digit_substitution_preserved=True, completion_execution_pending_release_and_startup=True,
        current_main_remains_V4251=True, full_goal_complete=False))
    print('B170 completion tools prepared;33 completion credits remain gated by registered patch/startup proofs.')
