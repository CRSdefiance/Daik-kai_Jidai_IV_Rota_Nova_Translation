"""Prepare paired full-content B170 fixtures and ordinary read-only cold boots."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B170_display_tools_v4291')

if __name__ == '__main__':
    assert not ROOT.exists()
    tools = [derive('scripts/research_lil_B169_display_fixture_v4241.py', 'scripts/research_lil_B170_display_fixture_v4291.py', {
        'B169': 'B170', 'lil_B169': 'lil_B170',
        'display_fixture_v4241': 'display_fixture_v4291', 'display_v4241': 'display_v4291',
        'all_routes_combined_v4204': 'all_routes_combined_v4251',
        'relocation_v4233': 'relocation_v4281', 'editorial_manuscript_v4': 'editorial_manuscript_v5',
        '[169]': '[170]', 'source_block=169': 'source_block=170',
        'len(commands) == 53': 'len(commands) == 45',
        'len(walk) == 62 and len(speeches) == 36': 'len(walk) == 54 and len(speeches) == 33',
        "sum(command['word'] == 0x8000 for command in walk) == 3": "sum(command['word'] == 0x8000 for command in walk) == 0",
        "sum(command['word'] in [0x100, 0x200, 0x300, 0x400] for command in walk) == 12": "sum(command['word'] in [0x100, 0x200, 0x300, 0x400] for command in walk) == 0",
        "sum(command['word'] == 0 for command in walk) == 1": "sum(command['word'] == 0 for command in walk) == 2",
        'all62_stored_fixture_commands': 'all54_stored_fixture_commands',
        'all12_relative_operands_three_predicates_and_single_tail_end_preserved': 'zero_relative_sites_zero_predicates_and_both_declared_ends_preserved',
        'all36_progressive_source_texts_and_later_A000_retained_without_flattening': 'all33_progressive_source_texts_pause_resources_later_A000_and_C200_retained_without_flattening',
        'source_event169_not_selected_or_eligibility_earned': 'source_event170_not_selected_or_eligibility_earned',
        'source_B169_later_numeric29_0001_A000_and_no_invented_resources_presentations_FE': 'source_B170_later_A000_hex1019_2001_resources_presentations_pause_C200_and_both_ends_retained',
        'all_three_original_membership_queries_retained_unforced': 'no_original_membership_queries_or_relative_sites',
        "['DK4_MES_B169_R0067', 'DK4_MES_B169_R0082', 'DK4_MES_B169_R0097']": '[]',
        'stored_speech_objects=36': 'stored_speech_objects=33',
        'actual_conditional_path_to_be_observed_without_forcing': 'actual_linear_path_pause_effect_C200_and_end_reachability_to_be_observed',
        'Paired B169 fixtures:36 progressive speeches,12 spans,three unforced predicates and later numeric29/0001 A000;no source command omitted.': 'Paired B170 fixtures:33 progressive speeches,45 source commands plus9 original init commands;pause,resources,later A000,C200 and both ends retained.',
    })]
    tools.append(derive('scripts/run_lil_B169_display_fixture_v4242.py', 'scripts/run_lil_B170_display_fixture_v4292.py', {
        'B169': 'B170', 'lil_B169': 'lil_B170',
        'display_fixture_v4241': 'display_fixture_v4291',
        'display_run_v4242': 'display_run_v4292', 'display_v4242': 'display_v4292',
        'source_event169_not_selected': 'source_event170_not_selected',
        "'displayed_original_source_block':169": "'displayed_original_source_block':170",
    }))
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tools=tools, source_block=170, speeches=33, source_commands=45,
        stored_fixture_commands=54, original_B22_init_commands=9, original_B22_init_A000=4,
        source_A000_operand_hex_words=['1019', '2001'], source_A000_semantics_not_inferred=True,
        source_declared_end_offsets=[1852, 1856], source_pause_offset=36, source_pause_resume=38,
        no_source_command_omission_flattening_or_forced_predicate=True,
        no_natural_eligibility_recruitment_or_earned_flag_claim=True, new_emulator_runs=0, full_goal_complete=False))
    print('Prepared paired complete B170 fixtures and20001-frame cold boots;all45 commands retained.')
