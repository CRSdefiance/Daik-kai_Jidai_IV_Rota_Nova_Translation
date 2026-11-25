"""Prepare paired cold-boot content fixtures with all53 B169 commands intact."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B169_display_tools_v4241')

if __name__ == '__main__':
    assert not ROOT.exists()
    tools = [derive('scripts/research_lil_B168_display_fixture_v4198.py','scripts/research_lil_B169_display_fixture_v4241.py',{
        'B168':'B169','lil_B168':'lil_B169',
        'display_fixture_v4198':'display_fixture_v4241','display_v4198':'display_v4241',
        'all_routes_combined_v4160':'all_routes_combined_v4204',
        'relocation_v4190':'relocation_v4233','editorial_manuscript_v7':'editorial_manuscript_v4',
        '[168]':'[169]','source_block=168':'source_block=169',
        'len(commands) == 82':'len(commands) == 53','len(walk) == 91 and len(speeches) == 54':'len(walk) == 62 and len(speeches) == 36',
        "sum(command['word'] == 0 for command in walk) == 2":"sum(command['word'] == 0 for command in walk) == 1",
        'all91_stored_fixture_commands':'all62_stored_fixture_commands',
        'all12_relative_operands_three_predicates_and_both_ends_preserved':'all12_relative_operands_three_predicates_and_single_tail_end_preserved',
        'all54_source_texts_including3_FE_and_later_A000_retained_without_flattening':'all36_progressive_source_texts_and_later_A000_retained_without_flattening',
        'source_event168_not_selected':'source_event169_not_selected',
        'source_B168_later_A000_and_all_resources_presentations_and_FE_notices_preserved':'source_B169_later_numeric29_0001_A000_and_no_invented_resources_presentations_FE',
        "['DK4_MES_B168_R0020', 'DK4_MES_B168_R0048', 'DK4_MES_B168_R0135']":"['DK4_MES_B169_R0067', 'DK4_MES_B169_R0082', 'DK4_MES_B169_R0097']",
        'stored_speech_objects=54':'stored_speech_objects=36',
        'Paired B168 fixtures:54 speeches/3 FE,12 spans,three unforced predicates and later A000;no source command omitted.':'Paired B169 fixtures:36 progressive speeches,12 spans,three unforced predicates and later numeric29/0001 A000;no source command omitted.',
    })]
    tools.append(derive('scripts/run_lil_B168_display_fixture_v4199.py','scripts/run_lil_B169_display_fixture_v4242.py',{
        'B168':'B169','lil_B168':'lil_B169','display_fixture_v4198':'display_fixture_v4241',
        'display_run_v4199':'display_run_v4242','display_v4199':'display_v4242',
        'source_event168_not_selected':'source_event169_not_selected',
        "'displayed_original_source_block':168":"'displayed_original_source_block':169",
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_block=169,speeches=36,source_commands=53,
        stored_fixture_commands=62,original_B22_init_commands=9,original_B22_init_A000=4,
        later_A000_numeric_operands=[29,1],source_end_offset=2558,
        no_source_command_omission_flattening_or_forced_predicate=True,
        no_natural_eligibility_recruitment_or_earned_flag_claim=True,new_emulator_runs=0,full_goal_complete=False))
    print('Paired B169 content fixtures and20001-frame cold-boot runners prepared;all commands/effects retained.')
