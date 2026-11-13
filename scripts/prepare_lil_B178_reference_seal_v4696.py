"""Prepare complete B178 reference approval with measured actual limits retained."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B178_reference_seal_tools_v4696');assert not ROOT.exists()
tool=derive('scripts/seal_lil_B177_references_v4640.py','scripts/seal_lil_B178_references_v4696.py',{
    'prepare_lil_B177_research_v4629':'prepare_lil_B178_research_v4685',
    'lil_B177_reference_approval_v4640':'lil_B178_reference_approval_v4696',
    'lil_B177_editorial_manuscript_v5':'lil_B178_editorial_manuscript_v3',
    'lil_B177_editorial_manuscript_v6':'lil_B178_editorial_manuscript_v4',
    'lil_B177_reference_census_v4632/all13_commands':'lil_B178_reference_census_v4688b/all16_commands',
    'lil_B177_relocated_controls_v4634/all10_progressive':'lil_B178_relocated_controls_v4690/all13_progressive',
    'lil_B177_stored_v4626/all10_final_stored_targets40':'lil_B178_stored_v4682/all13_final_stored_targets52',
    'lil_B177_ends_v4633':'lil_B178_ends_v4689',
    'lil_B177_actual_v4638/actual_all10_progressive':'lil_B178_actual_v4694/actual_all13_progressive',
    'lil_B177_display_fixture_v4635/complete_B177':'lil_B178_display_fixture_v4691/complete_B178',
    'lil_B177_actual_review_v4639/all2_actual_sheets10':'lil_B178_actual_review_v4695/all3_actual_sheets13',
    "len(control['relocated_dispatch_cases'])==10":"len(control['relocated_dispatch_cases'])==13",
    'all9_progressive_static_actors':'all12_progressive_static_actors',
    "len(stored['final_target_parity_cases'])==10 and stored['current_final_stored_macro_alignment_cases']==40":
        "len(stored['final_target_parity_cases'])==13 and stored['current_final_stored_macro_alignment_cases']==52",
    '==(24,16)':'==(28,24)',
    "actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==10":
        "actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==13",
    "len(v['selected_B22_command_pairs'])==22":"len(v['selected_B22_command_pairs'])==25",
    'single_source_end482_actually_reached':'single_source_end490_actually_reached','==[5255,5257]':'==[5977,5976]',
    "len(visual['all2_actual_sheets_viewed'])==2":"len(visual['all3_actual_sheets_viewed'])==3",
    'all2_actual_sheets_viewed':'all3_actual_sheets_viewed',
    "len(visual['paired_full_screen_views'])==3":"len(visual['paired_full_screen_views'])==4",
    "for s in visual['paired_full_screen_views'])==12":"for s in visual['paired_full_screen_views'])==16",
    "{'total':11,'speech':9,'control_or_end':2}":"{'total':14,'speech':12,'control_or_end':2}",
    "len(visual['actual_timing_differences'])==11":"len(visual['actual_timing_differences'])==14",
    'fourteen_following_A_button_indicator_animation_differences_retained_unmasked':'sampled_postscene_whole_RGB_differences_unmasked',
    'len(differences)==14':'len(differences)==4',
    'fourteen_following_indicator_differences_viewed_in_representative_full_screens_and_retained':'all_four_following_indicator_differences_viewed_in_full_and_retained',
    'whole_RGB_town5290_through5950_and_final9001_equal':'sampled_postscene_whole_RGB_equal_except_four_original_A_indicator_frames',
    "and not visual['PRNG_equality'] and visual['postscene9001_PRNG_seeds']==[463267532,403514907]":
        "and visual['PRNG_equality'] and visual['postscene9001_PRNG_seeds']==[3306586022,3306586022]",
    'source_all13_commands':'source_all16_commands','all22_stored_fixture_commands':'all25_stored_fixture_commands',
    "f['all22_stored_fixture_commands'])==22":"f['all25_stored_fixture_commands'])==25",
    'len(set(ids))==10':'len(set(ids))==13',"native['current_original_macro_alignment_calls']==80":"native['current_original_macro_alignment_calls']==104",
    'all13_clean_current_target_commands':'all16_clean_current_target_commands',
    'all10_panels9_progressive1_impersonal_FE_source_A000_C200_single_end_and_normal_town_return_pass':
        'all13_panels12_progressive1_impersonal_FE_source_A000_C200_single_end_and_normal_parent_return_pass',
    'original13_commands':'original16_commands',
    'source_end482_actual_target466_offline_and_fixture_end_actual':'source_end490_actual_target452_offline_and_fixture_end_actual',
    'all115_upper_portrait_name_samples_equal_and11_command_timing_differences_retained':
        'all115_upper_portrait_name_samples_equal_and14_command_timing_differences_retained',
    'whole_RGB_town_return_and_final_following_tutorial_equal':'postscene_whole_RGB_except_four_A_indicator_frames_and_final9001_equal',
    'five_native_state_components_whole1A04_actor_captain2_equal_PRNG_difference_retained':
        'five_native_state_components_whole1A04_actor_captain2_and_PRNG3306586022_equal',
    "block['block']==checked['block']==177":"block['block']==checked['block']==178",
    "len(block['command_map'])==13 and len(block['text_records'])==10":"len(block['command_map'])==16 and len(block['text_records'])==13",
    '==[(482,466)]':'==[(490,452)]','all13_structural_commands':'all16_structural_commands',
    'progressive9_impersonal_FE1':'progressive12_impersonal_FE1','single_end482_actual_target466_offline':'single_end490_actual_target452_offline',
    'single_end482_actually_reached':'single_end490_actually_reached',
    'all10':'all13','lil_B177':'lil_B178','B177':'B178',
    'references sealed:all ten actual panels,13 source commands,A000,C200,single end and normal town return.':
        'references sealed:all thirteen actual panels,16 source commands,A000,C200,single end and normal parent return.',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,actual13_panels25_commands14_timings4_unmasked_indicator_differences_bound=True,
    all3_actual_sheets_and16_full_screens_viewed=True,postscene_components_actor_PRNG_and_final_RGB_equal=True,
    no_source_event_eligibility_earned_state_full_RAM_future_world_or_hardware_claim=True,
    no_ROM_registry_ledger_orcredit_change_yet=True,full_goal_complete=False))
