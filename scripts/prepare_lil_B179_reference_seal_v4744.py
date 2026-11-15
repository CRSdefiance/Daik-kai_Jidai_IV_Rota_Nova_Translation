"""Prepare a B179 reference seal bound to fresh14-panel actual evidence."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B179_reference_seal_tools_v4744')
assert not ROOT.exists()
tool=derive('scripts/seal_lil_B178_references_v4696.py','scripts/seal_lil_B179_references_v4744.py',{
    'B178':'B179','prepare_lil_B178_research_v4685':'prepare_lil_B179_research_v4733',
    'reference_approval_v4696':'reference_approval_v4744',
    'reference_census_v4688b':'reference_census_v4736','relocated_controls_v4690':'relocated_controls_v4738',
    'all13_progressive_FE_dispatches_A000_C200_pairs_and3_leaves':'all14_progressive_FE_dispatches_A000_pairs_and2_leaves',
    'stored_v4682/all13_final_stored_targets52':'stored_v4730/all14_final_stored_targets56',
    'ends_v4689':'ends_v4737','actual_v4694/actual_all13_progressive_FE_A000_C200_and_single_end':
        'actual_v4742/actual_all14_progressive_FE_A000_and_single_end_no_C200',
    'display_fixture_v4691':'display_fixture_v4739',
    'actual_review_v4695/all3_actual_sheets13_planes':'actual_review_v4743/all3_actual_sheets14_planes',
    "len(control['relocated_dispatch_cases'])==13":"len(control['relocated_dispatch_cases'])==14",
    "len(control['all3_source_current_target_nonrelative_nonspeech_leaves'])==3":
        "len(control['all2_source_current_target_nonrelative_nonspeech_leaves'])==2",
    "len(control['relocated_C200_pairs'])==len(control['relocated_A000_structural_pairs'])==1":
        "len(control['relocated_C200_pairs'])==0 and len(control['relocated_A000_structural_pairs'])==1",
    'all12_progressive_static_actors':'all13_progressive_static_actors',
    "len(stored['final_target_parity_cases'])==13 and stored['current_final_stored_macro_alignment_cases']==52":
        "len(stored['final_target_parity_cases'])==14 and stored['current_final_stored_macro_alignment_cases']==56",
    '==(28,24)':'==(20,36)','all13_final_targets':'all14_final_targets',
    "actual['complete_matching_observations']==13":"actual['complete_matching_observations']==14",
    'single_source_end490_actually_reached':'single_source_end508_actually_reached',
    '[5977,5976]':'[6216,6215]',
    "len(visual['paired_full_screen_views'])==4 and sum(len(s['frames'])*2 for s in visual['paired_full_screen_views'])==16":
        "len(visual['paired_full_screen_views'])==5 and sum(len(s['frames'])*2 for s in visual['paired_full_screen_views'])==20",
    "{'total':14,'speech':12,'control_or_end':2}":"{'total':8,'speech':7,'control_or_end':1}",
    "len(visual['actual_timing_differences'])==14":"len(visual['actual_timing_differences'])==8",
    "row['frame']>=6010":"row['frame']>=6250",'[3306586022,3306586022]':'[403514907,403514907]',
    'len(set(ids))==13':'len(set(ids))==14',
    "native['all13_current_native_speech_planes_pass'] and native['current_original_macro_alignment_calls']==104":
        "native['all14_current_native_speech_planes_pass'] and native['current_original_macro_alignment_calls']==112",
    'all13_panels12_progressive1_impersonal_FE_source_A000_C200_single_end_and_normal_parent_return_pass':
        'all14_panels13_progressive1_impersonal_FE_source_A000_single_end_no_C200_and_normal_parent_return_pass',
    'source_end490_actual_target452_offline_and_fixture_end_actual':'source_end508_actual_target492_offline_and_fixture_end_actual',
    'all115_upper_portrait_name_samples_equal_and14_command_timing_differences_retained':
        'all115_upper_portrait_name_samples_equal_and8_command_timing_differences_retained',
    'five_native_state_components_whole1A04_actor_captain2_and_PRNG3306586022_equal':
        'five_native_state_components_whole1A04_actor_captain2_and_PRNG403514907_equal',
    "block['block']==checked['block']==178":"block['block']==checked['block']==179",
    "len(block['text_records'])==13":"len(block['text_records'])==14",
    '[(490,452)]':'[(508,492)]','all13_active_speech_targets':'all14_active_speech_targets',
    'all3_leaves_one_A000_C200_and_single_end_exact':'all2_leaves_one_A000_and_single_end_no_C200_exact',
    'progressive12_impersonal_FE1':'progressive13_impersonal_FE1',
    'single_end490_actual_target452_offline':'single_end508_actual_target492_offline',
    'all13_source_native_reference':'all14_source_native_reference','single_end490_actually_reached':'single_end508_actually_reached',
    'all thirteen actual panels,16 source commands,A000,C200,single end and normal parent return.':
        'all fourteen actual panels,16 source commands,A000,single end,no C200 and normal parent return.',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,source_speeches14_commands16_A0001_end1_no_C200=True,
    fresh_eight_timing_four_indicator_differences_twenty_fullscreens_bound=True,
    no_inherited_previous_block_outcome=True,main_V4701_unchanged=True,full_goal_complete=False))
